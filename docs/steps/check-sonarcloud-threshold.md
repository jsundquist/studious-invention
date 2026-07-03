# Check SonarCloud Threshold

## What happens

The SonarCloud quality gate status for the service is checked automatically. The company quality gate requires:

- No new critical or high severity issues introduced since the last passing gate
- Line coverage must not drop below 80%
- No new security hotspots left unreviewed

If the quality gate is passing, this step completes automatically and the workflow continues.

If the quality gate is failing, **the workflow pauses here** and waits until SonarCloud reports a passing gate. There is nothing to click — the workflow resumes automatically once your code changes result in a passing scan.

## What to do if the threshold is breached

1. Open SonarCloud and review the specific issues blocking the quality gate
2. Fix the issues in your code and push a pull request or commit to `main`
3. SonarCloud will re-scan automatically on push
4. Once the quality gate passes, the platform detects the change and the workflow continues

Common reasons for failure:

- **Coverage dropped** — new code was added without corresponding tests
- **New critical issue** — a code pattern flagged as a critical vulnerability or bug
- **Security hotspot** — new code that requires a security review in SonarCloud before it can be marked safe

## Note

You do not need to take any action in this workflow UI. Fix the code, push it, and the workflow resumes on its own.
