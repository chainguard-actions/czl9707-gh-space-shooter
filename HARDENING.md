<!-- markdownlint-disable -->

# Hardening Report: czl9707--gh-space-shooter/v2.0.2

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `1`

Action **czl9707--gh-space-shooter/v2.0.2** was hardened automatically. 12 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Sub-rule (a): The 'Generate game' step directly interpolates attacker-controlled inputs inside the run: shell command string. Specifically: `gh-space-shooter ${{ inputs.username }} --output ${{ inputs.output-path }} --strategy ${{ inputs.strategy }} --fps ${{ inputs.fps }}`. Any of these inputs can contain shell metacharacters (`;`, `|`, `&`, `$(...)`, etc.) that will be executed by the shell before any quoting takes effect, enabling command injection.

Locations:

- `action.yml:50`

### github-env-injection (severity: high)

The 'Generate game' step writes `${{ inputs.output-path }}` directly to $GITHUB_OUTPUT without sanitization: `echo "output-file=${{ inputs.output-path }}" >> $GITHUB_OUTPUT`. The value is not passed through `printf '%s' ... | tr -d '\n\r'` before the write, allowing newline injection that could set arbitrary output variables.

Locations:

- `action.yml:55`

### script-injection (severity: high)

Sub-rule (a): The 'Commit and push' step directly interpolates attacker-controlled inputs inside the run: shell command string: `OUTPUT_PATH="${{ inputs.output-path }}"`, `COMMIT_MSG="${{ inputs.commit-message }}"`, and `NO_AMEND="${{ inputs.no-amend }}"`. Even though the shell variables are later used with double-quotes, the ${{ }} expressions are substituted by the YAML template engine before the shell sees them, so an attacker can break out of the double-quoted string and inject arbitrary shell commands.

Locations:

- `action.yml:62`

### unpinned-uses (severity: high)

The action uses `actions/setup-python@v6`, which is pinned to a mutable version tag rather than an immutable 40-character commit SHA. A compromised or altered tag could introduce malicious code. It should be pinned to a full SHA, e.g. `actions/setup-python@<40-char-sha> # v6`.

Locations:

- `action.yml:44`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.username }}" appears directly in run: block of step "Generate game"; move to env: map

Locations:

- `action.yml:63`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.output-path }}" appears directly in run: block of step "Generate game"; move to env: map

Locations:

- `action.yml:64`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.strategy }}" appears directly in run: block of step "Generate game"; move to env: map

Locations:

- `action.yml:65`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.fps }}" appears directly in run: block of step "Generate game"; move to env: map

Locations:

- `action.yml:66`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.output-path }}" appears directly in run: block of step "Generate game"; move to env: map

Locations:

- `action.yml:67`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.output-path }}" appears directly in run: block of step "Commit and push"; move to env: map

Locations:

- `action.yml:75`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.commit-message }}" appears directly in run: block of step "Commit and push"; move to env: map

Locations:

- `action.yml:76`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.no-amend }}" appears directly in run: block of step "Commit and push"; move to env: map

Locations:

- `action.yml:77`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, github-env-injection, static-inline-injection

**Notes:**

Fixed all 12 findings in action.yml:
1. Pinned actions/setup-python@v6 to full SHA a309ff8b426b58ec0e2a45f0f869d46889d02405.
2. Moved all ${{ inputs.* }} expressions in the 'Generate game' step (username, output-path, strategy, fps) to an env: block as INPUT_USERNAME, INPUT_OUTPUT_PATH, INPUT_STRATEGY, INPUT_FPS; updated run: to use double-quoted env vars.
3. Sanitized output-path before writing to $GITHUB_OUTPUT using printf '%s' ... | tr -d '\n\r'.
4. Moved all ${{ inputs.* }} expressions in the 'Commit and push' step (output-path, commit-message, no-amend) to an env: block as OUTPUT_PATH, COMMIT_MSG, NO_AMEND; removed inline template expressions from the run: shell script.

