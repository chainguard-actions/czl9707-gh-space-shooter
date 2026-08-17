<!-- markdownlint-disable -->

# Hardening Report: czl9707--gh-space-shooter/v2.0.0

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **czl9707--gh-space-shooter/v2.0.0** was hardened automatically. 18 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Sub-rule (a): Multiple ${{ inputs.* }} expressions are directly interpolated inside run: shell commands in the 'Generate game' step. This allows an attacker (who controls inputs) to inject arbitrary shell commands. Offending lines include: `gh-space-shooter ${{ inputs.username }} \`, `--output ${{ inputs.output-path }} \`, `--strategy ${{ inputs.strategy }} \`, `--fps ${{ inputs.fps }}`, and `echo "output-file=${{ inputs.output-path }}" >> $GITHUB_OUTPUT`. These should be moved to env: variables and then double-quoted in the shell script.

Locations:

- `action.yml:52`
- `action.yml:53`
- `action.yml:54`
- `action.yml:55`
- `action.yml:56`

### script-injection (severity: high)

Sub-rule (a): Multiple ${{ inputs.* }} expressions are directly interpolated inside the run: shell script in the 'Commit and push' step. Offending lines: `OUTPUT_PATH="${{ inputs.output-path }}"`, `COMMIT_MSG="${{ inputs.commit-message }}"`, `NO_AMEND="${{ inputs.no-amend }}"`. An attacker controlling these inputs can inject shell metacharacters before the shell ever sees the value.

Locations:

- `action.yml:62`
- `action.yml:63`
- `action.yml:64`

### github-env-injection (severity: high)

The 'Generate game' step writes an unsanitized ${{ inputs.output-path }} expression directly to $GITHUB_OUTPUT without the required sanitization step (printf '%s' ... | tr -d '\n\r'). A newline embedded in the input value could inject arbitrary key=value pairs into the output file. Offending line: `echo "output-file=${{ inputs.output-path }}" >> $GITHUB_OUTPUT`

Locations:

- `action.yml:56`

### unpinned-uses (severity: high)

The action.yml composite step uses actions/setup-python@v5, which is pinned to a mutable version tag rather than a full 40-character commit SHA. This is vulnerable to supply-chain attacks if the tag is moved.

Locations:

- `action.yml:44`

### script-injection (severity: high)

Sub-rule (a): ${{ env.PYTHON_LATEST }} and ${{ secrets.PYPI_API_TOKEN }} are directly interpolated inside run: shell commands in publish.yml. Offending lines: `run: uv python install ${{ env.PYTHON_LATEST }}` and `run: uv publish --token ${{ secrets.PYPI_API_TOKEN }}`. Even env.* and secrets.* contexts should not be interpolated directly into run: scripts; they should be passed via env: variables.

Locations:

- `.github/workflows/publish.yml:27`
- `.github/workflows/publish.yml:37`

### script-injection (severity: high)

Sub-rule (a): ${{ matrix.python-version }} is directly interpolated inside a run: shell command in test.yml. Offending lines: `run: uv python install ${{ matrix.python-version }}` and `echo "Tests completed for Python ${{ matrix.python-version }}" >> $GITHUB_STEP_SUMMARY`. Matrix values are workflow-controllable and must not be interpolated directly into shell scripts.

Locations:

- `.github/workflows/test.yml:27`
- `.github/workflows/test.yml:35`

### unpinned-uses (severity: high)

publish.yml references multiple actions pinned to mutable tags instead of full commit SHAs: actions/checkout@v6, astral-sh/setup-uv@v7, callowayproject/bump-my-version@master, ncipollo/release-action@v1. These are all vulnerable to supply-chain attacks.

Locations:

- `.github/workflows/publish.yml:21`
- `.github/workflows/publish.yml:24`
- `.github/workflows/publish.yml:30`
- `.github/workflows/publish.yml:43`

### unpinned-uses (severity: high)

test.yml references actions pinned to mutable tags instead of full commit SHAs: actions/checkout@v6 and astral-sh/setup-uv@v7. These are vulnerable to supply-chain attacks.

Locations:

- `.github/workflows/test.yml:20`
- `.github/workflows/test.yml:23`

### permissions (severity: medium)

publish.yml has no top-level permissions: key and no job-level permissions: key on any job. Without explicit permissions, the workflow inherits the repository's default token permissions, which may be overly broad.

Locations:

- `.github/workflows/publish.yml:1`

### permissions (severity: medium)

test.yml has no top-level permissions: key and no job-level permissions: key on any job. Without explicit permissions, the workflow inherits the repository's default token permissions, which may be overly broad.

Locations:

- `.github/workflows/test.yml:1`

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

**Fixes applied:** unpinned-uses, script-injection, github-env-injection, static-inline-injection, permissions

**Notes:**

Fixed all findings across action.yml, publish.yml, and test.yml:

**action.yml:**
- Pinned actions/setup-python@v5 to full SHA (a26af69be951a213d495a4c3e4e4022e16d87065)
- 'Generate game' step: moved inputs.username, inputs.output-path, inputs.strategy, inputs.fps into env: block; sanitized output-path with tr -d '\n\r' before writing to GITHUB_OUTPUT
- 'Commit and push' step: moved inputs.output-path, inputs.commit-message, inputs.no-amend into env: block

**publish.yml:**
- Pinned actions/checkout@v6, astral-sh/setup-uv@v7, callowayproject/bump-my-version@master, ncipollo/release-action@v1 to full SHAs
- Moved env.PYTHON_LATEST and secrets.PYPI_API_TOKEN into env: blocks for their respective run: steps
- Added top-level permissions: contents: write

**test.yml:**
- Pinned actions/checkout@v6 and astral-sh/setup-uv@v7 to full SHAs
- Moved matrix.python-version into env: blocks for 'Install Python' and 'Test Summary' steps
- Added top-level permissions: contents: read

