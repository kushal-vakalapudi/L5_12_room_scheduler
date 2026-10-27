# Lab 5 Baseline Findings

Baseline findings below were recorded from the original, unmodified
`scheduler_system.py` and the baseline Pylint, Bandit, and Flake8 reports.
Line numbers refer to that original source and remain historical references
after fixes. The first-group fixes and their verification results are noted in
the corresponding rows. Runtime observations are identified separately from
static-analysis findings.

| Issue ID | Source/tool | Severity or category | Original line number | Finding | Why it matters | Planned fix | Verification method |
|---|---|---|---:|---|---|---|---|
| B-01 | Bandit B605; runtime observation | High (Bandit); Windows compatibility | 43 | **Baseline:** `os.system("cat " + file)` starts a shell command using a concatenated filename. Bandit reported B605; at runtime on Windows, `cat` was not recognized. **Fixed:** the log is now displayed using Python file I/O; no shell is invoked. | A shell command can expose command-injection risk if the filename is influenced by untrusted input, and the command failed on this Windows system. | **Completed:** replaced shell execution with context-managed Python file reads/writes. Expected filesystem `OSError`s are reported to stderr by exception type without printing the path. | **Verified:** Bandit on current source: no issues identified (exit 0). Scheduler/logging test displayed conflict content with no shell error. Missing log parent reported `FileNotFoundError` without a traceback or path. |
| B-02 | Bandit B110; Pylint W0702; Flake8 E722 | Low (Bandit); exception handling | 23-28 (reported at line 27) | **Baseline:** `cancel_reservation` caught every exception with a bare `except` and silently passed. **Fixed:** a missing reservation is now reported explicitly; unrelated errors are not caught. | Unrelated programming and data errors were hidden, making failures difficult to diagnose; the expected missing-reservation case was not distinguished from other errors. | **Completed:** look up the reservation first, report and return only when it is absent, then perform normal equipment restoration and deletion. | **Verified:** Bandit on current source: no issues identified (exit 0); current-source search found no bare `except`. Runtime test confirmed successful cancellation restores equipment and missing reservation prints a message. |
| F-01 | Runtime observation; source inspection | Functional bug (not assigned a tool severity) | 30-32, 48, 50 | **Baseline:** `"14-12"` produced `-2` because `slot_hours` subtracted the start hour from the end hour without validating the order. **Fixed:** the demo uses `"12-14"` and slot parsing rejects malformed, out-of-range, equal, and reversed same-day intervals. | Negative or zero durations are not valid same-day reservations; accepting them could create invalid bookings. | **Completed:** validate the interval in `slot_hours` and before any reservation/equipment mutation in `schedule_room`; explicitly reject overnight slots. | **Verified:** `09-11` returns 2, `0-23` returns 23; equal, reversed, malformed, and out-of-range slots raise `ValueError`; invalid booking leaves state unchanged. Normal demo displays duration 2. |
| F-06 | Manual functional review; not tool-reported | Booking state integrity | 16-18 | **Baseline:** equipment was decremented item-by-item before a reservation was created. If a later requested item was unknown or unavailable, an exception could leave earlier inventory decremented without a booking. **Fixed:** validate the requested equipment set and availability before changing inventory. | Failed booking attempts must not leave the shared equipment pool in a partially updated state. | **Completed:** count requested items, reject unknown or insufficient inventory with `ValueError`, and only then decrement inventory and create the reservation. | **Verified:** tested a mixed known/unknown equipment request and an over-capacity request; both were rejected and reservation, conflict, and equipment state remained unchanged. |
| P-01 | Pylint W0102 | Mutable default argument | 11 | `schedule_room` used `equipment_list=[]` as a default argument. | Mutable defaults are shared between calls; later changes could unexpectedly affect other reservations. | **Completed:** default to `None` and create a new list for each call. | Current Pylint score is 10.00/10; the reservation/conflict tests passed. |
| P-02 | Pylint W0603 | Global state | 12 | `schedule_room` used `global next_reservation`. | Global mutation couples the function to module state and makes behavior harder to test and reason about. | **Completed:** use an `itertools.count` iterator for unique IDs without a `global` statement. | Current Pylint score is 10.00/10; distinct reservation IDs were verified. |
| P-03 | Pylint C0103 | Naming | 9 | Pylint flagged `next_reservation` for not following its expected UPPER_CASE naming for a constant. | The name/style did not clearly communicate the mutable counter's role. | **Completed:** replace the integer with `reservation_ids`, an iterator. | Current Pylint score is 10.00/10. |
| P-04 | Pylint C0206 | Dictionary iteration | 13 | The loop iterated over `reservations` keys and then indexed `reservations[r]`. | This is less direct and readable than iterating over dictionary entries. | **Completed:** iterate over `reservations.values()`. | Current Pylint score is 10.00/10; conflicting reservations were detected in testing. |
| P-05 | Pylint C0209 | String formatting | 15 | The conflict message used `%` formatting where Pylint recommends an f-string. | The formatting style is less readable. | **Completed:** format the message with an f-string. | Current Pylint score is 10.00/10; conflict message output was verified. |
| P-06 | Pylint W1514, R1732 | File handling and encoding | 35, 40 | The original `export_schedule` and `logConflicts` calls used `open` without explicit encoding or a context manager. | Default encodings can vary by system, and files may not be closed reliably if an exception occurs. | **Completed:** both file operations use context managers and UTF-8 encoding. | Current Pylint score is 10.00/10; end-to-end execution wrote and read schedule/log files in a temporary directory. |
| P-07 | Pylint C0103 | Naming | 39 | Pylint reported `logConflicts` as not following snake_case function naming. | Inconsistent naming makes the function harder to read and use consistently. | **Completed:** renamed it to `log_conflicts` and updated its call site. | Current Pylint score is 10.00/10; normal execution called the renamed function. |
| P-08 | Pylint C0114 | Missing documentation | 1 | The module had no module docstring. | The module's purpose and behavior were not documented at its entry point. | **Completed:** added a module docstring. | Current Pylint score is 10.00/10. |
| P-09 | Pylint C0116 | Missing documentation | 11, 22, 30, 34, 39, 45 | The original functions lacked docstrings. | Function purposes and expected inputs/behavior were less clear to maintainers. | **Completed:** added concise docstrings to the current public functions and `main`. | Current Pylint score is 10.00/10. |
| F-02 | Flake8 E302 | Formatting: blank lines | 11, 22, 30, 34, 39, 45 | Flake8 expected two blank lines before top-level function definitions but found one. | The file did not follow the expected top-level spacing convention. | **Completed:** formatted function definitions with the required spacing. | Current Flake8 run reports zero diagnostics. |
| F-03 | Flake8 E501; Pylint C0301 | Formatting: long lines | 14, 18 | Flake8 reported lines 14 (87 characters) and 18 (102 characters) over its 79-character limit; Pylint also flagged line 18 (102/100). | Long lines reduce readability and fail the configured style checks. | **Completed:** wrapped conditions, reservation data, and output formatting. | Current Pylint run reports 10.00/10; current Flake8 run reports zero diagnostics. |
| F-04 | Flake8 F841; Pylint W0612 | Unused local variables | 46, 47, 49 | `a`, `a_more`, and `c` were assigned but never used. Both tools reported the unused assignments. | Dead assignments add noise and can obscure which booking results matter. | **Completed:** removed unused assignments and the invalid integer slot example. | Current Pylint run reports 10.00/10; current Flake8 run reports zero diagnostics; normal execution passed. |
| F-05 | Flake8 E305 | Formatting: blank lines | 59 | Flake8 expected two blank lines after the `main` function definition but found one before the module-level call. | The module did not follow the expected spacing convention after a top-level function. | **Completed:** use a standard `if __name__ == "__main__":` entry point with correct spacing. | Current Flake8 run reports zero diagnostics; normal execution passed. |
## Fix order

