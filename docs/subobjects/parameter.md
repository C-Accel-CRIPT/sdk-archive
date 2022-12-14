# Parameter

## Definition
An input value to an algorithm

??? note
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


## Vocabulary
For a list of valid parameters please visit CRIPT
<a href="https://criptapp.org/keys/parameter-key/" target="_blank">parameter keys</a>


## Create
```python
my_parameter = cript.Parameter(key="buffer_distance", value="10", )
```

!!! warning
    Please be sure to use the correct value type _(str, int, etc.)_ because the SDK checks
    and if it is wrong it will throw an error. The correct types for all
    <a href="https://criptapp.org/keys/parameter-key/" target="_blank">parameter keys</a>
    can be found in the `Value type` column



## Add to <a href="../algorithm" target="_blank">algorithm</a>
```python
my_algorithm.add_parameter(my_parameter)
```

## Save
```python
my_software_configuration.add_algorithm()   # add algorithm to software configuration

my_software_configuration.save()    # save software configuration
```

## Remove from <a href="../algorithm" target="_blank">algorithm</a>
```python
my_algorithm.remove_parameter(my_parameter)
```