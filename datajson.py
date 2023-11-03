import dataclasses
from io import StringIO
import json
from typing import Any, TextIO, TypeVar, get_args, get_origin
 
 
__all__ = ["encode", "encode_to_string", "decode", "decode_from_string"]
 
T = TypeVar("T")
 
def decode(cls: type[T], io: TextIO) -> T:
    def decode_type_value(cls: type, value: Any) -> Any:
        if cls == int or cls == bool or cls == float or cls == str:
            if not isinstance(value, cls):
                value_json = json.dumps(value)
                raise ValueError(f"Cannot deserialize {cls.__name__} from {value_json}")
 
            return value
        
        if cls == Any:
            return value
 
        if get_origin(cls) == list and len(get_args(cls)) == 1:
            list_type = get_args(cls)[0]
            list_values = []
 
            if not isinstance(value, list):
                value_json = json.dumps(value)
                raise ValueError(f"Cannot deserialize List[{list_type}] from {value_json}")
 
            for entry in value:
                list_values.append(decode_type_value(list_type, entry))
 
            return list_values
 
        if get_origin(cls) == dict and len(get_args(cls)) == 2:
            dict_key_type = get_args(cls)[0]
            dict_value_type = get_args(cls)[1]
            dict_values = {}
 
            if not isinstance(value, dict):
                value_json = json.dumps(value)
                raise ValueError(f"Cannot deserialize Dict[{dict_key_type}, {dict_value_type}] from {value_json}")
 
            for item_key, item_value in value.items():
                dict_key = decode_type_value(dict_key_type, item_key)
                dict_value = decode_type_value(dict_value_type, item_value)
 
                dict_values[dict_key] = dict_value
 
            return dict_values
 
        if dataclasses.is_dataclass(cls):
            field_values = {}
 
            if not isinstance(value, dict):
                raise ValueError(f"Cannot deserialize dataclass {cls.__name__} from a non-object!")
 
            for field_name, field in cls.__dataclass_fields__.items():
                raw_value = value.get(field_name)
                field_values[field_name] = decode_type_value(field.type, raw_value)
 
            return cls(**field_values)
 
        raise TypeError(f"Cannot deserialize attribute: {cls.__name__}")
 
    values = json.load(io)
    return decode_type_value(cls, values)
 
def decode_from_string(cls: type[T], data: str) -> T:
    io = StringIO(data)
    return decode(cls, io)
 
def encode(data: Any, io: TextIO):
    def default(data: Any) -> Any:
        if dataclasses.is_dataclass(data):
            return data.__dict__
 
        raise TypeError("Can't encode something that is not a dataclass!")
 
    json.dump(data, io, default=default)
 
def encode_to_string(data: Any) -> str:
    io = StringIO()
    encode(data, io)
    return io.getvalue()
    