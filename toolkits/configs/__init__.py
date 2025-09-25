import yaml
import re
from dataclasses import dataclass
import platform
import os

CONFIG_ADDRESSES_ADDRESS = os.path.join(os.path.dirname(__file__), "addresses.yaml")

## YAML reader set up
yaml.SafeLoader.add_implicit_resolver(
    u'tag:yaml.org,2002:float',
    re.compile(u'''^(?:
     [-+]?(?:[0-9][0-9_]*)\\.[0-9_]*(?:[eE][-+]?[0-9]+)?
    |[-+]?(?:[0-9][0-9_]*)(?:[eE][-+]?[0-9]+)
    |\\.[0-9_]+(?:[eE][-+][0-9]+)?
    |[-+]?[0-9][0-9_]*(?::[0-5]?[0-9])+\\.[0-9_]*
    |[-+]?\\.(?:inf|Inf|INF)
    |\\.(?:nan|NaN|NAN))$''', re.X),
    list(u'-+0123456789.'))

def setup_addresses():
    try:
        user = os.getlogin()
    except:
        user = "tqtraaqs"
    global_addresses = {
        "user": user,
        "home": os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    }

    with open(CONFIG_ADDRESSES_ADDRESS, "rb") as file:
        config_data = yaml.safe_load(file)

    if "global_addresses" in config_data:
        for k in set(["_".join(s.split("_")[:-1]) for s in config_data["global_addresses"].keys()]):
            value = config_data["global_addresses"][k + f"_{platform.system().lower()}"]
            value = config_data["global_addresses"][k + f"_{platform.system().lower()}"]
            for kg, vg in global_addresses.items():
                value = value.replace("$" + kg.upper() + "$", vg)
            
            global_addresses[k] = value
    
    addresses = {}
    for k in config_data["addresses"].keys():
        ad = config_data["addresses"][k]
        modified_ad = ""

        splitted = ad.split("$")
        assert len(splitted) % 2 == 1, f"The number of $ characters in each address (c.f. {k}) must be even."
        for i in range(len(splitted)):
            if i % 2 == 0:
                modified_ad += splitted[i]
            else:
                assert splitted[i].lower() in global_addresses.keys(), f"Invalid value found: ${splitted[i]}$ in {k}."
                modified_ad += global_addresses[splitted[i].lower()]
        if platform.system().lower() == "windows":
            modified_ad = modified_ad.replace("/", "\\")
        addresses[k] = modified_ad

    
    Addresses = dataclass(type("Addresses", (), addresses))
    if "dated" in config_data:
        for var in config_data["dated"]:
            add = getattr(Addresses, var)
            setattr(Addresses, f"get_{var}_by_date", lambda date, add=add : os.path.join(
                os.path.dirname(add), date, os.path.basename(add)
            ))
    return Addresses, config_data.get("properties", [])

Addresses, properties = setup_addresses()
package_names = []
for property in properties:
    package_name = "".join([s[0].upper() + s[1:] for s in property.split("_")])
    package_names.append(package_name)
    address = getattr(Addresses, property)
    with open(address) as file:
        properties_dict = yaml.safe_load(file)
    exec(f"global {package_name}")
    exec(f"{package_name} = dataclass(type('{package_name}', (), properties_dict))")

__all__ = [
    "Addresses",
    *package_names
]