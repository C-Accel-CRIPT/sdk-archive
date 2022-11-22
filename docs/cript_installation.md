# How to Install CRIPT

This page will give you a step by step guide on how to install [CRIPT Python SDK](https://pypi.org/project/cript/) on your system.


## Steps
1.  Install [Python 3.9+](https://www.python.org/downloads/)
2.  Create a virtual environment
    * It is best practice to create a dedicated [python virtual environment](https://docs.python.org/3/library/venv.html) for each python project

    === ":fontawesome-brands-windows: **_Windows:_**"
        ```bash 
        python -m venv .\venv
        ```

    === ":fontawesome-brands-apple: **_Mac_** & :fontawesome-brands-linux: **_Linux:_**"
        ```bash 
        python3 -m venv ./venv
        ```

3.  Activate your virtual environment

    === ":fontawesome-brands-windows: **_Windows:_**"
        ```bash 
        .\venv\Scripts\activate
        ```

    === ":fontawesome-brands-apple: **_Mac_** & :fontawesome-brands-linux: **_Linux:_**"
        ```bash 
        source venv/bin/activate
        ```

4.  Install the [latest version of CRIPT](https://pypi.org/project/cript/)
    ```bash
     pip install -U cript
    ```
5.  Create your CRIPT Script!