from datetime import date, datetime
from decimal import Decimal, getcontext, ROUND_HALF_UP, ROUND_UP
from typing import List, Optional

from dateutil.relativedelta import relativedelta
from dateutil.parser import parser
from pydantic import BaseModel

from dependencies import UOWDep
from handlers import IHandler
from models.models import TariffValue
from schemas import TariffValueAddDTO, TariffRelDTO, CategoryRelDTO
from unitofwork import UnitOfWork
from utils import prev_date


class IService:
    repo: str
    handlers: List['IHandler']

    def add(self, dto: BaseModel, *args, uow: UnitOfWork = UOWDep) -> int:
        with uow:
            cur_repo = uow.__getattribute__(self.repo)
            model_id = cur_repo.add_obj(dto)
            uow.commit()
            return model_id

    def get_all(self,
                uow: UnitOfWork = UOWDep,
                validate: bool = True,
                with_relation: bool = False,
                **filter_by
                ):
        with uow:
            cur_repo = uow.__getattribute__(self.repo)
            return cur_repo.get_obj(with_relation=with_relation, validate=validate, **filter_by)

    def get_one(self,
                uow: UnitOfWork = UOWDep,
                validate: bool = True,
                with_relation: bool = False,
                **filter_by
                ):
        with uow:
            cur_repo = uow.__getattribute__(self.repo)
            return cur_repo.get_obj(with_relation=with_relation, validate=validate, return_lst=False, **filter_by)


class CategoryService(IService):
    repo = 'category'

    def __init__(self, handlers: List['IHandler']):
        self.handlers = handlers

    def calculate_accruals(self,
                           category: CategoryRelDTO,
                           date_from: Optional[datetime] = None
                           ):
        l = []
        for handler in self.handlers:
            handler.DTO_MODEL
            l.append(handler.calc(category, date_from))
        res = handler.DTO_MODEL()


class ProviderService(IService):
    repo = 'provider'


class UnitService(IService):
    repo = 'unit'


class TariffTypeService(IService):
    repo = 'tariff_type'


class TariffService(IService):
    repo = 'tariff'


class CounterService(IService):
    repo = 'counter'

    def add(self, dto: BaseModel, category_id: int, uow: UnitOfWork = UOWDep) -> int:
        with uow:
            cur_repo = uow.__getattribute__(self.repo)
            category = uow.category.get_obj(validate=False, return_lst=False, id=category_id)
            model = cur_repo.add_obj(dto, category)
            uow.commit()
            return model


class IndicatorService(IService):
    repo = 'indicator'


class TariffValueService(IService):
    repo = 'tariff_value'

    def change_value(self, tv: TariffValueAddDTO, uow: UnitOfWork = UOWDep) -> int:
        with uow:
            try:
                cur_tv: TariffValue = uow.tariff_value.get_obj(validate=False, tariff_id=tv.tariff_id)[-1]
            except IndexError:
                raise ValueError('Категорії з таким id не знайдено в базі')

            cur_tv.end_date = prev_date(tv.start_date)
            uow.tariff_value.add_obj(tv)
            uow.commit()
