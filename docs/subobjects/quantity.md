# Quantity

## Definition
The amount of material involved in a process. They are used in the ingredients sub-object. 


## Super-Object
* <a href="../ingredient" target="_blank">Ingredients</a>


## Sub-Objects
* None


## Attributes

| Attribute        | Type | Example | Description                                                                       | Required |
|------------------|------|---------|-----------------------------------------------------------------------------------|----------|
| key              | str  | "mass"  | Pick from [type of quantity](https://criptapp.org/keys/quantity-key/)             | True     |
| value            | Any  | 1.23    | amount of material                                                                | True     |
| unit             | str  | "grams" | unit for quantity                                                                 | True     |
| uncertainty      | Any  | 0.1     | uncertainty of value (margin of error)                                            | True     |
| uncertainty_type | any  | std     |  Pick [ Uncertainty type Vocabulary](https://criptapp.org/keys/uncertainty-type/) | True     |                                                                                           | True     |


!!! tip "Quantity"
    The proper: 

    * value type (number)
    * range ([0, 1.79e+308])
    * SI Unit (kg)
    * Preferred Unit (ml)
    * Description
    
    can be found in the [CRIPT Quantity vocabulary](https://criptapp.org/keys/quantity-key/)



## Quantity Node

```json

```



## Navigating to quantity 

## Create
```python
initiator_qty = cript.Quantity(key="volume", value=0.017, unit="ml")
```

## Add Quantity to Ingredient
```python
initiator = cript.Ingredient(
    keyword="initiator", 
    material=solution, 
    quantities=[initiator_qty]
)
```

## Save

## Get

## Delete
