"""Module to work with setuptools."""
import toml
from setuptools import setup


def get_install_requirements():
    """Extracts required libraries from Pipfile and returns in a list suitable
    for setuptools."""
    try:
        with open(file="Pipfile", encoding="UTF-8") as pipfile_handle:
            pipfile = pipfile_handle.read()
        pipfile_toml = toml.loads(pipfile)
    except FileNotFoundError:
        return []  # if the package's key isn't there then just return an empty list
    try:
        required_packages = pipfile_toml["packages"].items()
    except KeyError:
        return []

    return [f"{pkg}{ver}" if ver != "*" else pkg for pkg, ver in required_packages]


if __name__ == "__main__":
    setup(
        install_requires=get_install_requirements(),
    )
