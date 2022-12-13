# File

## Definition
The File sub-object provides a link to papers, books, or other scholarly work and allows users
to specify in what way the work relates to that data. More specifically, users can specify that the
data was directly extracted from, inspired by, derived from, etc. the 
<a href="../../nodes/data" target="_blank">Data</a>.


## Attributes

| Attribute       | Type | Example                                                                                           | Description                                                                 | Required |
|-----------------|------|---------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------|----------|
| source          | str  | "path/to/my/file" or "https://en.wikipedia.org/wiki/Simplified_molecular-input_line-entry_system" | path to the file can be URL or local path                                   | True     |
| type            | str  | "logs"                                                                                            | Pick from [CRIPT File Type](https://criptapp.org/keys/file-type/)           | True     |
| extension       | str  | ".csv"                                                                                            | file extension                                                              | True     |
| data_dictionary | str  | {}                                                                                            | set of information describing the contents, format, and structure of a file | False    |


## File Node

```json
{
    "url": "https://criptapp.org/api/file/3df04dab-c32f-409c-9617-4d0fa005024e/",
    "uid": "3df04dab-c32f-409c-9617-4d0fa005024e",
    "group": "https://criptapp.org/api/group/deaa7088-2aac-4f30-a3f6-ad8a4439cafa/",
    "project": "https://criptapp.org/api/project/71c02b08-3dfb-48e4-80a4-79a4dbc1f5f2/",
    "checksum": "a109173ead2236a3be738205407b1f7ec6222e235e32201e76ad3114160e8d2a",
    "name": "H NMR_ATRP of MMA.pdf",
    "extension": ".pdf",
    "unique_name": "3df04dab-c32f-409c-9617-4d0fa005024e.pdf",
    "source": "https://criptapp.org/file/download/3df04dab-c32f-409c-9617-4d0fa005024e/",
    "type": "data",
    "public": true,
    "created_at": "2022-05-24T19:14:29.284983Z",
    "updated_at": "2022-08-04T04:04:37.798069Z"
}
```

## Finding File within CRIPT website

## Create
```python
proj = cript.Project.get(uri="38e7b0d0-a8f7-4864-bef8-209ee6cc60f6") # project the file belongs to

file_path = "C:\Users\myUsername\OneDrive\Desktop\CRIPT\myfile.csv" # path to local file

my_file = cript.File(project=proj, source=file_path) # create file node
```

## Upload
```python
my_file.save() # upload the file to CRIPT
```

## Download
Download a file from CRIPT

```python
my_file = cript.File(project=proj, source=file_path)

path = "C:\Users\navid\OneDrive\Desktop\CRIPT_Downloads"

file.download_file(path=path)
```

!!! note "Default Download"
    The default path for a download is your current directory

## Get

## Delete
