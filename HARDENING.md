<!-- markdownlint-disable -->

# Hardening Report: czl9707--gh-space-shooter/v2.0.3

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **czl9707--gh-space-shooter/v2.0.3** was hardened automatically. 12 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

The 'Generate game' step (rule a) directly interpolates multiple untrusted inputs into the run: shell command without going through env: variables: `gh-space-shooter ${{ inputs.username }} --output ${{ inputs.output-path }} --strategy ${{ inputs.strategy }} --fps ${{ inputs.fps }}`. An attacker-controlled value for any of these inputs (e.g. inputs.username containing shell metacharacters) can execute arbitrary commands. Additionally, `echo "output-file=${{ inputs.output-path }}" >> $GITHUB_OUTPUT` also interpolates an input directly into the shell.

Locations:

- `action.yml:57`
- `action.yml:58`
- `action.yml:59`
- `action.yml:60`
- `action.yml:62`

### script-injection (severity: high)

The 'Commit and push' step (rule a) directly interpolates untrusted inputs into the run: shell command: `OUTPUT_PATH="${{ inputs.output-path }}"`, `COMMIT_MSG="${{ inputs.commit-message }}"`, and `NO_AMEND="${{ inputs.no-amend }}"`. Even though the values are assigned to shell variables, the interpolation happens before the shell processes the script, so an attacker-controlled input containing shell metacharacters or newlines can break out of the quoted string and execute arbitrary commands.

Locations:

- `action.yml:68`
- `action.yml:69`
- `action.yml:70`

### github-env-injection (severity: high)

The 'Generate game' step writes the untrusted input `${{ inputs.output-path }}` directly to $GITHUB_OUTPUT without sanitization: `echo "output-file=${{ inputs.output-path }}" >> $GITHUB_OUTPUT`. A value containing newlines could inject additional key=value pairs into GITHUB_OUTPUT, potentially overwriting other outputs. The required sanitization step (`printf '%s' "$VAR" | tr -d '\n\r'`) is absent.

Locations:

- `action.yml:62`

### unpinned-uses (severity: high)

The action uses `actions/setup-python@v6`, which is pinned to a mutable tag (`v6`) rather than an immutable 40-character commit SHA. If the tag is moved (e.g. by a supply-chain compromise of the upstream action), the action will silently execute different code. It should be pinned to a full SHA, e.g. `actions/setup-python@<40-char-sha> # v6`.

Locations:

- `action.yml:46`

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
1. Pinned actions/setup-python@v6 to full SHA ece7cb06caefa5fff74198d8649806c4678c61a1
2. In 'Generate game' step: moved inputs.username, inputs.output-path, inputs.strategy, inputs.fps to env: block as INPUT_USERNAME, INPUT_OUTPUT_PATH, INPUT_STRATEGY, INPUT_FPS; referenced as shell variables with double-quoting
3. Sanitized INPUT_OUTPUT_PATH with 'printf | tr -d \n\r' before writing to GITHUB_OUTPUT to prevent env injection
4. In 'Commit and push' step: moved inputs.output-path, inputs.commit-message, inputs.no-amend to env: block as INPUT_OUTPUT_PATH, INPUT_COMMIT_MSG, INPUT_NO_AMEND; referenced as shell variables

