from datetime import datetime
from typing import Optional, List, Self, Union

from pydantic import BaseModel


# _________________________________Category______________________________________
class CategoryAddDTO(BaseModel):
    name: str


class CategoryDTO(CategoryAddDTO):
    id: int


class CategoryRelDTO(CategoryDTO):
    provider: 'ProviderRelDTO'
    counters: List['CounterRelDTO']


# _________________________________ Provider ______________________________________
class ProviderAddDTO(BaseModel):
    name: str
    category_id: int
    created_at: datetime


class ProviderDTO(ProviderAddDTO):
    id: int


class ProviderRelDTO(ProviderDTO):
    category: 'CategoryDTO'
    tariffs: List['TariffRelDTO']


# _________________________________ Unit ______________________________________
class UnitAddDTO(BaseModel):
    value: str


class UnitDTO(BaseModel):
    id: int


# _________________________________ TariffType ______________________________________
class TariffTypeAddDTO(BaseModel):
    type: str


class TariffTypeDTO(TariffTypeAddDTO):
    id: int


# _________________________________ Tariff ______________________________________
class TariffAddDTO(BaseModel):
    name: str
    provider_id: int
    tariff_type_id: int
    # counter_id: Optional[int] = None


class TariffDTO(TariffAddDTO):
    id: int


class TariffRelDTO(TariffDTO):
    tariff_type: 'TariffTypeDTO'
    tariff_values: List['TariffValueDTO']
    # provider: 'ProviderDTO'


# _________________________________ Tariff ______________________________________
class CounterAddDTO(BaseModel):
    name: str
    unit_id: int


class CounterDTO(CounterAddDTO):
    id: int


class CounterRelDTO(CounterDTO):
    unit: 'UnitDTO'
    indicators: List['IndicatorDTO']


# _________________________________ Indicator ______________________________________
class IndicatorAddDTO(BaseModel):
    value: int
    date: Optional[datetime] = None
    counter_id: int


class IndicatorDTO(IndicatorAddDTO):
    id: int

    def __sub__(self, other: 'IndicatorDTO'):
        diff = self.value - other.value
        out_obj = self.model_copy()
        out_obj.value = diff
        return out_obj


# _________________________________ TariffValue ______________________________________
class TariffValueAddDTO(BaseModel):
    value: float
    tariff_id: int
    start_date: datetime
    end_date: Optional[datetime] = None


class TariffValueDTO(TariffValueAddDTO):
    id: int


# ___________________________________XXXXXX_____________________________________________
class CalculationFee(BaseModel):
    category: 'CategoryDTO'
    provider: 'ProviderDTO'
    # counters: List['CalculationCounter']
    accruals: List[Union['Consumption', 'Subscription', 'Additional']]
    # consumption: 'Consumption'
    # subscription: 'Subscription'
    # additional: 'Additional'


# class CalculationCounter(BaseModel):
#     counter: CounterDTO
#     unit: UnitDTO
#     consumption: str


class Subscription(BaseModel):
    tariff: 'TariffCalc'
    sum: str


class Consumption(BaseModel):
    tariff: 'TariffCalc'
    sum: str
    cons_volume: int
    counter_name: str
    unit: str


class Additional(BaseModel):
    tariff: 'TariffCalc'
    sum: str


class TariffCalc(BaseModel):
    name: str
    value: str
    type: 'TariffTypeDTO'
