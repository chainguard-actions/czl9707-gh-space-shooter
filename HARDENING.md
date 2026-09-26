<!-- markdownlint-disable -->

# Hardening Report: czl9707--gh-space-shooter/v2.0.4

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **czl9707--gh-space-shooter/v2.0.4** was hardened automatically. 11 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The action uses `actions/setup-python@v6`, which is pinned to a mutable version tag rather than a full 40-character commit SHA. This means the action could be silently updated to a different (potentially malicious) version without any change to this file.

Locations:

- `action.yml:44`

### script-injection (severity: high)

Multiple `${{ inputs.* }}` expressions are interpolated directly inside `run:` shell command strings, violating sub-rule (a). In the 'Generate game' step, `${{ inputs.username }}`, `${{ inputs.output-path }}`, `${{ inputs.strategy }}`, and `${{ inputs.fps }}` are embedded directly in the shell command line — an attacker-controlled value containing shell metacharacters (`;`, `|`, `$(...)`, etc.) would be executed by the shell. In the 'Commit and push' step, `${{ inputs.output-path }}`, `${{ inputs.commit-message }}`, and `${{ inputs.no-amend }}` are interpolated directly into shell variable assignments. All of these must be moved to `env:` blocks and then referenced as double-quoted shell variables (e.g., `"$INPUT_USERNAME"`).

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

In the 'Generate game' step, the value `${{ inputs.output-path }}` is written directly to `$GITHUB_OUTPUT` without sanitization: `echo "output-file=${{ inputs.output-path }}" >> $GITHUB_OUTPUT`. An attacker-controlled input containing newline characters could inject arbitrary key-value pairs into the GitHub output environment. The value must be sanitized with `printf '%s' "$VALUE" | tr -d '\n\r'` before being written to `$GITHUB_OUTPUT`.

Locations:

- `action.yml:59`

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
1. Pinned actions/setup-python@v6 to full SHA ece7cb06caefa5fff74198d8649806c4678c61a1 (# v6 comment preserved).
2. In 'Generate game' step: moved ${{ inputs.username }}, ${{ inputs.output-path }}, ${{ inputs.strategy }}, ${{ inputs.fps }} to env: block as INPUT_USERNAME, INPUT_OUTPUT_PATH, INPUT_STRATEGY, INPUT_FPS; referenced as double-quoted shell variables.
3. In 'Generate game' step: sanitized INPUT_OUTPUT_PATH with `printf '%s' "$INPUT_OUTPUT_PATH" | tr -d '\n\r'` before writing to $GITHUB_OUTPUT.
4. In 'Commit and push' step: moved ${{ inputs.output-path }}, ${{ inputs.commit-message }}, ${{ inputs.no-amend }} to env: block as INPUT_OUTPUT_PATH, INPUT_COMMIT_MESSAGE, INPUT_NO_AMEND; referenced as shell variables.