1. **Completed:** addressed the High-severity Bandit B605 shell execution
   finding with Python file I/O; Bandit and runtime checks passed.
2. **Completed:** removed silent exception suppression in reservation
   cancellation; missing reservations are reported and unrelated exceptions
   are not caught.
3. **Completed:** fixed the negative duration at its source, validated
   same-day time ranges, and rejected zero-duration, reversed, malformed, and
   out-of-range intervals.
4. **Completed:** fixed the mutable default, reservation ID state, file
   handling, naming, documentation, and remaining Pylint findings.
5. **Completed:** resolved the baseline Flake8 findings and verified the
   scheduler plus all three analysis tools. Final after-analysis reports are
   saved as `pylint_report_after.txt`, `bandit_report_after.txt`, and
   `flake8_report_after.txt`.

## Current implementation and verification

Current source references (these are separate from the historical baseline
line numbers in the table):

- `schedule_room`: `scheduler_system.py:15`; validates the slot at line 17,
  checks requested equipment before mutation at lines 21-26, detects
  conflicts at lines 28-33, and assigns unique IDs at line 38.
- `cancel_reservation`: `scheduler_system.py:47`; explicitly reports a
  missing reservation at lines 49-52.
- `slot_hours`: `scheduler_system.py:59`; validates hour syntax and bounds at
  lines 61-67 and rejects equal/reversed intervals at lines 68-70.
- `export_schedule`: `scheduler_system.py:73`; uses a UTF-8 context manager.
- `log_conflicts`: `scheduler_system.py:79`; uses Python file I/O and reports
  expected filesystem errors at lines 87-91.
- `main`: `scheduler_system.py:94`; uses a valid demo interval and handles an
  invalid user-entered interval.

Final after-analysis results on the current source, saved in the listed files:

- Pylint: **10.00/10**, `pylint_report_after.txt`.
- Flake8: **0 diagnostics**, `flake8_report_after.txt`.
- Bandit: **0 findings**, `bandit_report_after.txt`.
- The original `*_before.txt` reports were not modified.

Executed verification:

- Python syntax compilation with Python's `compile()` built-in: passed.
- Pylint, Flake8, and Bandit on the current source: passed with the results
  above.
- Targeted slot tests: valid intervals returned expected positive durations;
  equal, reversed, malformed, and out-of-range intervals were rejected.
- Invalid booking test: rejection did not mutate reservations or equipment.
- Reservation tests: conflict detection, distinct IDs, cancellation, equipment
  restoration, and missing-reservation handling passed.
- Equipment allocation tests: unknown equipment and requests exceeding
  inventory were rejected without changing reservation, conflict, or equipment
  state.
- End-to-end normal run in a temporary directory: exited successfully, printed
  a duration of 2, and wrote the expected schedule and conflict log.
- End-to-end reversed user-input run: reported the invalid slot and exited
  cleanly without creating that booking.
- `git diff --check`: passed.

No source or documentation findings from the baseline reports remain
outstanding in the current Pylint, Flake8, or Bandit runs. Final after-analysis
reports are complete, and the Lab 5 deliverables have been committed.

The **original baseline** Bandit report contained one High and one Low finding,
with no Medium finding. The current Bandit run reports no findings. No severity
is assigned here to the runtime observation or to style/quality diagnostics
unless a tool explicitly reports one.
