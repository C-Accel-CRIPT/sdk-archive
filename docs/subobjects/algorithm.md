# Algorithm

## Definition
Algorithm consists of parameter and condition details used in the [computation](../nodes/computation.md) 
and [computational process](../nodes/computational_process.md).


## Can be added to
* <a href="../software_configuration" target="_blank">Software Configuration</a>


## Sub-Objects
* <a href="../../subobjects/parameter" target="_blank">Parameter</a>
* <a href="../../subobjects/citation" target="_blank">Citation</a>


## Attributes

| Attribute | Type                            | Example             | Description                                   | Required |
|-----------|---------------------------------|---------------------|-----------------------------------------------|----------|
| key       | str                             | "advanced_sampling" | type of algorithm                             | True     |
| type      | str                             |                     | specific type of configuration, algorithm     | True     |
| parameter | list[[Parameter](../parameter)] |                     | setup associated parameters                   | False    |
| citation  | list[[Citation](../citation)]   |                     | reference to a book, paper, or scholarly work | False    |



## Algorithm keys
Please visit 
<a href="https://criptapp.org/keys/algorithm-key/" target="_blank">CRIPT algorithm vocabulary</a>


## algorithm Node

```json

```

## Navigating to algorithm

## Create
```python
my_algorithm = cript.Algorithm(key="advanced_sampling", type="simple random sampling")
```

## Add to <a href="../software_configuration" target="_blank">Software Configuration</a>
```python
my_software_configuration.add_algorithm(my_algorithm)
```

## Remove from <a href="../software_configuration" target="_blank">Software Configuration</a>
```python
my_software_configuration.remove_algorithm(my_algorithm)
```

## Save
```python
my_computation.save()   # save the primary node
```

## Get
```python

```