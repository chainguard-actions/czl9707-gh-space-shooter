<!-- markdownlint-disable -->

# Hardening Report: czl9707--gh-space-shooter/v2.0.2

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **czl9707--gh-space-shooter/v2.0.2** was hardened automatically. 11 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): Multiple ${{ inputs.* }} expressions are directly interpolated inside run: shell command strings, allowing an attacker to inject arbitrary shell commands via crafted input values. In the 'Generate game' step: `gh-space-shooter ${{ inputs.username }} --output ${{ inputs.output-path }} --strategy ${{ inputs.strategy }} --fps ${{ inputs.fps }}` and `echo "output-file=${{ inputs.output-path }}" >> $GITHUB_OUTPUT`. In the 'Commit and push' step: `OUTPUT_PATH="${{ inputs.output-path }}"`, `COMMIT_MSG="${{ inputs.commit-message }}"`, and `NO_AMEND="${{ inputs.no-amend }}"`. All inputs should be passed via env: variables and then referenced as quoted shell variables (e.g., "$INPUT_USERNAME") instead of being interpolated directly.

Locations:

- `action.yml:55`
- `action.yml:56`
- `action.yml:57`
- `action.yml:58`
- `action.yml:59`
- `action.yml:66`
- `action.yml:67`
- `action.yml:68`

### github-env-injection (severity: high)

In the 'Generate game' step, the untrusted input value ${{ inputs.output-path }} is written directly to $GITHUB_OUTPUT without sanitization: `echo "output-file=${{ inputs.output-path }}" >> $GITHUB_OUTPUT`. An attacker-controlled value containing newlines could inject arbitrary key=value pairs into the GitHub output environment. The value must be sanitized with `printf '%s' "$VALUE" | tr -d '\n\r'` before being written to $GITHUB_OUTPUT.

Locations:

- `action.yml:59`

### unpinned-uses (severity: high)

The action uses `actions/setup-python@v6` which is pinned to a mutable tag rather than an immutable 40-character commit SHA. A tag can be moved to point to a different (potentially malicious) commit, enabling supply-chain attacks. It should be pinned to a full SHA, e.g., `actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065 # v6`.

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

Fixed all findings in action.yml: (1) Pinned actions/setup-python@v6 to full SHA ece7cb06caefa5fff74198d8649806c4678c61a1. (2) Moved all ${{ inputs.* }} expressions in 'Generate game' step to env: block (INPUT_USERNAME, INPUT_OUTPUT_PATH, INPUT_STRATEGY, INPUT_FPS) and referenced them as quoted shell variables. (3) Sanitized INPUT_OUTPUT_PATH with printf '%s' | tr -d '\n\r' before writing to $GITHUB_OUTPUT to prevent env injection. (4) Moved all ${{ inputs.* }} expressions in 'Commit and push' step to env: block (INPUT_OUTPUT_PATH, INPUT_COMMIT_MSG, INPUT_NO_AMEND) and referenced them as shell variables.

