from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='cript',
    version='0.0.1',
    url='',
    author='Dylan Walsh',
    author_email='dylanwal@mit.edu',
    description='CRIPT (A Community Resource for Innovation in Polymer Technology)',
    classifiers=[
                  "Programming Language :: Python :: 3",
                  "Operating System :: OS Independent",
              ],
    package_dir={"": "src"},
    py_modules=["cript", "criptdb"],
    packages=find_packages(where="src"),
    install_requires=[
        "pymongo>=3.11",
        "pint>=0.17",
        "bson>=0.5"
    ]
)
