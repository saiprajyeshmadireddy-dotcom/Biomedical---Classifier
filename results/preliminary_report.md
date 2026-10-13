# Preliminary Results and Limitations

## Processor configuration
- **Processor A:** 5 qubits; linear-chain edges `(0,1), (1,2), (2,3), (3,4)`.
- **Processor B:** 7 qubits; participant-defined edges `(0,1), (1,2), (2,3), (3,4), (4,5), (5,6), (1,4)`.
- Both configurations use the listed basis gates `rz`, `sx`, `x`, `cx` in the currently described setup.
- **Important:** The available guideline PDFs did not provide an exact official Processor B coupling map/noise model. The Processor B connectivity is a participant assumption and must not be presented as official.

## Preliminary transpilation comparison
Previously recorded for a small 5-qubit test circuit using `optimization_level=0` and `seed_transpiler=42`, with listed edges treated as bidirectional:

| Metric | Processor A | Processor B |
|---|---:|---:|
| Configured qubits | 5 | 7 |
| Logical circuit qubits | 5 | 5 |
| Circuit depth | 12 | 5 |
| Total operations | 18 | 9 |
| CX count | 15 | 6 |
| SWAP count | 0 | 0 |
| RZ count | 2 | 2 |
| SX count | 1 | 1 |

These are **preliminary recorded results**, not freshly reproduced in this package. They describe transpilation of a small test circuit, not a quantum ECG classifier benchmark and not execution on physical quantum hardware. Re-run `compare_processors.py` and replace the table/CSV with current outputs before submission.

## Classical ECG baseline (previously recorded)
- Accuracy: `0.6729`
- Macro precision: `0.4426`
- Macro recall: `0.7629`
- Macro F1: `0.4775`
- Weighted F1: `0.7365`

The previous run reportedly used `LogisticRegression` with `StandardScaler`, `class_weight="balanced"`, and `max_iter=300`; an `lbfgs` convergence warning occurred. These values are included for continuity only. Re-run the ECG script and confirm the latest metrics and confusion matrix before submission. This is a **classical baseline**, not quantum-classifier performance.

## Reproducibility checklist
1. Run `check_processors.py`.
2. Run `compare_processors.py` and check the output CSV.
3. Run `main_real_ecg.py` and check the metrics JSON and confusion matrix.
4. Record Python and package versions used.
5. Confirm the exact challenge-required metrics and deliverables with the organizer's instructions.
