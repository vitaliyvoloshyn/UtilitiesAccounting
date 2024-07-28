from typing import Type, List, Union, Sequence, Any

from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from models import Base, Category, Provider
from models.models import Unit, TariffType, Tariff, Counter, Indicator, TariffValue
from repositories.interface import AbstractRepository
from schemas import CategoryDTO, IndicatorDTO, TariffValueAddDTO, TariffDTO, TariffRelDTO, CategoryRelDTO


class SQLAlchemyRepository(AbstractRepository):
    model: Type[Base] = None
    dto: BaseModel = None
    rel_dto: BaseModel = None

    def __init__(self, session: Session):
        self.session = session

    def add_obj(self, dto: BaseModel) -> Base:
        dict_dto = dto.dict()
        model = self.model(**dict_dto)
        self.session.add(model)
        return model

    def get_obj(self,
                with_relation: bool = False,
                validate: bool = True,
                return_lst: bool = True,
                **filter_by
                ) -> Union[List[BaseModel], List[Base]]:
        query = select(self.model).filter_by(**filter_by)
        res = self.session.execute(query).scalars().all()
        if not res:
            raise ValueError(f'Категорії з id={filter_by["id"]} в базі не знайдено')
        if not return_lst:
            if len(res) > 1:
                raise ValueError('Знайдено більше одного результату')
            res = res[0]
        return self.model_validate(res, with_relation) if validate else res

    def update(self, pk: int, **data):
        stmt = update(self.model).filter_by(id=pk).values(**data)
        self.session.execute(stmt)

    def delete(self, pk: int):
        orm_model = self.session.execute(select(self.model).filter_by(id=pk)).scalar()
        self.session.delete(orm_model)

    def model_validate(self, orm: Union[Base, Sequence[Base]], with_relation: bool = False) \
            -> Union[BaseModel, List[BaseModel]]:
        dto = self.dto
        if with_relation:
            dto = self.rel_dto
        if isinstance(orm, (list, Sequence)):
            return [dto.model_validate(row, from_attributes=True) for row in orm]
        return dto.model_validate(orm, from_attributes=True)


class CategoryRepository(SQLAlchemyRepository):
    model = Category
    dto = CategoryDTO
    rel_dto = CategoryRelDTO


class ProviderRepository(SQLAlchemyRepository):
    model = Provider


class UnitRepository(SQLAlchemyRepository):
    model = Unit


class TariffTypeRepository(SQLAlchemyRepository):
    model = TariffType


class TariffRepository(SQLAlchemyRepository):
    model = Tariff
    dto = TariffDTO
    rel_dto = TariffRelDTO


class CounterRepository(SQLAlchemyRepository):
    model = Counter

    def add_obj(self, counter_dto: BaseModel, category: Base) -> Base:
        counter = self.model(**counter_dto.dict())
        counter.categories.append(category)
        self.session.add(counter)
        return counter


class IndicatorRepository(SQLAlchemyRepository):
    model = Indicator
    dto = IndicatorDTO


class TariffValueRepository(SQLAlchemyRepository):
    model = TariffValue
    dto = TariffValueAddDTO
