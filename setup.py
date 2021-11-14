import toml
from setuptools import setup


def get_install_requirements():
    try:
        with open("Pipfile") as fh:
            pipfile = fh.read()
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
