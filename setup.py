import pathlib
from setuptools import setup
from setuptools import find_packages


here = pathlib.Path(__file__).parent.resolve()
# single-source of version in the package
version = (here / "src" / "cript" / "VERSION.txt").read_text(encoding="utf-8")
# TODO: fill out README with installation guide, smallest working example, etc.
long_description = (here / "README.md").read_text(encoding="utf-8")


setup(
    name="cript",
    version=version,
    description="CRIPT Python SDK",
    url="https://github.com/C-Accel-CRIPT/cript",
    author="CRIPT Development Team",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=3.9",
    install_requires=[
        "beartype >= 0.10.4",
        "globus-sdk >= 3.7.0",
        "pint >= 0.19.2",
        "requests >= 2.27.1",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
)
