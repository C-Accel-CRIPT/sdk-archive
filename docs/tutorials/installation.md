!!! abstract
    This page will give you a through guide on how to set up the
    <a href="https://pypi.org/project/cript/" target="_blank">CRIPT Python SDK</a>
    on your system.

1.  Make sure <a href="https://www.python.org/downloads/" target="_blank">Python 3.9+</a> is installed.

2.  It is best practice to create a dedicated <a href="https://docs.python.org/3/library/venv.html" target="_blank">python virtual environment</a> for each python project:

    === ":fontawesome-brands-windows: **_Windows:_**"
        ``` powershell
        python -m venv .\venv
        ```

    === ":fontawesome-brands-apple: **_Mac_** & :fontawesome-brands-linux: **_Linux:_**"
        ``` bash 
        python3 -m venv ./venv
        ```

3.  Next, activate your virtual environment:

    === ":fontawesome-brands-windows: **_Windows:_**"
        ``` powershell 
        .\venv\Scripts\activate
        ```

    === ":fontawesome-brands-apple: **_Mac_** & :fontawesome-brands-linux: **_Linux:_**"
        ``` bash 
        source venv/bin/activate
        ```

4.  Finally, install <a href="https://pypi.org/project/cript/" target="_blank">CRIPT from Python Package Index (PyPI)</a> into your virtual environment:
    ``` bash
     pip install cript
    ```
You may also install other Python packages into this environment that might be useful for organizing your data, such as <a href="https://pandas.pydata.org/" target="_blank">Pandas</a> or <a href="https://numpy.org/" target="_blank">Numpy</a>.


Now you're ready to use the CRIPT Python SDK! Check out the <a href="../full_tutorial">full tutorial</a> for some examples.
