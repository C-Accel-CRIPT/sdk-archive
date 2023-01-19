!!! abstract
    This page will give you a through guide on how to set up the
    <a href="https://pypi.org/project/cript/" target="_blank">CRIPT Python SDK</a>
    on your system.

1.  Install <a href="https://www.python.org/downloads/" target="_blank">Python 3.9+</a>

2.  Create a virtual environment

    > It is best practice to create a dedicated
    <a href="https://docs.python.org/3/library/venv.html" target="_blank">python virtual environment</a> for each python project

    === ":fontawesome-brands-windows: **_Windows:_**"
        ``` powershell
        python -m venv .\venv
        ```

    === ":fontawesome-brands-apple: **_Mac_** & :fontawesome-brands-linux: **_Linux:_**"
        ``` bash 
        python3 -m venv ./venv
        ```

3.  Activate your virtual environment

    === ":fontawesome-brands-windows: **_Windows:_**"
        ``` powershell 
        .\venv\Scripts\activate
        ```

    === ":fontawesome-brands-apple: **_Mac_** & :fontawesome-brands-linux: **_Linux:_**"
        ``` bash 
        source venv/bin/activate
        ```

4.  Install <a href="https://pypi.org/project/cript/" target="_blank">CRIPT from Python Package Index (PyPI)</a>
    ``` bash
     pip install cript
    ```

5.  Create your CRIPT Script!
