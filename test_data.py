import datetime

from schemas import CategoryAddDTO, UnitAddDTO, ProviderAddDTO, TariffTypeAddDTO, TariffAddDTO, CounterAddDTO, \
    IndicatorAddDTO, TariffValueAddDTO
from services import CategoryService, UnitService, ProviderService, TariffTypeService, TariffService, CounterService, \
    IndicatorService, TariffValueService
from utils import TariffTypeValue, UnitType
from handlers import SubscriptionDefine, ConsumptionDefine

category_service = CategoryService([ConsumptionDefine(), SubscriptionDefine(), ])
unit_service = UnitService()
provider_service = ProviderService()
tt_service = TariffTypeService()
tariff_service = TariffService()
counter_service = CounterService()
indicator_service = IndicatorService()
tariff_value_service = TariffValueService()

category_water = CategoryAddDTO(name='Водопостачання')

provider_water = ProviderAddDTO(name='Українське ВКП', category_id=1, created_at=datetime.date(2024, 2, 10))

unit_kw = UnitAddDTO(value=UnitType.electricity)
unit_m = UnitAddDTO(value=UnitType.volume)

tt_sub = TariffTypeAddDTO(type=TariffTypeValue.subscription)
tt_con = TariffTypeAddDTO(type=TariffTypeValue.consumption)
tt_add = TariffTypeAddDTO(type=TariffTypeValue.additional)



counter_cold_water = CounterAddDTO(
    name='Лічильник холодної води',
    unit_id=2,
    category_id=1,
)
counter_hot_water = CounterAddDTO(
    name='Лічильник гарячої води',
    unit_id=2,
    category_id=1,
)

tariff_water_sub = TariffAddDTO(name='Абонплата',
                                provider_id=1,
                                tariff_type_id=2)
tariff_water_in_con = TariffAddDTO(name='Водопостачання',
                                   provider_id=1,
                                   tariff_type_id=3)

tariff_water_out_con = TariffAddDTO(name='Водовідведення',
                                   provider_id=1,
                                   tariff_type_id=3)
tariff_water_add = TariffAddDTO(name='Додаткові нарахування',
                                provider_id=1,
                                tariff_type_id=1)

indicator_cold_water_1 = IndicatorAddDTO(
    value=1198,
    counter_id=1,
)
indicator_cold_water_2 = IndicatorAddDTO(
    value=1210,
    counter_id=1,
)
indicator_hot_water_1 = IndicatorAddDTO(
    value=584,
    counter_id=2,
)
indicator_hot_water_2 = IndicatorAddDTO(
    value=586,
    counter_id=2,
)

tariff_value_water_sub = TariffValueAddDTO(
    value=19.10,
    tariff_id=1,
    start_date=datetime.date(2024, 2, 1),
)
tariff_value_water_in_con_1 = TariffValueAddDTO(
    value=37.52,
    tariff_id=2,
    start_date=datetime.date(2024, 2, 1),
)

tariff_value_water_out_con_1 = TariffValueAddDTO(
    value=41.10,
    tariff_id=3,
    start_date=datetime.date(2024, 5, 1),
)



def add_test_data():
    # print(f'Додано значення в таблицю Unit id = {unit_service.add(unit_m)}')
    unit_service.add(unit_kw)
    unit_service.add(unit_m)
    category_service.add(category_water)
    provider_service.add(provider_water)
    tt_service.add(tt_add)
    tt_service.add(tt_sub)
    tt_service.add(tt_con)
    tariff_service.add(tariff_water_sub)
    tariff_service.add(tariff_water_in_con)
    # tariff_service.add(tariff_water_in_con_1)
    tariff_service.add(tariff_water_out_con)
    # tariff_service.add(tariff_water_out_con_1)
    tariff_service.add(tariff_water_add)
    counter_service.add(counter_cold_water, 1)
    counter_service.add(counter_hot_water, 1)
    indicator_service.add(indicator_cold_water_1)
    indicator_service.add(indicator_cold_water_2)
    indicator_service.add(indicator_hot_water_1)
    indicator_service.add(indicator_hot_water_2)
    tariff_value_service.add(tariff_value_water_sub)
    tariff_value_service.add(tariff_value_water_in_con_1)
    # tariff_value_service.add(tariff_value_water_in_con_2)
    tariff_value_service.add(tariff_value_water_out_con_1)
    # tariff_value_service.add(tariff_value_water_out_con_2)
    category = category_service.get_one(with_relation=True, name='Водопостачання')
    print(category)
    for i in category_service.handlers:
        print(i.calc(category, datetime.date(2024, 5, 30)))
