<!-- markdownlint-disable -->

# Hardening Report: czl9707--gh-space-shooter/v2.0.4

> This file was generated automatically by the hardening agent.

**Policy SHA:** `374911c4be584df24e6da57af2d990570ef0f859`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **czl9707--gh-space-shooter/v2.0.4** was hardened automatically. 13 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The composite step points at a tag instead of a full commit SHA: `uses: actions/setup-python@v6`.

Locations:

- `action.yml:47`

### script-injection (severity: high)

Sub-rule (a): in the 'Generate game' step, ${{ }} expressions are placed directly inside the run: script, unquoted: `gh-space-shooter ${{ inputs.username }} \`, `--output ${{ inputs.output-path }} \`, `--strategy ${{ inputs.strategy }} \`, `--fps ${{ inputs.fps }}`, and `echo "output-file=${{ inputs.output-path }}" >> $GITHUB_OUTPUT`.

Locations:

- `action.yml:63`

### script-injection (severity: high)

Sub-rule (a): in the 'Commit and push' step, ${{ }} expressions are placed directly inside the run: script: `OUTPUT_PATH="${{ inputs.output-path }}"`, `COMMIT_MSG="${{ inputs.commit-message }}"`, `NO_AMEND="${{ inputs.no-amend }}"`. Double quotes don't help here, because the expression is substituted into the script text before the shell parses it.

Locations:

- `action.yml:75`

### github-env-injection (severity: high)

The 'Generate game' step writes an untrusted input to $GITHUB_OUTPUT with no newline stripping: `echo "output-file=${{ inputs.output-path }}" >> $GITHUB_OUTPUT`. A value containing a newline can inject extra output entries. Pass the value through env and run `printf '%s' ... | tr -d '\n\r'` before the write.

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
index 840fd31..78a7209 100644
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
+        safe_output=$(printf '%s' "$INPUT_OUTPUT_PATH" | tr -d '\n\r')
+        echo "output-file=$safe_output" >> "$GITHUB_OUTPUT"
     - name: Commit and push
       shell: bash
+      env:
+        INPUT_OUTPUT_PATH: ${{ inputs.output-path }}
+        INPUT_COMMIT_MESSAGE: ${{ inputs.commit-message }}
+        INPUT_NO_AMEND: ${{ inputs.no-amend }}
       run: |
         git config --local user.email "github-actions[bot]@users.noreply.github.com"
         git config --local user.name "github-actions[bot]"
 
-        OUTPUT_PATH="${{ inputs.output-path }}"
-        COMMIT_MSG="${{ inputs.commit-message }}"
-        NO_AMEND="${{ inputs.no-amend }}"
+        OUTPUT_PATH="$INPUT_OUTPUT_PATH"
+        COMMIT_MSG="$INPUT_COMMIT_MESSAGE"
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

Pinned actions/setup-python to ece7cb06caefa5fff74198d8649806c4678c61a1 (# v6). Moved inputs.username, output-path, strategy and fps into the env: block of the 'Generate game' step and quoted them where the script uses them. Stripped newlines from the output path before writing it to $GITHUB_OUTPUT. Moved output-path, commit-message and no-amend into the env: block of the 'Commit and push' step. This re-applies the previous harden's patch.

### Iteration 2

**Fixes applied:** script-injection, invalid-yaml

**Notes:**

Fixed two problems in action.yml.

1. invalid-yaml: the 'Generate game' step was broken. Its env entry for GH_TOKEN was joined onto the 'name:' line, and the 'id:', 'shell:' and 'env:' keys were missing. I put back 'id: generate' (the action's output-file reads steps.generate.outputs), 'shell: bash' and a proper 'env:' block. GH_TOKEN is the variable the CLI reads (src/gh_space_shooter/cli.py).

2. script-injection: in 'Commit and push' I removed the line that pasted the no-amend input straight into the script (NO_AMEND="${{ inputs.no-amend }}"). I also fixed the stray extra quote, so the line is now NO_AMEND="$INPUT_NO_AMEND".

The first attempt at the second edit reported success, but re-reading the file showed it hadn't applied. I applied it again and confirmed the file now has only the correct line.

