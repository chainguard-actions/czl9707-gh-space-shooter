<!-- markdownlint-disable -->

# Hardening Report: czl9707--gh-space-shooter/v2.0.2

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **czl9707--gh-space-shooter/v2.0.2** was hardened automatically. 16 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Sub-rule (a): Multiple ${{ inputs.* }} expressions are interpolated directly into run: shell commands in action.yml. In the 'Generate game' step: `gh-space-shooter ${{ inputs.username }} --output ${{ inputs.output-path }} --strategy ${{ inputs.strategy }} --fps ${{ inputs.fps }}` and `echo "output-file=${{ inputs.output-path }}" >> $GITHUB_OUTPUT`. In the 'Commit and push' step: `OUTPUT_PATH="${{ inputs.output-path }}"`, `COMMIT_MSG="${{ inputs.commit-message }}"`, `NO_AMEND="${{ inputs.no-amend }}"` are all interpolated directly into the shell script body before the shell parses them, allowing an attacker-controlled value to inject shell metacharacters.

Locations:

- `action.yml:52`
- `action.yml:53`
- `action.yml:54`
- `action.yml:55`
- `action.yml:57`
- `action.yml:65`
- `action.yml:66`
- `action.yml:67`

### script-injection (severity: high)

Sub-rule (a): ${{ matrix.python-version }} is interpolated directly into a run: shell command in test.yml: `run: uv python install ${{ matrix.python-version }}` and `echo "Tests completed for Python ${{ matrix.python-version }}" >> $GITHUB_STEP_SUMMARY`. The matrix value flows through YAML template substitution before the shell parses it.

Locations:

- `.github/workflows/test.yml:26`
- `.github/workflows/test.yml:35`

### script-injection (severity: high)

Sub-rule (a): ${{ env.PYTHON_LATEST }} is interpolated directly into a run: shell command in publish.yml: `run: uv python install ${{ env.PYTHON_LATEST }}`. Any ${{ ... }} expression inside a run: block is a script-injection risk as it is substituted before the shell parses the command.

Locations:

- `.github/workflows/publish.yml:33`

### github-env-injection (severity: high)

The 'Generate game' step writes the unsanitized input value ${{ inputs.output-path }} directly to $GITHUB_OUTPUT without the required sanitization step (printf '%s' ... | tr -d '\n\r'): `echo "output-file=${{ inputs.output-path }}" >> $GITHUB_OUTPUT`. An attacker-controlled value containing newlines could inject additional environment variables or outputs.

Locations:

- `action.yml:57`

### unpinned-uses (severity: high)

action.yml uses actions/setup-python@v6 — a mutable version tag instead of a full 40-character commit SHA. This is vulnerable to supply-chain attacks if the tag is moved.

Locations:

- `action.yml:44`

### unpinned-uses (severity: high)

publish.yml uses multiple unpinned action references with mutable tags or branch names instead of full 40-character commit SHAs: actions/checkout@v6, astral-sh/setup-uv@v7, callowayproject/bump-my-version@master (branch!), pypa/gh-action-pypi-publish@release/v1 (branch!), ncipollo/release-action@v1.

Locations:

- `.github/workflows/publish.yml:27`
- `.github/workflows/publish.yml:30`
- `.github/workflows/publish.yml:36`
- `.github/workflows/publish.yml:46`
- `.github/workflows/publish.yml:49`

### unpinned-uses (severity: high)

test.yml uses multiple unpinned action references with mutable version tags instead of full 40-character commit SHAs: actions/checkout@v6, astral-sh/setup-uv@v7.

Locations:

- `.github/workflows/test.yml:19`
- `.github/workflows/test.yml:22`

### missing-permissions (severity: medium)

test.yml has no top-level permissions: key and the 'test' job also has no job-level permissions: key. Without explicit permissions, the workflow inherits the default repository permissions, which may be overly broad (e.g., write access to contents).

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

**Fixes applied:** script-injection, github-env-injection, unpinned-uses, missing-permissions, static-inline-injection

**Notes:**

Fixed all findings across action.yml, test.yml, and publish.yml:

**action.yml**:
- Pinned actions/setup-python@v6 → @ece7cb06caefa5fff74198d8649806c4678c61a1 # v6
- Moved all ${{ inputs.* }} expressions (username, output-path, strategy, fps, commit-message, no-amend) into env: blocks; referenced as $INPUT_USERNAME, $INPUT_OUTPUT_PATH, $INPUT_STRATEGY, $INPUT_FPS, $OUTPUT_PATH, $COMMIT_MSG, $NO_AMEND in shell
- Sanitized output-path before writing to $GITHUB_OUTPUT using printf + tr -d '\n\r'

**test.yml**:
- Added top-level `permissions: contents: read`
- Pinned actions/checkout@v6 → @d23441a48e516b6c34aea4fa41551a30e30af803 # v6
- Pinned astral-sh/setup-uv@v7 → @37802adc94f370d6bfd71619e3f0bf239e1f3b78 # v7
- Moved ${{ matrix.python-version }} into env: PYTHON_VERSION in both affected steps

**publish.yml**:
- Pinned actions/checkout@v6 → @d23441a48e516b6c34aea4fa41551a30e30af803 # v6
- Pinned astral-sh/setup-uv@v7 → @37802adc94f370d6bfd71619e3f0bf239e1f3b78 # v7
- Pinned callowayproject/bump-my-version@master → @1f1e0da9e4647e424cdcb736b3cd4d26a8bb70fb # master
- Pinned pypa/gh-action-pypi-publish@release/v1 → @ba38be9e461d3875417946c167d0b5f3d385a247 # release/v1
- Pinned ncipollo/release-action@v1 → @339a81892b84b4eeb0f6e744e4574d79d0d9b8dd # v1
- Moved ${{ env.PYTHON_LATEST }} into env: PYTHON_VER in the Install Python step

