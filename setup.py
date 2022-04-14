import pathlib
from setuptools import setup
from setuptools import find_packages


here = pathlib.Path(__file__).parent.resolve()
version = (here / "src" / "cript" / "VERSION.txt").read_text(encoding="utf-8")
long_description = (here / "README.md").read_text(encoding="utf-8")


setup(
    name="cript",
    version=version,
    description="CRIPT REST API and data model bindings",
    url="https://github.com/C-Accel-CRIPT/cript"
    author="CRIPT Development Team",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=3.9",
    install_requires=["beartype >= 0.10.0", "pint >= 0.18", "boto3 >= 1.21.10", "botocore >= 1.24.10", "globus-sdk >= 3.6.0"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
)