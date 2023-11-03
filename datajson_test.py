from dataclasses import dataclass
from typing import Any, Dict, List
import unittest
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
    metadata: Dict[str, Any]

class FullTest(unittest.TestCase):
    def setUp(self):
        self.my_project = Project("DataJson", True, [Author("Rodney", "McKay", 34)], {"type_safe": True, "well_tested": "meh"})
        self.expected_json = '{"name": "DataJson", "is_cool": true, "authors": [{"first_name": "Rodney", "last_name": "McKay", "age": 34}], "metadata": {"type_safe": true, "well_tested": "meh"}}'
    
    def test_encoding(self):
        json_string = datajson.encode_to_string(self.my_project)
        self.assertEqual(json_string, self.expected_json)
        
    def test_decoding(self):
        decoded_project = datajson.decode_from_string(Project, self.expected_json)
        self.assertEqual(decoded_project, self.my_project)

if __name__ == '__main__':
    unittest.main()
