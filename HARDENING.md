<!-- markdownlint-disable -->

# Hardening Report: czl9707--gh-space-shooter/v2.0.5

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **czl9707--gh-space-shooter/v2.0.5** was hardened automatically. 11 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Rule (a): Multiple ${{ inputs.* }} expressions are directly interpolated inside run: shell command strings, allowing an attacker to inject arbitrary shell commands via user-controlled inputs.

In the 'Generate game' step (line ~44): `gh-space-shooter ${{ inputs.username }} --output ${{ inputs.output-path }} --strategy ${{ inputs.strategy }} --fps ${{ inputs.fps }}` — all four inputs are interpolated directly into the shell command.

In the 'Commit and push' step (line ~53): `OUTPUT_PATH="${{ inputs.output-path }}"`, `COMMIT_MSG="${{ inputs.commit-message }}"`, and `NO_AMEND="${{ inputs.no-amend }}"` — inputs are interpolated directly into shell variable assignments. An attacker controlling these inputs (e.g. via workflow_dispatch or a calling workflow) can break out of the quoted context and execute arbitrary commands.

Locations:

- `action.yml:44`
- `action.yml:53`

### github-env-injection (severity: high)

The 'Generate game' step writes the value of ${{ inputs.output-path }} directly to $GITHUB_OUTPUT without sanitization (no `printf '%s' ... | tr -d '\n\r'` step). An attacker-controlled input containing newlines could inject additional key=value pairs into the GitHub output environment file, potentially overwriting other outputs or causing unexpected behavior.

Offending line: `echo "output-file=${{ inputs.output-path }}" >> $GITHUB_OUTPUT`

Locations:

- `action.yml:49`

### unpinned-uses (severity: high)

The action uses `actions/setup-python@v6` which is pinned to a mutable tag (`v6`) rather than an immutable 40-character commit SHA. If the tag is moved (e.g. by a supply-chain compromise of the upstream repository), the action would silently execute different code. It should be pinned to a full SHA, e.g. `actions/setup-python@<40-char-sha> # v6`.

Locations:

- `action.yml:37`

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

Fixed all findings in action.yml:
1. Pinned actions/setup-python@v6 to full SHA ece7cb06caefa5fff74198d8649806c4678c61a1 (keeping # v6 comment).
2. Moved all ${{ inputs.* }} expressions in 'Generate game' step (username, output-path, strategy, fps) to env: block as INPUT_USERNAME, INPUT_OUTPUT_PATH, INPUT_STRATEGY, INPUT_FPS; referenced as double-quoted shell variables.
3. Moved all ${{ inputs.* }} expressions in 'Commit and push' step (output-path, commit-message, no-amend) to env: block as INPUT_OUTPUT_PATH, INPUT_COMMIT_MSG, INPUT_NO_AMEND; referenced as shell variables.
4. Sanitized output-path before writing to $GITHUB_OUTPUT using `printf '%s' "$INPUT_OUTPUT_PATH" | tr -d '\n\r'` to prevent newline injection.

