<!-- markdownlint-disable -->

# Hardening Report: czl9707--gh-space-shooter/v1.0.3

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `1`

Action **czl9707--gh-space-shooter/v1.0.3** was hardened automatically. 8 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Multiple `${{ inputs.* }}` expressions are directly interpolated inside `run:` shell command strings (rule a), allowing script injection. In the 'Generate game GIF' step, `${{ inputs.username }}`, `${{ inputs.output-path }}`, `${{ inputs.strategy }}`, and `${{ inputs.fps }}` are all interpolated directly into the shell command. In the 'Commit and push GIF' step, `${{ inputs.output-path }}` and `${{ inputs.commit-message }}` are interpolated directly. An attacker controlling these inputs (e.g. via workflow_dispatch or a calling workflow) can inject arbitrary shell commands. All these values must be moved to `env:` variables and referenced as properly double-quoted `"$VAR"` shell variables.

Locations:

- `action.yml:55`
- `action.yml:56`
- `action.yml:57`
- `action.yml:58`
- `action.yml:64`
- `action.yml:65`

### unpinned-uses (severity: high)

The step 'Set up Python' uses `actions/setup-python@v5`, which is pinned to a mutable tag (`v5`) rather than an immutable full-length commit SHA (40 hex characters). A tag can be moved to point to a different, potentially malicious commit. It should be pinned to a specific SHA, e.g. `actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065 # v5`.

Locations:

- `action.yml:39`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.username }}" appears directly in run: block of step "Generate game GIF"; move to env: map

Locations:

- `action.yml:59`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.output-path }}" appears directly in run: block of step "Generate game GIF"; move to env: map

Locations:

- `action.yml:60`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.strategy }}" appears directly in run: block of step "Generate game GIF"; move to env: map

Locations:

- `action.yml:61`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.fps }}" appears directly in run: block of step "Generate game GIF"; move to env: map

Locations:

- `action.yml:62`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.output-path }}" appears directly in run: block of step "Commit and push GIF"; move to env: map

Locations:

- `action.yml:69`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.commit-message }}" appears directly in run: block of step "Commit and push GIF"; move to env: map

Locations:

- `action.yml:70`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, static-inline-injection

**Notes:**

1. Pinned actions/setup-python@v5 to full SHA a26af69be951a213d495a4c3e4e4022e16d87065 with # v5 comment. 2. In 'Generate game GIF' step: moved ${{ inputs.username }}, ${{ inputs.output-path }}, ${{ inputs.strategy }}, and ${{ inputs.fps }} into env: block as USERNAME, OUTPUT_PATH, STRATEGY, FPS; updated run: to use "$USERNAME", "$OUTPUT_PATH", "$STRATEGY", "$FPS". 3. In 'Commit and push GIF' step: moved ${{ inputs.output-path }} and ${{ inputs.commit-message }} into env: block as OUTPUT_PATH and COMMIT_MESSAGE; updated run: to use "$OUTPUT_PATH" and "$COMMIT_MESSAGE".

