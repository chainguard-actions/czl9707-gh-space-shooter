<!-- markdownlint-disable -->

# Hardening Report: czl9707--gh-space-shooter/v2.0.4

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `1`

Action **czl9707--gh-space-shooter/v2.0.4** was hardened automatically. 17 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Sub-rule (a): The 'Generate game' step in action.yml directly interpolates multiple inputs expressions inside run: shell commands without going through env: variables. Offending lines: `gh-space-shooter ${{ inputs.username }}`, `--output ${{ inputs.output-path }}`, `--strategy ${{ inputs.strategy }}`, `--fps ${{ inputs.fps }}`, and `echo "output-file=${{ inputs.output-path }}" >> $GITHUB_OUTPUT`. An attacker controlling these inputs can inject arbitrary shell commands.

Locations:

- `action.yml:55`
- `action.yml:56`
- `action.yml:57`
- `action.yml:58`
- `action.yml:59`

### script-injection (severity: high)

Sub-rule (a): The 'Commit and push' step in action.yml directly interpolates inputs expressions into shell variable assignments inside a run: block: `OUTPUT_PATH="${{ inputs.output-path }}"`, `COMMIT_MSG="${{ inputs.commit-message }}"`, `NO_AMEND="${{ inputs.no-amend }}"`. These are YAML-template-substituted before the shell sees them, allowing injection of shell metacharacters.

Locations:

- `action.yml:67`
- `action.yml:68`
- `action.yml:69`

### github-env-injection (severity: high)

The 'Generate game' step writes ${{ inputs.output-path }} directly to $GITHUB_OUTPUT without sanitization (no `printf '%s' ... | tr -d '\n\r'` step). An attacker-controlled input containing newlines could inject additional key=value pairs into the output context.

Locations:

- `action.yml:59`

### script-injection (severity: high)

Sub-rule (a): In publish.yml, the 'Install Python' run: step directly interpolates `${{ env.PYTHON_LATEST }}` into the shell command: `uv python install ${{ env.PYTHON_LATEST }}`. Any ${{ ... }} expression inside a run: block is a script-injection risk regardless of context.

Locations:

- `.github/workflows/publish.yml:32`

### script-injection (severity: high)

Sub-rule (a): In test.yml, the 'Install Python' run: step directly interpolates `${{ matrix.python-version }}` into the shell command: `uv python install ${{ matrix.python-version }}`. Additionally, the 'Test Summary' step interpolates `${{ matrix.python-version }}` into an echo command that writes to $GITHUB_STEP_SUMMARY. Any ${{ ... }} expression inside a run: block is a script-injection risk.

Locations:

- `.github/workflows/test.yml:27`
- `.github/workflows/test.yml:36`

### unpinned-uses (severity: high)

action.yml references actions/setup-python@v6 — a mutable version tag rather than an immutable 40-character commit SHA. This allows supply-chain attacks if the tag is moved.

Locations:

- `action.yml:43`

### unpinned-uses (severity: high)

publish.yml contains multiple unpinned uses: references using mutable tags/branches instead of full 40-character commit SHAs: actions/checkout@v6 (line 26), astral-sh/setup-uv@v7 (line 29), callowayproject/bump-my-version@master (line 35), pypa/gh-action-pypi-publish@release/v1 (line 44), ncipollo/release-action@v1 (line 47).

Locations:

- `.github/workflows/publish.yml:26`
- `.github/workflows/publish.yml:29`
- `.github/workflows/publish.yml:35`
- `.github/workflows/publish.yml:44`
- `.github/workflows/publish.yml:47`

### unpinned-uses (severity: high)

test.yml contains unpinned uses: references using mutable version tags instead of full 40-character commit SHAs: actions/checkout@v6 (line 21), astral-sh/setup-uv@v7 (line 24).

Locations:

- `.github/workflows/test.yml:21`
- `.github/workflows/test.yml:24`

### missing-permissions (severity: medium)

test.yml has no top-level `permissions:` key and the single job 'test' also has no `permissions:` key. Without explicit permissions, the workflow inherits the default repository permissions, which may be overly broad.

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

Fixed all findings across action.yml, publish.yml, and test.yml:

1. action.yml - Generate game step: Moved all ${{ inputs.* }} expressions (username, output-path, strategy, fps) into env: block; sanitized output-path with printf/tr before writing to GITHUB_OUTPUT.
2. action.yml - Commit and push step: Moved ${{ inputs.output-path }}, ${{ inputs.commit-message }}, ${{ inputs.no-amend }} into env: block.
3. action.yml - Pinned actions/setup-python@v6 to SHA ece7cb06caefa5fff74198d8649806c4678c61a1.
4. publish.yml - Pinned all 5 unpinned actions to full commit SHAs; moved ${{ env.PYTHON_LATEST }} into env: block for the Install Python step.
5. test.yml - Pinned actions/checkout@v6 and astral-sh/setup-uv@v7 to full SHAs; moved ${{ matrix.python-version }} into env: blocks for Install Python and Test Summary steps; added top-level permissions: contents: read.

