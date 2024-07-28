from abc import ABC, abstractmethod
from typing import List

from pydantic import BaseModel


class AbstractRepository(ABC):
    @abstractmethod
    def add_obj(self, *args, **kwargs) -> BaseModel:
        ...

    @abstractmethod
    def get_obj(self, *args, **kwargs) -> List[BaseModel]:
        ...

    @abstractmethod
    def update(self, *args, **kwargs) -> BaseModel:
        ...

    @abstractmethod
    def delete(self, *args, **kwargs):
        ...
