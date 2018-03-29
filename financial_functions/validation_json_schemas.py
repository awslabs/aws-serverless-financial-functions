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

fvschedule_schema = {
    "type": "object",
    "properties": {
        "principal": {
            "type": "number"
        },
        "schedule": {
            "type": "array",
            "items": {
                "type": "number"
            }
        }
    },
    "required": ["principal", "schedule"],
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

xnpv_schema = {
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
        },
        "dates": {
            "type": "array",
            "items": {
                "type": "string",
                "minItems": 1,
                "pattern": "^[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}$"
            }
        }
    },
    "required": ["rate", "values", "dates"],
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

xirr_schema = {
    "type": "object",
    "properties": {
        "values": {
            "type": "array",
            "items": {
                "type": "number"
            },
            "minItems": 2
        },
        "dates": {
            "type": "array",
            "items": {
                "type": "string",
                "minItems": 2,
                "pattern": "^[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}$"
            }
        },
        "guess": {
            "type": "number"
        }
    },
    "required": ["values", "dates"],
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

effect_schema = {
    "type": "object",
    "properties": {
        "nominal_rate": {
            "type": "number"
        },
        "npery": {
            "type": "number",
            "minimum": 1
        }
    },
    "required": ["nominal_rate", "npery"],
    "additionalProperties": False
}

nominal_schema = {
    "type": "object",
    "properties": {
        "effect_rate": {
            "type": "number"
        },
        "npery": {
            "type": "number",
            "minimum": 1
        }
    },
    "required": ["effect_rate", "npery"],
    "additionalProperties": False
}

sln_schema = {
    "type": "object",
    "properties": {
        "cost": {
            "type": "number"
        },
        "salvage": {
            "type": "number"
        },
        "life": {
            "type": "number"
        }
    },
    "required": ["cost", "salvage", "life"],
    "additionalProperties": False
}

wrapper_schema = {
    "type": "object",
    "properties": {
        "function_name": {
            "type": "string"
        },
        "args": {
            "type": "object"
        }
    },
    "required": ["function_name", "args"],
    "additionalProperties": False
}
