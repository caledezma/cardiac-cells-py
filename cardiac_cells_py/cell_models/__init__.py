"""Initialise the cell models module"""
import enum

from .minimal_model.model import MinimalModel

class CellModels(enum.Enum):
    """Factory to obtain cell models."""
    MINIMAL_MODEL = MinimalModel