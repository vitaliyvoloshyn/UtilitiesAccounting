from abc import ABC, abstractmethod
from datetime import date, datetime
from decimal import Decimal
from types import NoneType
from typing import List, Optional, Type

from dateutil.relativedelta import relativedelta
from pydantic import BaseModel

from schemas import TariffRelDTO, CategoryRelDTO, TariffValueDTO, IndicatorDTO, Subscription, CalculationFee
from utils import TariffTypeValue


class IHandler(ABC):
    TARIFF_TYPE: TariffTypeValue = ''
    DTO_MODEL: Type[CalculationFee]

    @abstractmethod
    def calc(self, *args):
        pass

    @staticmethod
    def _first_day_of_month(date_: datetime
                            ) -> datetime:
        """Повертає перший день місяця переданої дати"""
        return datetime(date_.year, date_.month, 1)

    def tariff_define(self, tariffs: List[TariffRelDTO]) -> list[TariffRelDTO]:
        """Повертає обєкт TariffRelDTO з категорії"""
        res = [tariff_ for tariff_ in tariffs if tariff_.tariff_type.type == self.TARIFF_TYPE]
        if res:
            return res
        raise ValueError('tariff define error')

    def _date_from(self,
                   date_from: datetime,
                   provider_create: datetime,
                   ) -> datetime:
        """Порівнює дату створення провайдера і дату початку відліку"""
        provider_create = self._first_day_of_month(provider_create)
        if not date_from:
            return provider_create
        date_from = self._first_day_of_month(date_from)
        return date_from if date_from > provider_create else provider_create

    def calculate_accruals(self,
                           category: CategoryRelDTO,
                           date_from: Optional[datetime] = None
                           ) -> CalculationFee:
        sub = self.calc(category, date_from)
        add = self.calc()


class SubscriptionDefine(IHandler):
    TARIFF_TYPE = TariffTypeValue.subscription
    DTO_SUB_MODEL = Subscription

    def calc(self,
             category: CategoryRelDTO,
             date_from: Optional[datetime] = None,
             ) -> Decimal:
        """Знаходить повну суму по абонплаті за період з дати створення оператора послуг до минулого місяця від
        поточної дати
        на вхід приймає дату, з якої починати відлік і обєкт CategoryRelDTO"""
        check_date = self._date_from(date_from, category.provider.created_at)
        date_to = self._first_day_of_month(datetime.today())
        total_fee = Decimal('0')
        try:
            check_tariff = self.tariff_define(category.provider.tariffs)
        except ValueError:
            return total_fee
        while check_date < date_to:
            cur_value = 0
            for tariff in check_tariff:
                for tv in tariff.tariff_values:
                    cur_value = tv.value
                    try:
                        if tv.start_date <= check_date <= tv.end_date:
                            break
                    except TypeError:
                        ...
            total_fee += Decimal(str(cur_value))
            check_date += relativedelta(months=1)
        return total_fee


class AdditionalDefine(IHandler):
    TARIFF_TYPE = TariffTypeValue.additional

    def calc(self,
             category: CategoryRelDTO,
             date_from: Optional[datetime] = None,
             ) -> Decimal:
        """Знаходить повну суму по додаткавим нарахуванням за період з дати створення оператора послуг до минулого
        місяця від поточної дати на вхід приймає дату, з якої починати відлік і обєкт CategoryRelDTO"""
        total: Decimal = Decimal('0')
        try:
            tariffs = self.tariff_define(category.provider.tariffs)
        except ValueError:
            return total
        for tariff in tariffs:
            for tv in tariff.tariff_values:
                total += Decimal(str(tv.value))
        return total


class ConsumptionDefine(IHandler):
    TARIFF_TYPE = TariffTypeValue.consumption

    def calc(self,
             category: CategoryRelDTO,
             date_from: Optional[datetime] = None,
             ) -> Decimal:
        total_fee = Decimal('0')

        try:
            check_tariff = self.tariff_define(category.provider.tariffs)
        except ValueError:
            return total_fee

        for counter in category.counters:
            for diff in self.get_diff_indicator(counter.indicators):
                cur_value = 0
                for tariff in check_tariff:
                    for tv in tariff.tariff_values:
                        cur_value = tv.value
                        try:
                            if tv.start_date <= diff.date <= tv.end_date:
                                break
                        except TypeError:
                            ...
                    total_fee += (Decimal(str(cur_value)) * Decimal(str(diff.value)))
        return total_fee

    @staticmethod
    def get_diff_indicator(ind: list[IndicatorDTO]):
        if not ind or len(ind) == 1:
            raise ValueError
        for i in range(1, len(ind)):
            diff = ind[i] - ind[i - 1]
            yield diff
