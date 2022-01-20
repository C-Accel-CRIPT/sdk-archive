import pprint

from cript import *
from cript import Q

cond_key = Cond.keys

for k, v in cond_key.items():
    v["unit_prefer"] = v["unit"]
    if v["unit"] != "":
        v["unit"] = str(Q(v["unit"]).to_base_units().units)

    print(f"{k}: {v['unit']}")


print()
print("#" * 50)
print("#" * 50)
print()


prop_key = Prop.keys
# pprint.pprint(prop_key)

for k, v in prop_key.items():
    v["unit_prefer"] = v["unit"]
    if v["unit"] != "" and v["unit"] is not None:
        v["unit"] = str(Q(v["unit"]).to_base_units().units)

    print(f"{k}: {v['unit']}")


print()
print("#" * 50)
print("#" * 50)
print()


data_key = Data.keys
# pprint.pprint(data_key)

for k, v in data_key.items():
    v["unit_prefer"] = v["unit"]
    if v["unit"] != "" and v["unit"] is not None:
        temp_list = []
        for unit_ in v["unit"]:
            if unit_ == "":
                temp_list.append(unit_)
            else:
                temp_list.append(str(Q(unit_).to_base_units().units))
        v["unit"] = temp_list

    print(f"{k}: {v['unit']}")

print()
print("#" * 50)
print("#" * 50)
print()


prop_key = Prop.keys
# pprint.pprint(prop_key)

for k, v in prop_key.items():
    v["unit_prefer"] = v["unit"]
    if v["unit"] != "" and v["unit"] is not None:
        v["unit"] = str(Q(v["unit"]).to_base_units().units)

    print(f"{k}: {v['unit']}")