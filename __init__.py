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
    ProductIngredient,
    Procedure,
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
    ProductIngredient,
    Procedure,
    Process,
    Experiment,
]


secondary_node_lists = {
    "conditions": Condition,
    "properties": Property,
    "components": MaterialComponent,
    "quantities": Quantity,
    "material_ingredients": MaterialIngredient,
    "product_ingredients": ProductIngredient,
    "procedures": Procedure,
}


from .api_connector import API
