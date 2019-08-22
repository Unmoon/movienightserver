from setuptools import find_packages
from setuptools import setup

setup(
    name="movienightserver",
    version="1.0.0",
    url="",
    author="Unmoon",
    author_email="joona@unmoon.com",
    description="Simple VLC-based server that syncs video playback for clients.",
    packages=find_packages(where="src"),
    package_dir={"movienightserver": "src/movienightserver"},
    entry_points={"console_scripts": ["movienightserver=movienightserver.main:main"]},
    install_requires=[],
)
