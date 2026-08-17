"""Fake gh-space-shooter CLI for testing."""
import sys
import os


def main():
    """Parse --output argument and create a minimal GIF file."""
    args = sys.argv[1:]
    output = None
    prev = None
    positional = []

    for arg in args:
        if prev in ("--output", "-out", "-o"):
            output = arg
            prev = None
        elif arg.startswith("--output="):
            output = arg.split("=", 1)[1]
            prev = None
        elif arg.startswith("-"):
            prev = arg
        else:
            if prev is None:
                positional.append(arg)
            prev = None

    if output is None:
        # Default: use first positional arg as username
        username = positional[0] if positional else "unknown"
        output = f"{username}-gh-space-shooter.gif"

    # Create parent directory if needed
    outdir = os.path.dirname(output)
    if outdir:
        os.makedirs(outdir, exist_ok=True)

    # Write a minimal valid GIF89a (1x1 pixel)
    gif_data = (
        b"GIF89a"
        b"\x01\x00\x01\x00\x80\x00\x00"  # header + screen descriptor
        b"\xff\xff\xff\x00\x00\x00"        # global color table (2 colors)
        b"\x21\xf9\x04\x00\x00\x00\x00\x00"  # graphic control extension
        b"\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00"  # image descriptor
        b"\x02\x02\x44\x01\x00"            # image data
        b"\x3b"                             # trailer
    )

    with open(output, "wb") as f:
        f.write(gif_data)

    print(f"Fake gh-space-shooter: created {output}")
    sys.exit(0)


if __name__ == "__main__":
    main()
