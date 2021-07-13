"""Initialise the cell models module"""
import enum
from typing import Union

from .minimal_model.model import MinimalModel

class CellModels(enum.Enum):
    """Factory to obtain cell models."""
    MINIMAL_MODEL = MinimalModel

    @classmethod
    def valid_models(cls):
        return cls._member_names_