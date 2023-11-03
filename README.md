# Python DataJson Library

## Example Usage

```PYTHON
from dataclasses import dataclass
from typing import List
import datajson

@dataclass
class Author:
    first_name: str
    last_name: str
    age: int

@dataclass
class Project:
    name: str
    is_cool: bool
    authors: List[Author]

my_project = Project("DataJson", True, [Author("Rodney", "McKay", 34)])
assert datajson.encode_to_string(my_project) == '{"name": "DataJson", "is_cool": true, "authors": [{"first_name": "Rodney", "last_name": "McKay", "age": 34}]}'

a_project = datajson.decode_from_string(Project, '{"name": "DataJson", "is_cool": true, "authors": [{"first_name": "Rodney", "last_name": "McKay", "age": 34}]}')
assert a_project == my_project
```

## Why this lbirary exists.

This library arose from myself having a very complex structure of dataclasses that I wanted to easily (de-)serialize to/from json. When I realized that the python `json` module doens't natively support encoding dataclasses, I tried various approaches to solve this problem. I first experimented with using [dataclasses-json](https://github.com/lidatong/dataclasses-json), a really cool library that basically does exactly what I need. When trying to use that library however, I found out that it is not possible to type-check methods that were added by class decorators in python at the moment, until [intersection types](https://github.com/python/typing/issues/213) are added. So I set out to write my own, simple library that mimics the semantics of the json module, except for introducing more tight type-checking. I wanted to keep things simple, so this library only consists of one file with very little code in it. It was created to solve a very specific problem and I figured I'd share it in case anybody needs it. However, I don't really have any plans to develop this library any further.
