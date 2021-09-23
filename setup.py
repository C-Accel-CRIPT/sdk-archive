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
                  "Programming Language :: Python :: 3.9",
                  "Operating System :: OS Independent",
              ],
    package_dir={"": "src"},
    py_modules=["cript"],
    packages=find_packages(where="src"),
    package_data={
        "": ["*.xlsx", "*.zip", "*.csv"]
    },
    python_requires=">=3.9",
    install_requires=[
        "pymongo[srv]>=3.11",
        "pint>=0.17",
        "jsonpatch>=1.32",
        "fuzzywuzzy>=0.18.0",
        "rxnpy>=0.0.1"
    ]
)
