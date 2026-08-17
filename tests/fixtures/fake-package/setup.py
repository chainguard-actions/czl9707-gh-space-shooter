from setuptools import setup

setup(
    name="gh-space-shooter",
    version="999.0.0",
    py_modules=["fake_gh_space_shooter"],
    entry_points={
        "console_scripts": [
            "gh-space-shooter=fake_gh_space_shooter:main",
        ],
    },
)
