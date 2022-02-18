from .nodes import (
    Group,
    Collection,
    File,
    Data,
    Condition,
    Property,
    Identity,
    MaterialComponent,
    Material,
    Quantity,
    MaterialIngredient,
    IntermediateIngredient,
    Step,
    Process,
    Experiment,
)


node_classes = [
    Group,
    Collection,
    File,
    Data,
    Condition,
    Property,
    Identity,
    MaterialComponent,
    Material,
    Quantity,
    MaterialIngredient,
    IntermediateIngredient,
    Step,
    Process,
    Experiment,
]


secondary_node_lists = {
    "conditions": Condition,
    "properties": Property,
    "components": MaterialComponent,
    "quantities": Quantity,
    "material_ingredients": MaterialIngredient,
    "product_ingredients": IntermediateIngredient,
    "steps": Step,
}


from .api_connector import API
