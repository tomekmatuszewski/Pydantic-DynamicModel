from pydantic import create_model, BaseModel
from pydantic.types import StrictStr,StrictInt
from typing import Optional, Dict, List
import json
from pydantic import ValidationError

entity = "two_levels_model"

def get_file(entity: str):
    with open(f"{entity}.json") as file_json:
        return json.load(file_json)

class Config:
    extra= 'forbid'

def create_dynamic_model(json_model: dict, new_model: dict) -> dict:
    for field, value in json_model.items():
        if json_model[field]["type"] != "json":
            new_model[field] = (eval(json_model[field]["type"]), ...)
        else:
            new_model[field] = (create_model(field, **create_dynamic_model(json_model[field]["data"], {}), __config__=Config), ...)

    return new_model


if __name__ == "__main__":
    json_model = get_file(entity)
    Model = create_model(entity, **create_dynamic_model(json_model, {}), __config__=Config)
    print(Model.schema_json(indent=4))

    # checking
    dct = {
        "name": "1",
        "addresses": [
            {"street": "street address", "city": "City"},
            {"street": "111", "postal": "111-1111"}
        ],
        "custom_attributes": {
            "attr1": "attr1-ffff",
            "attr2": "attr2"
        }
    }

    print(Model(**dct))

    dct1 = {
        "name": "1",
        "addresses": [
            {"street": "street address", "city": "City"},
            {"street": "111", "postal": "111-1111"}
        ],
        "custom_attributes": {
            "attr1": "attr1-ffff",
            "attr2": "attr2",
            "extra": "1111"
        }
    }

    try:
        Model(**dct1)
    except ValidationError as e:
        print(e)

    dct2 = {
        "name": "1",
        "addresses": [
            {"street": "street address", "city": "City"},
            {"street": "111", "postal": "111-1111"}
        ],
        "custom_attributes": {
            "attr1": "attr1-ffff",
            "attr2": "attr2"
        },
        "extra": "not_allowed"
    }

    try:
        Model(**dct2)
    except ValidationError as e:
        print(e)

    dct3 = {
        "name": 1,
        "addresses": [
            {"street": "street address", "city": "City"},
            {"street": "111", "postal": "111-1111"}
        ],
        "custom_attributes": {
            "attr1": "attr1-ffff",
            "attr": "attr2"
        }
    }

    try:
        Model(**dct3)
    except ValidationError as e:
        print(e)

        dct4 = {
            "name1": "tt",
            "addresses": [],
            "custom_attributes": {
                "attr1": "attr1-ffff",
                "attr2": 1
            }
        }

        try:
            Model(**dct4)
        except ValidationError as e:
            print(e)