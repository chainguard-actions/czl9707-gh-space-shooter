<!-- markdownlint-disable -->

# Hardening Report: czl9707--gh-space-shooter/v2.0.5

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **czl9707--gh-space-shooter/v2.0.5** was hardened automatically. 14 finding(s) were identified and resolved across 1 iteration(s).

## Findings Fixed

### script-injection (severity: high)

Sub-rule (a): Multiple ${{ inputs.* }} expressions are interpolated directly inside run: shell command strings in action.yml. In the 'Generate game' step, inputs.username, inputs.output-path, inputs.strategy, and inputs.fps are injected directly into the shell command line — an attacker-controlled value can inject arbitrary shell commands. In the 'Commit and push' step, inputs.output-path, inputs.commit-message, and inputs.no-amend are interpolated directly into shell variable assignments (e.g. OUTPUT_PATH="${{ inputs.output-path }}"). These should be passed via env: variables and then referenced as double-quoted shell variables.

Locations:

- `action.yml:55`
- `action.yml:56`
- `action.yml:57`
- `action.yml:58`
- `action.yml:59`
- `action.yml:66`
- `action.yml:67`
- `action.yml:68`

### script-injection (severity: high)

Sub-rule (a): ${{ env.PYTHON_LATEST }} is interpolated directly inside a run: shell command string in publish.yml (line: `run: uv python install ${{ env.PYTHON_LATEST }}`). Even though env.* looks safe, any ${{ ... }} expression inside a run: block is a script-injection risk as it undergoes YAML template substitution before the shell sees it. It should be referenced as the shell env var $PYTHON_LATEST instead.

Locations:

- `.github/workflows/publish.yml:33`

### script-injection (severity: high)

Sub-rule (a): ${{ matrix.python-version }} is interpolated directly inside a run: shell command string in test.yml (line: `run: uv python install ${{ matrix.python-version }}`). Matrix values flow through YAML template substitution before the shell sees them and must not appear directly in run: blocks. It should be referenced as a shell env var instead.

Locations:

- `.github/workflows/test.yml:28`

### github-env-injection (severity: high)

The 'Generate game' step writes the value of ${{ inputs.output-path }} directly to $GITHUB_OUTPUT without sanitization: `echo "output-file=${{ inputs.output-path }}" >> $GITHUB_OUTPUT`. An attacker-controlled input containing newlines could inject arbitrary key=value pairs into GITHUB_OUTPUT. The value must be sanitized with `printf '%s' "$VAR" | tr -d '\n\r'` before writing.

Locations:

- `action.yml:59`

### unpinned-uses (severity: high)

Multiple uses: references are pinned to mutable tags or branch names rather than immutable 40-character commit SHAs, making the action vulnerable to supply-chain attacks if those tags are moved or branches are force-pushed. Failing references: action.yml: `actions/setup-python@v6`; publish.yml: `actions/checkout@v6`, `astral-sh/setup-uv@v7`, `callowayproject/bump-my-version@master`, `pypa/gh-action-pypi-publish@release/v1`, `ncipollo/release-action@v1`; test.yml: `actions/checkout@v6`, `astral-sh/setup-uv@v7`.

Locations:

- `action.yml:44`
- `.github/workflows/publish.yml:26`
- `.github/workflows/publish.yml:29`
- `.github/workflows/publish.yml:33`
- `.github/workflows/publish.yml:42`
- `.github/workflows/publish.yml:45`
- `.github/workflows/test.yml:20`
- `.github/workflows/test.yml:23`

### missing-permissions (severity: medium)

test.yml has no top-level permissions: key and the single job ('test') also has no job-level permissions: key. Without explicit permissions, the workflow inherits the repository's default token permissions, which may be broader than necessary (e.g. write access to contents). A minimal permissions block such as `permissions: read-all` or specific scopes should be added.

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

1. action.yml - script-injection/static-inline-injection: Moved all ${{ inputs.* }} expressions (username, output-path, strategy, fps, commit-message, no-amend) into env: blocks in both 'Generate game' and 'Commit and push' steps. Shell scripts now reference them as double-quoted env vars.

2. action.yml - github-env-injection: Sanitized the output-path value with `printf '%s' "$INPUT_OUTPUT_PATH" | tr -d '\n\r'` before writing to $GITHUB_OUTPUT.

3. action.yml - unpinned-uses: Pinned actions/setup-python@v6 to @ece7cb06caefa5fff74198d8649806c4678c61a1.

4. publish.yml - script-injection: Replaced `uv python install ${{ env.PYTHON_LATEST }}` with `uv python install "$PYTHON_LATEST"` (shell env var already available).

5. publish.yml - unpinned-uses: Pinned actions/checkout@v6, astral-sh/setup-uv@v7, callowayproject/bump-my-version@master, pypa/gh-action-pypi-publish@release/v1, and ncipollo/release-action@v1 to their full commit SHAs.

6. test.yml - script-injection: Moved ${{ matrix.python-version }} into env: blocks as PYTHON_VERSION in both 'Install Python' and 'Test Summary' steps.

7. test.yml - unpinned-uses: Pinned actions/checkout@v6 and astral-sh/setup-uv@v7 to their full commit SHAs.

8. test.yml - missing-permissions: Added top-level `permissions: contents: read` block.

