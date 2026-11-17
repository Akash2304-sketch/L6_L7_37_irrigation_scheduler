# Lab 7 Report — Fuzzing for Input Validation Bugs

**Project:** L6_L7_37 — Irrigation Scheduler  
**Technique:** Property-based fuzz testing with Hypothesis  
**Functions tested:** `parse_zone`, `moisture_average`, `water_needed`

## 1. Objective

Use Hypothesis to generate unexpected and malformed inputs, identify input
validation weaknesses, and harden the three irrigation-scheduler functions.

## 2. Initial defects in the supplied implementation

- `parse_zone` unpacked the result of `split(':')` without checking the
  separator count, accepted blank names and did not validate finite positive
  areas.
- `moisture_average` did not reject empty input or empty CSV fields, did not
  constrain readings to the 0–100 range, and could divide by zero.
- `water_needed` unpacked `split('|')` without validating the delimiter,
  accepted non-finite values, and did not reject non-positive area or negative
  rainfall.
- The original interactive entry point allowed malformed input exceptions to
  terminate the program.

## 3. Fuzz-test design

The updated test suite uses `@given` with arbitrary text and `None` for each
function. A documented invalid input may raise `ValueError`; any other
unexpected exception fails the test. Additional generated valid-input tests
check output invariants and calculation correctness.

## 4. Fixes implemented

- Added type, empty-string, separator-count, numeric and finite-number checks.
- Enforced positive plot/zone area, non-negative rainfall, and soil moisture
  readings in the inclusive range 0–100.
- Kept the original calculation behaviour: integer-floor moisture average and
  `max(area * 5 - rainfall, 0)` water requirement.
- Added user-friendly error handling in the interactive application.

## 5. Execution evidence

The lab handout requires four terminal screenshots. Capture them from your own
terminal after installing dependencies. Do not use illustrative output as
evidence of a real test run.

### Screenshot 1 — Original buggy application

Run the original version before applying the fix, for example with malformed
inputs such as `north`, an empty moisture CSV, and `10|1|2`. Capture the
terminal output and the exception.

### Screenshot 2 — Fuzz tests against original code

Run:

```bash
python -m pytest -v test_irrigation_scheduler.py
```

Capture the failing output while the original implementation is in place.
Hypothesis should report a minimized failing example.

### Screenshot 3 — Fixed application

Run:

```bash
python irrigation_scheduler.py
```

Enter valid sample inputs such as `north:120`, `40,35,50`, and `120|8`.
Capture the successful output.

### Screenshot 4 — Fuzz tests against fixed code

Run:

```bash
python -m pytest -v test_irrigation_scheduler.py
```

Capture the passing test summary.

## 6. Result

The fixed implementation explicitly validates all three input formats and
rejects malformed values with `ValueError`. The property-based tests check
both arbitrary inputs and generated valid inputs. Attach the four genuine
terminal screenshots above to this report before submission.
