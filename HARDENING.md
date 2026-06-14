<!-- markdownlint-disable -->

# Hardening Report: czl9707--gh-space-shooter/v2.0.0

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `1`

Action **czl9707--gh-space-shooter/v2.0.0** was hardened automatically. 11 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The action uses `actions/setup-python@v5`, which is a mutable tag reference rather than a pinned full 40-character commit SHA. This means the action could silently pull in different (potentially malicious) code if the tag is moved.

Locations:

- `action.yml:44`

### script-injection (severity: high)

Rule (a): Multiple ${{ inputs.* }} expressions are directly interpolated inside run: shell command strings, allowing an attacker-controlled value to inject arbitrary shell commands. In the 'Generate game' step: inputs.username, inputs.output-path, inputs.strategy, and inputs.fps are all interpolated directly into the shell command line (lines 57-61). In the 'Commit and push' step: inputs.output-path, inputs.commit-message, and inputs.no-amend are interpolated directly into shell variable assignments (lines 70-72). All these values should instead be passed via env: variables and referenced as quoted shell variables.

Locations:

- `action.yml:57`
- `action.yml:58`
- `action.yml:59`
- `action.yml:60`
- `action.yml:61`
- `action.yml:70`
- `action.yml:71`
- `action.yml:72`

### github-env-injection (severity: high)

The 'Generate game' step writes an untrusted input value directly to $GITHUB_OUTPUT without sanitization: `echo "output-file=${{ inputs.output-path }}" >> $GITHUB_OUTPUT`. The value of inputs.output-path is attacker-controlled and could contain newline characters that inject additional key=value pairs into GITHUB_OUTPUT. The required sanitization step (printf '%s' "$VAR" | tr -d '\n\r') is missing before the write.

Locations:

- `action.yml:61`

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

Fixed all findings in action.yml: (1) Pinned actions/setup-python@v5 to full commit SHA a26af69be951a213d495a4c3e4e4022e16d87065 with # v5 comment. (2) Moved all ${{ inputs.* }} expressions (username, output-path, strategy, fps, commit-message, no-amend) out of run: shell strings and into env: blocks in both the 'Generate game' and 'Commit and push' steps; referenced them as quoted shell variables. (3) Sanitized the output-path value with printf '%s' | tr -d '\n\r' before writing to $GITHUB_OUTPUT to prevent newline injection.

