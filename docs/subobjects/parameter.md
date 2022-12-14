# Parameter

## Definition
An input value to an algorithm

!!! note
    For typical computations, the difference between
    parameter and condition lies in whether it changes the thermodynamic state of the simulated
    system: Variables that are part of defining a thermodynamic state should be defined as a condition
    in a parent node. 
    
    Therefore, ‘number’ and ‘volume’ need to be listed as conditions while
    ‘boundaries’ and ‘origin’ are parameters of ensemble size

## Can be added to
* <a href="../algorithm" target="_blank">algorithm</a>

## Attribute
| Attribute | Type | Example           | Description       | Required |
|-----------|------|-------------------|-------------------|----------|
| key       | str  | "buffer_distance" | type of parameter | True     |
| value     | any  | "10"              | value for type    | True     |
| unit      | str  | "meter"           | unit of parameter | True     |



## Create
```python

```


## Add to <a href="../algorithm" target="_blank">algorithm</a>
```python

```

## Save
```python

```

## Remove from <a href="../algorithm" target="_blank">algorithm</a>
```python

```