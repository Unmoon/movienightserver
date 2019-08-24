from setuptools import find_packages
from setuptools import setup

setup(
    name="movienightserver",
    version="1.0.0",
    url="https://github.com/Unmoon/movienightserver",
    author="Unmoon",
    author_email="joona@unmoon.com",
    description="Simple server that syncs video playback for clients using Movie Night.",
    packages=find_packages(where=""),
    package_dir={"movienightserver": "movienightserver"},
    entry_points={"console_scripts": ["movienightserver=movienightserver.main:main"]},
)
