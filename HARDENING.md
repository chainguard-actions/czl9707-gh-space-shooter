<!-- markdownlint-disable -->

# Hardening Report: czl9707--gh-space-shooter/v2.0.3

> This file was generated automatically by the hardening agent.

**Policy SHA:** `374911c4be584df24e6da57af2d990570ef0f859`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **czl9707--gh-space-shooter/v2.0.3** was hardened automatically. 13 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

action.yml refers to an action by a version tag instead of a full commit SHA: `uses: actions/setup-python@v6`.

Locations:

- `action.yml:47`

### script-injection (severity: high)

Sub-rule (a): in the 'Generate game' step, inputs are pasted straight into the run script with no quotes: `gh-space-shooter ${{ inputs.username }} \`, `--output ${{ inputs.output-path }} \`, `--strategy ${{ inputs.strategy }} \`, `--fps ${{ inputs.fps }}`, and `echo "output-file=${{ inputs.output-path }}" >> $GITHUB_OUTPUT`.

Locations:

- `action.yml:63`

### script-injection (severity: high)

Sub-rule (a): in the 'Commit and push' step, inputs are pasted straight into the run script: `OUTPUT_PATH="${{ inputs.output-path }}"`, `COMMIT_MSG="${{ inputs.commit-message }}"`, `NO_AMEND="${{ inputs.no-amend }}"`. A commit message containing `"` or `$(...)` breaks out of the quotes and runs as a command.

Locations:

- `action.yml:75`

### github-env-injection (severity: high)

The 'Generate game' step writes inputs.output-path straight into $GITHUB_OUTPUT without stripping newlines (`printf '%s' ... | tr -d '\n\r'`): `echo "output-file=${{ inputs.output-path }}" >> $GITHUB_OUTPUT`. A value containing a newline can add extra outputs.

Locations:

- `action.yml:67`

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

### prior-fix (severity: high)

Carried forward from this version's previous harden, which fixed it; fix it again unless the code no longer has the problem. The previous harden changed action.yml without recording a finding for it, and this analysis reported nothing there. Re-apply its security changes unless the code no longer needs them. The previous patch:
```diff
diff --git a/action.yml b/action.yml
index 840fd31..ec72db2 100644
--- a/action.yml
+++ b/action.yml
@@ -1,11 +1,9 @@
 name: 'GitHub Space Shooter'
 description: 'Transform your GitHub contribution graph into a space shooter game GIF'
 author: 'zane'
-
 branding:
   icon: 'navigation-2'
   color: 'black'
-
 inputs:
   github-token:
     description: 'GitHub token for fetching contribution data (usually secrets.GITHUB_TOKEN)'
@@ -34,54 +32,75 @@ inputs:
     description: 'Commit message for the GIF update'
     required: false
     default: 'Update space shooter game GIF'
-
 outputs:
   output-file:
     description: 'Path to the generated output file (GIF or WebP)'
     value: ${{ steps.generate.outputs.output-file }}
-
 runs:
   using: 'composite'
   steps:
     - name: Set up Python
       uses: actions/setup-python@v6
       with:
         python-version: '3.12'
-
     - name: Install gh-space-shooter
       shell: bash
       run: |
         python -m pip install --upgrade pip
         pip install gh-space-shooter
-
     - name: Generate game
       id: generate
       shell: bash
       env:
         GH_TOKEN: ${{ inputs.github-token }}
+        INPUT_USERNAME: ${{ inputs.username }}
+        INPUT_OUTPUT_PATH: ${{ inputs.output-path }}
+        INPUT_STRATEGY: ${{ inputs.strategy }}
+        INPUT_FPS: ${{ inputs.fps }}
       run: |
-        gh-space-shooter ${{ inputs.username }} \
-          --output ${{ inputs.output-path }} \
-          --strategy ${{ inputs.strategy }} \
-          --fps ${{ inputs.fps }}
-        echo "output-file=${{ inputs.output-path }}" >> $GITHUB_OUTPUT
-
+        gh-space-shooter "$INPUT_USERNAME" \
+          --output "$INPUT_OUTPUT_PATH" \
+          --strategy "$INPUT_STRATEGY" \
+          --fps "$INPUT_FPS"
+        safe_output_path=$(printf '%s' "$INPUT_OUTPUT_PATH" | tr -d '\n\r')
+        echo "output-file=$safe_output_path" >> "$GITHUB_OUTPUT"
     - name: Commit and push
       shell: bash
+      env:
+        INPUT_OUTPUT_PATH: ${{ inputs.output-path }}
+        INPUT_COMMIT_MSG: ${{ inputs.commit-message }}
+        INPUT_NO_AMEND: ${{ inputs.no-amend }}
       run: |
         git config --local user.email "github-actions[bot]@users.noreply.github.com"
         git config --local user.name "github-actions[bot]"
 
-        OUTPUT_PATH="${{ inputs.output-path }}"
-        COMMIT_MSG="${{ inputs.commit-message }}"
-        NO_AMEND="${{ inputs.no-amend }}"
+        OUTPUT_PATH="$INPUT_OUTPUT_PATH"
+        COMMIT_MSG="$INPUT_COMMIT_MSG"
+        NO_AMEND="$INPUT_NO_AMEND"
 
         git add "$OUTPUT_PATH"
 
         SHOULD_AMEND="false"
         if [ "$NO_AMEND" != "true" ]; then
           git log -1 --oneline
-        
+
           LAST_MSG=$(git log -1 --pretty=%s 2>/dev/null || echo "")
           LAST_FILES=$(git log -1 --name-only --pretty=format: 2>/dev/null | grep -v '^$' || echo "")
 

```

Locations:

- `action.yml`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, github-env-injection, static-inline-injection, prior-fix

**Notes:**

Fixed every finding in action.yml. These are the same security changes as the earlier harden patch (that patch also deleted blank lines, which I left alone). I didn't run or test the action afterwards.

- **Pinned action:** `actions/setup-python` now points to commit ece7cb06caefa5fff74198d8649806c4678c61a1, with a `# v6` comment. I got the SHA from a lookup, not by guessing.
- **Generate game step:** the username, output-path, strategy and fps inputs now go through the step's `env:` block. The script uses them as double-quoted variables, so a value can't run as a command.
- **Step output:** before output-path is written to `$GITHUB_OUTPUT`, newlines are removed with `printf '%s' | tr -d '\n\r'`, so a crafted value can't add extra outputs.
- **Commit and push step:** output-path, commit-message and no-amend now go through `env:` as well. The existing shell variables (`OUTPUT_PATH`, `COMMIT_MSG`, `NO_AMEND`) take their values from these, so the rest of the script works as before.

### Iteration 2

**Fixes applied:** invalid-yaml

**Notes:**

Fixed the 'Generate game' step in action.yml, which an earlier edit had left broken. That edit had merged the step's 'id: generate', 'shell: bash' and 'env:' lines into the GH_TOKEN line, and left a stray `{{ inputs.output-path }}" >> $GITHUB_OUTPUT` at the end of the output line. I put back the id, shell and env keys, keeping all the hardened env vars, and removed the stray text. The output value is still sanitized before it is written to GITHUB_OUTPUT. No other behaviour changed.

