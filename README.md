# Q1 Biomedical Signal Classifier — QFF Fall Fest 2026, Phase 1

This repository contains a classical ECG classification baseline and preliminary processor-configuration/transpilation comparison work.

## Important status note
- **Processor A** is configured as a 5-qubit linear chain in the current project files.
- **Processor B** is represented as a 7-qubit, heavy-hex-inspired participant-defined model.
- The available participant guideline PDFs did not provide an exact official Processor B coupling map/noise model. Therefore, the Processor B topology in this repository must be labelled as a **participant assumption**, not an official QFF hardware definition.
- The comparison CSV in `results/` contains previously recorded preliminary transpilation results for a small test circuit. It is not a fresh run, a real-hardware result, or evidence that the quantum ECG classifier is complete.

## Repository layout
- `project/processors/` — project scripts and processor JSON configuration files.
- `results/` — generated metrics and preliminary comparison outputs.
- `data/` — dataset notes only. Do not commit the full raw dataset unless its license and project rules permit it.
- `docs/` — additional project notes.

## Setup
Use the Python version and dependency versions that the team has already tested. From the repository root, create/activate a virtual environment and install the dependencies listed in `requirements.txt`.

Windows PowerShell example:
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Re-run and verify before submission
Run commands from the repository root:
```powershell
python .\project\processors\check_processors.py
python .\project\processors\compare_processors.py
python .\project\processors\main_real_ecg.py
```

Check the scripts' output paths before running. Use newly generated outputs as the submitted results; do not treat preliminary values as a replacement for rerunning the code.

## Dataset
The project uses the MIT-BIH heartbeat dataset downloaded from Kaggle:
https://www.kaggle.com/datasets/shayanfazeli/heartbeat

Record the exact dataset version, source, and license/usage terms that the team verified. This note does not claim that the dataset license has been independently verified.

## Before handing in
- [ ] Confirm the official challenge requirements and required deliverables.
- [ ] Run the validation, comparison, and ECG baseline scripts successfully.
- [ ] Confirm output files correspond to the latest run.
- [ ] Keep Processor B marked as a participant assumption unless organizers provide the official definition.
- [ ] Check `.gitignore` and avoid uploading virtual environments, secrets, or unapproved raw data.
- [ ] Ensure `requirements.txt` matches the packages actually imported by the team's scripts.
