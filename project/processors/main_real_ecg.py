from pathlib import Path
import json
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, classification_report, ConfusionMatrixDisplay,
    f1_score, precision_score, recall_score,
)
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
RESULTS_DIR = ROOT / "results"
RESULTS_DIR.mkdir(exist_ok=True)


def load_split(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Could not find {path}. Put the CSV in the project's Data folder.")
    frame = pd.read_csv(path, header=None)
    if frame.shape[1] != 188:
        raise ValueError(f"{path.name} has {frame.shape[1]} columns; expected 188 (187 ECG values + 1 label).")
    X = frame.iloc[:, :-1].to_numpy(dtype=np.float32)
    y = frame.iloc[:, -1].to_numpy(dtype=np.int64)
    return X, y


def main():
    print("Loading MIT-BIH heartbeat CSV files...")
    X_train, y_train = load_split(DATA_DIR / "mitbih_train.csv")
    X_test, y_test = load_split(DATA_DIR / "mitbih_test.csv")
    print(f"Training rows: {len(y_train):,}; features per row: {X_train.shape[1]}")
    print(f"Test rows:     {len(y_test):,}; features per row: {X_test.shape[1]}")
    print("Training classical baseline: StandardScaler + Logistic Regression...")
    started = time.time()
    model = make_pipeline(
        StandardScaler(),
        LogisticRegression(max_iter=300, class_weight="balanced", solver="lbfgs", random_state=42),
    )
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    accuracy = float(accuracy_score(y_test, y_pred))
    macro_precision = float(precision_score(y_test, y_pred, average="macro", zero_division=0))
    macro_recall = float(recall_score(y_test, y_pred, average="macro", zero_division=0))
    macro_f1 = float(f1_score(y_test, y_pred, average="macro", zero_division=0))
    weighted_f1 = float(f1_score(y_test, y_pred, average="weighted", zero_division=0))
    report_text = classification_report(y_test, y_pred, zero_division=0)
    report_dict = classification_report(y_test, y_pred, output_dict=True, zero_division=0)

    results = {
        "project": "ALGOX - PS-Q1 Biomedical Signal Classifier",
        "dataset": "Kaggle ECG Heartbeat Categorization Dataset (MIT-BIH CSV split)",
        "dataset_note": "External dataset; confirm hackathon rules and dataset terms before submission.",
        "model": "StandardScaler + LogisticRegression(class_weight='balanced', max_iter=300)",
        "train_samples": int(len(y_train)), "test_samples": int(len(y_test)),
        "features_per_sample": int(X_train.shape[1]),
        "class_labels_seen_in_train": sorted(int(v) for v in np.unique(y_train)),
        "class_labels_seen_in_test": sorted(int(v) for v in np.unique(y_test)),
        "accuracy": accuracy, "macro_precision": macro_precision,
        "macro_recall": macro_recall, "macro_f1": macro_f1,
        "weighted_f1": weighted_f1,
        "elapsed_seconds": round(time.time() - started, 2),
        "classification_report": report_dict,
        "scope_note": "Classical ML results only; not quantum-hardware results or Processor A/B benchmark results.",
    }
    (RESULTS_DIR / "ecg_metrics.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    pd.DataFrame([{
        "accuracy": accuracy, "macro_precision": macro_precision,
        "macro_recall": macro_recall, "macro_f1": macro_f1,
        "weighted_f1": weighted_f1, "train_samples": len(y_train), "test_samples": len(y_test),
    }]).to_csv(RESULTS_DIR / "ecg_metrics.csv", index=False)

    print("\n=== Test-set results ===")
    print(f"Accuracy:         {accuracy:.4f}")
    print(f"Macro precision:  {macro_precision:.4f}")
    print(f"Macro recall:     {macro_recall:.4f}")
    print(f"Macro F1:         {macro_f1:.4f}")
    print(f"Weighted F1:      {weighted_f1:.4f}")
    print("\nPer-class report:\n" + report_text)

    display = ConfusionMatrixDisplay.from_predictions(y_test, y_pred, cmap="Blues", values_format="d")
    display.ax_.set_title("MIT-BIH ECG Heartbeat Classification — Test Split")
    display.figure_.tight_layout()
    display.figure_.savefig(RESULTS_DIR / "ecg_confusion_matrix.png", dpi=180)
    plt.close(display.figure_)
    print(f"\nSaved metrics and confusion matrix in: {RESULTS_DIR}")
    print("Reminder: classical baseline only; no quantum hardware or official Processor A/B results are claimed.")


if __name__ == "__main__":
    main()
