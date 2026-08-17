#!/bin/sh
# Fake gh-space-shooter: parses --output argument and creates a minimal GIF file.
# This avoids calling the real CLI or GitHub API during tests.

OUTPUT=""
prev=""
for arg in "$@"; do
  case "$prev" in
    --output|-out|-o)
      OUTPUT="$arg"
      ;;
  esac
  prev="$arg"
done

if [ -z "$OUTPUT" ]; then
  # Default output name based on first positional arg
  for arg in "$@"; do
    case "$arg" in
      -*) ;;
      *)
        if [ -z "$OUTPUT" ]; then
          OUTPUT="${arg}-gh-space-shooter.gif"
        fi
        ;;
    esac
  done
fi

if [ -z "$OUTPUT" ]; then
  OUTPUT="gh-space-shooter.gif"
fi

# Create parent directory if needed
OUTDIR="$(dirname "$OUTPUT")"
if [ -n "$OUTDIR" ] && [ "$OUTDIR" != "." ]; then
  mkdir -p "$OUTDIR"
fi

# Write a minimal valid GIF89a file (1x1 pixel, transparent)
# GIF89a header + logical screen descriptor + global color table + image descriptor + image data + trailer
printf 'GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x00\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b' > "$OUTPUT"

echo "Fake gh-space-shooter: created $OUTPUT"
exit 0
