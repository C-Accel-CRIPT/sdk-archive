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


## Citation Node

```json linenums="1" hl_lines="10"

```

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

## Delete
```python
data.delete()
```