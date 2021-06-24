from typing import Union, List
from dataclasses import dataclass


@dataclass
class Gene:
    name: str
    labels: Union[List[str], None] = None
