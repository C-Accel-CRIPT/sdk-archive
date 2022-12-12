# Data

## Definition

The data node contains the meta-data to describe data that is beyond a single value i.e. n-dimensional data.


## Sub-Objects
* <a href="../../subobjects/citation" target="_blank">Citation</a>


## Attributes

| Attribute             | Type                                                | Example                  | Description                                                                             | Required |
|-----------------------|-----------------------------------------------------|--------------------------|-----------------------------------------------------------------------------------------|----------|
| experiment            | [Experiment](experiment.md)                         |                          | Experiment the data belongs to                                                          | True     |
| name                  | str                                                 | "my_data_name"           | Name of the data node                                                                   | True     |
| type                  | str                                                 | "nmr_h1"                 | Pick from [CRIPT data type controlled vocabulary](https://criptapp.org/keys/data-type/) | True     |
| files                 | list[[File](../supporting_nodes/file.md)]           | [file_1, file_2, file_3] | List of file nodes                                                                      | False    |
| sample_preperation    | [Process](process.md)                               |                          |                                                                                         | False    |
| computations          | list[[Computation](computation.md)]                 |                          | data produced from this Computation method                                              | False    |
| computational_process | [Computational Process](./computational_process.md) |                          | data was produced from this computation process                                         | False    |
| materials             | list[[Material](./material.md)]                     |                          | materials with attributes associated with the data node                                 | False    |
| process               | list[[Process](./process.md)]                       |                          | processes with attributes associated with the data node                                 | False    |
| citations             | [Citation](../subobjects/citation.md)               |                          | reference to a book, paper, or scholarly work                                           | False    |

## data Node

```json
{
    "url": "https://criptapp.org/api/data/2c70e00a-b4db-429a-a8ac-3b0d751f03cc/",
    "uid": "2c70e00a-b4db-429a-a8ac-3b0d751f03cc",
    "experiment": "https://criptapp.org/api/experiment/4ff25aaa-e139-494c-85ea-babca0a4c24c/",
    "name": "Crude SEC of polystyrene",
    "files": [],
    "type": "sec_trace",
    "sample_preparation": "https://criptapp.org/api/process/030ce2e9-834f-4912-9357-e589b1d1e7c1/",
    "computational_process": null,
    "computations": [],
    "citations": [],
    "notes": null,
    "public": true,
    "created_at": "2022-04-28T03:04:50.750972Z",
    "updated_at": "2022-08-11T00:40:46.416956Z",
    "group": "https://criptapp.org/api/group/3c612a84-1bf7-483a-942a-7ab56f71f83c/"
}
```



## Navigating to data 
`Data` can be easily found on <a href="https://criptapp.org" target="_blank">CRIPT</a> home screen in the 
<a href="https://criptapp.org/data/" target="_blank">Data link</a>

## Create
```python
expt = cript.Experiment.get(uid="e8ab6e1d-fd39-44c3-ac34-4d0a32296327")

my_data = cript.Data(
    experiment=expt, 
    name="My data", 
    type="sec_trace",
)
```

## Save
```python
my_data.save()
```

## Get
**_Get Project Node via UID:_**
```python
my_data = cript.Data.get(url="163cdec2-4f52-4a2c-8438-dc7f1c844fe9")
```

**_Get Project Node via URL:_**
```python
my_data = cript.Data.get(url="https://criptapp.org/data/163cdec2-4f52-4a2c-8438-dc7f1c844fe9/")
```

**_Get Project Node via Name:_**
```python
expt = cript.Experiment.get(uid="e8ab6e1d-fd39-44c3-ac34-4d0a32296327")
my_data = cript.Data.get(url="https://criptapp.org/data/163cdec2-4f52-4a2c-8438-dc7f1c844fe9/", experiment=expt)
```

## Delete

```python
my_data.delete()
```
