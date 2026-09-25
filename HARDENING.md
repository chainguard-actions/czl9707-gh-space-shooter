<!-- markdownlint-disable -->

# Hardening Report: czl9707--gh-space-shooter/v2.0.0

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **czl9707--gh-space-shooter/v2.0.0** was hardened automatically. 11 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The action uses `actions/setup-python@v5`, which is a mutable tag reference rather than a pinned 40-character commit SHA. A tag can be moved to point to a different (potentially malicious) commit, enabling supply-chain attacks.

Locations:

- `action.yml:44`

### script-injection (severity: high)

Sub-rule (a): Multiple `${{ inputs.* }}` expressions are interpolated directly inside `run:` shell command strings before the shell processes them, allowing an attacker to inject arbitrary shell commands via crafted input values.

In the 'Generate game' step (around line 51):
  - `gh-space-shooter ${{ inputs.username }} \`
  - `--output ${{ inputs.output-path }} \`
  - `--strategy ${{ inputs.strategy }} \`
  - `--fps ${{ inputs.fps }}`
  - `echo "output-file=${{ inputs.output-path }}" >> $GITHUB_OUTPUT`

In the 'Commit and push' step (around line 60):
  - `OUTPUT_PATH="${{ inputs.output-path }}"`
  - `COMMIT_MSG="${{ inputs.commit-message }}"`
  - `NO_AMEND="${{ inputs.no-amend }}"`

All these should be moved to `env:` variables and referenced as `"$VAR"` in the shell script.

Locations:

- `action.yml:51`
- `action.yml:60`

### github-env-injection (severity: high)

The 'Generate game' step writes `${{ inputs.output-path }}` directly to `$GITHUB_OUTPUT` without sanitization: `echo "output-file=${{ inputs.output-path }}" >> $GITHUB_OUTPUT`. An attacker can supply a value containing newlines to inject arbitrary key=value pairs into the GitHub output context. The required sanitization step (`printf '%s' "$VAR" | tr -d '\n\r'`) is missing before the write.

Locations:

- `action.yml:55`

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

Fixed all findings in hardened/action/action.yml:
1. Pinned actions/setup-python@v5 to full SHA a26af69be951a213d495a4c3e4e4022e16d87065 (# v5 comment preserved).
2. Moved all ${{ inputs.* }} expressions out of run: blocks into env: maps for both 'Generate game' (INPUT_USERNAME, INPUT_OUTPUT_PATH, INPUT_STRATEGY, INPUT_FPS) and 'Commit and push' (INPUT_OUTPUT_PATH, INPUT_COMMIT_MSG, INPUT_NO_AMEND) steps; referenced as shell variables in the scripts.
3. Sanitized the output-path value before writing to $GITHUB_OUTPUT using `printf '%s' "$INPUT_OUTPUT_PATH" | tr -d '\n\r'` to prevent newline injection.

