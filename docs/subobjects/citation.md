# Citation

## Definition
The citation sub-object provides a link to papers, books, or other scholarly work and allows users
to specify in what way the work relates to that data. More specifically, users can specify that the
data was directly extracted from, inspired by, derived from, etc. the 
<a href="../../nodes/reference" target="_blank">Reference</a>.


## Can be added to
* <a href="../../nodes/process" target="_blank">Process</a>
* <a href="../../nodes/data" target="_blank">Data</a>
* <a href="../../nodes/computational_process" target="_blank">Computational Process</a>
* <a href="../property" target="_blank">Property</a>
* <a href="../computational_forcefield" target="_blank">Computational Forcefield</a>
* <a href="../equipment" target="_blank">Equipment</a>
* <a href="../algorithm" target="_blank">Algorithm</a>
* <a href="../software_configuration" target="_blank">Software Configuration</a>


## Attributes

| Attribute | Type | Example               | Description                                                               | Required |
|-----------|------|-----------------------|---------------------------------------------------------------------------|----------|
| type      | str  | "derived_from"        | Pick from [CRIPT citation type](https://criptapp.org/keys/citation-type/) | True     |
| reference | str  | "My Scholarly Article" | Reference to a book, paper, or scholarly work                             | True     |

## Navigating to Citation

## Create
```python
my_citation = cript.citation(type="extracted_by_nlp", reference="https://myreference.com")
```

## Add Citation to Node
```python
data.add_citation(my_citation)
```

## Save
```python
data.save()
```

## Remove Citation From Node
```python
data.remove_citation(my_citation)
```

## Citation Node

```json hl_lines="11"
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