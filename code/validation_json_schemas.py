# TODO validate type is in valid set of values for all below

fv_schema = {
    "type": "object",
    "properties": {
        "rate": {
            "type": "number"
        },
        "nper": {
            "type": "number"
        },
        "pmt": {
            "type": "number"
        },
        "pv": {
            "type": "number"
        },
        "type": {
            "type": "integer",
            "enum": [0, 1]
        }
    },
    "anyOf": [
        {
            "required": ["rate", "nper", "pmt"]
        },
        {
            "required": ["rate", "nper", "pv"]
        }
    ],
    "additionalProperties": False
}

pv_schema = {
    "type": "object",
    "properties": {
        "rate": {
            "type": "number"
        },
        "nper": {
            "type": "number"
        },
        "pmt": {
            "type": "number"
        },
        "fv": {
            "type": "number"
        },
        "type": {
            "type": "integer",
            "enum": [0, 1]
        }
    },
    "anyOf": [
        {
            "required": ["rate", "nper", "pmt"]
        },
        {
            "required": ["rate", "nper", "fv"]
        }
    ],
    "additionalProperties": False
}

npv_schema = {
    "type": "object",
    "properties": {
        "rate": {
            "type": "number"
        },
        "values": {
            "type": "array",
            "items": {
                "type": "number",
                "minItems": 1
            }
        }
    },
    "required": ["rate", "values"],
    "additionalProperties": False
}

pmt_schema = {
    "type": "object",
    "properties": {
        "rate": {
            "type": "number"
        },
        "nper": {
            "type": "number"
        },
        "pv": {
            "type": "number"
        },
        "fv": {
            "type": "number"
        },
        "type": {
            "type": "integer",
            "enum": [0, 1]
        }
    },
    "required": ["rate", "nper", "pv"],
    "additionalProperties": False
}

ppmt_schema = {
    "type": "object",
    "properties": {
        "rate": {
            "type": "number"
        },
        "per": {
            "type": "number",
            "minimum": 1
        },
        "nper": {
            "type": "number"
        },
        "pv": {
            "type": "number"
        },
        "fv": {
            "type": "number"
        },
        "type": {
            "type": "integer",
            "enum": [0, 1]
        }
    },
    "required": ["rate", "per", "nper", "pv"],
    "additionalProperties": False
}

irr_schema = {
    "type": "object",
    "properties": {
        "values": {
            "type": "array",
            "items": {
                "type": "number"
            },
            "minItems": 2
        }
    },
    "required": ["values"],
    "additionalProperties": False
}

mirr_schema = {
    "type": "object",
    "properties": {
        "values": {
            "type": "array",
            "items": {
                "type": "number"
            },
            "minItems": 2
        },
        "finance_rate": {
            "type": "number"
        },
        "reinvest_rate": {
            "type": "number"
        }
    },
    "required": ["values", "finance_rate", "reinvest_rate"],
    "additionalProperties": False
}

nper_schema = {
    "type": "object",
    "properties": {
        "rate": {
            "type": "number"
        },
        "pmt": {
            "type": "number"
        },
        "pv": {
            "type": "number"
        },
        "fv": {
            "type": "number"
        },
        "type": {
            "type": "integer",
            "enum": [0, 1]
        }
    },
    "anyOf": [
        {
            "required": ["rate", "pmt", "pv"]
        },
        {
            "required": ["rate", "pv", "fv"]
        }
    ],
    "additionalProperties": False
}

rate_schema = {
    "type": "object",
    "properties": {
        "nper": {
            "type": "number"
        },
        "pmt": {
            "type": "number"
        },
        "pv": {
            "type": "number"
        },
        "fv": {
            "type": "number"
        },
        "type": {
            "type": "integer",
            "enum": [0, 1]
        },
        "guess": {
            "type": "number"
        }
    },
    "anyOf": [
        {
            "required": ["nper", "pmt", "pv"]
        },
        {
            "required": ["nper", "pv", "fv"]
        }
    ],
    "additionalProperties": False
}
