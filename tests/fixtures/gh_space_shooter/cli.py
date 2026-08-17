"""Fake gh_space_shooter CLI for testing - creates a minimal GIF without API calls."""
import os
import sys


def app():
    """Fake Typer app that parses --output and creates a minimal GIF file."""
    args = sys.argv[1:]
    output = None
    strategy = "random"
    fps = 40
    prev = None

    for arg in args:
        if prev in ("--output", "-out", "-o"):
            output = arg
            prev = None
        elif prev == "--strategy" or prev == "-s":
            strategy = arg
            prev = None
        elif prev == "--fps":
            fps = arg
            prev = None
        elif arg.startswith("--output="):
            output = arg.split("=", 1)[1]
            prev = None
        elif arg.startswith("-"):
            prev = arg
        else:
            # positional argument (username)
            prev = None

    if output is None:
        # Default output name
        output = "gh-space-shooter.gif"

    # Create parent directory if needed
    outdir = os.path.dirname(output)
    if outdir:
        os.makedirs(outdir, exist_ok=True)

    # Write a minimal valid GIF89a file (1x1 pixel)
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

    print(f"Fake gh-space-shooter: created {output} (strategy={strategy}, fps={fps})")
    sys.exit(0)


if __name__ == "__main__":
    app()
