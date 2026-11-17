# L6_L7_37 — Irrigation Scheduler

## Lab 7: Fuzzing for Input Validation Bugs

This folder contains the original irrigation-scheduler exercise, hardened input
validation, and Hypothesis property-based tests.

### Files

| File | Purpose |
|---|---|
| `irrigation_scheduler.py` | Hardened functions and interactive demo |
| `test_irrigation_scheduler.py` | Hypothesis fuzz and property tests |
| `requirements.txt` | Test dependencies |
| `LAB7_REPORT.md` | Report notes and commands for the required evidence |

### Setup and run (Python 3.8+)

From this folder:

```bash
python -m pip install -r requirements.txt
python irrigation_scheduler.py
python -m pytest -v test_irrigation_scheduler.py
```

Invalid inputs raise `ValueError` from the functions. The interactive program
catches validation errors and continues to the next input prompt.

See `LAB7_REPORT.md` for the test properties and evidence checklist.
