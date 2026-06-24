<!-- markdownlint-disable -->

# Hardening Report: czl9707--gh-space-shooter/v2.0.3

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `1`

Action **czl9707--gh-space-shooter/v2.0.3** was hardened automatically. 12 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): Multiple `${{ inputs.* }}` expressions are directly interpolated into the 'Generate game' run: shell script without going through env: variables. This allows an attacker-controlled input to inject arbitrary shell commands. Offending lines: `gh-space-shooter ${{ inputs.username }} \`, `--output ${{ inputs.output-path }} \`, `--strategy ${{ inputs.strategy }} \`, `--fps ${{ inputs.fps }}`, and `echo "output-file=${{ inputs.output-path }}" >> $GITHUB_OUTPUT`.

Locations:

- `action.yml:57`

### script-injection (severity: high)

Rule (a): Multiple `${{ inputs.* }}` expressions are directly interpolated into the 'Commit and push' run: shell script. Specifically: `OUTPUT_PATH="${{ inputs.output-path }}"`, `COMMIT_MSG="${{ inputs.commit-message }}"`, and `NO_AMEND="${{ inputs.no-amend }}"`. Even though the values are assigned to shell variables, the interpolation happens before the shell processes the script, allowing injection of shell metacharacters.

Locations:

- `action.yml:70`

### github-env-injection (severity: high)

The 'Generate game' step writes `${{ inputs.output-path }}` directly to `$GITHUB_OUTPUT` without sanitization: `echo "output-file=${{ inputs.output-path }}" >> $GITHUB_OUTPUT`. An attacker-controlled input containing newlines could inject arbitrary environment variables or output values. The required sanitization (`printf '%s' ... | tr -d '\n\r'`) is absent.

Locations:

- `action.yml:61`

### unpinned-uses (severity: high)

The action uses `actions/setup-python@v6`, which is a mutable tag reference rather than a pinned full 40-character commit SHA. This is vulnerable to supply-chain attacks if the tag is moved to point to a different (potentially malicious) commit.

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

**Fixes applied:** unpinned-uses, script-injection, static-inline-injection, github-env-injection

**Notes:**

1. Pinned actions/setup-python@v6 to full SHA ece7cb06caefa5fff74198d8649806c4678c61a1. 2. Moved all ${{ inputs.* }} expressions (username, output-path, strategy, fps) in the 'Generate game' step to an env: block as INPUT_USERNAME, INPUT_OUTPUT_PATH, INPUT_STRATEGY, INPUT_FPS, and referenced them as shell variables. 3. Moved all ${{ inputs.* }} expressions (output-path, commit-message, no-amend) in the 'Commit and push' step to an env: block as OUTPUT_PATH, COMMIT_MSG, NO_AMEND, removing the inline interpolation. 4. Sanitized the output-path value before writing to $GITHUB_OUTPUT using printf '%s' | tr -d '\n\r' to prevent newline injection.

