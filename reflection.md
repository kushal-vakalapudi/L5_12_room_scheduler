# Lab 5 Reflection

## 1. What static code analysis is and why it is useful

Static code analysis checks source code without running the application. It
helps find likely bugs, risky patterns, and maintainability or style problems
early, before they become harder to reproduce. It complements runtime tests:
the tools identify suspicious code, while tests verify the program's actual
behavior.

## 2. What Pylint, Bandit, and Flake8 detected

The original Pylint report rated the source **5.60/10**. It identified issues
including a mutable default argument, global state, a bare exception handler,
unmanaged file handles and unspecified encodings, naming and documentation
problems, long lines, and unused variables.

The original Bandit report found a **High** B605 shell-execution issue in the
conflict logger and a **Low** B110 issue for silently catching and suppressing
all exceptions.

The original Flake8 report contained **13 diagnostics**, covering top-level
spacing, long lines, a bare exception, and unused variables. After the fixes,
all three tools were rerun: Pylint rated the source **10.00/10**, Bandit
reported **no findings**, and Flake8 reported **zero diagnostics**. The
original baseline reports were kept separate from the final after-analysis
reports.

## 3. The most important fixes and why

Replacing `os.system("cat " + file)` with Python file I/O removed shell
execution, addressed Bandit's High finding, and made conflict-log display work
on Windows. Replacing the bare `except` with explicit handling for a missing
reservation stopped unexpected errors from being hidden.

The scheduler now validates same-day start and end hours, rejects equal or
reversed ranges, and validates before creating a booking. It also checks
requested equipment availability before changing inventory, so a failed
booking does not partially allocate equipment. These changes address observed
runtime errors and protect scheduler state.

## 4. What I learned

Code quality includes more than passing a linter. Clear names, documentation,
consistent formatting, and context-managed file operations improve
maintainability. Security analysis can identify risky patterns even in a small
program, and platform-specific behavior matters: a shell command available on
one system may fail on another.

Tests are necessary alongside static analysis. I verified valid and invalid
time ranges, booking conflicts, failed-booking state preservation,
cancellation and equipment restoration, missing reservations, and normal
scheduler execution in temporary directories. The final analyzer results
confirm the reported diagnostics were addressed; the baseline reports retain
the evidence of what the tools originally found.
