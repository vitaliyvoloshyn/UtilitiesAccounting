from dataclasses import dataclass
from datetime import date, timedelta


@dataclass
class TariffTypeValue:
    subscription: str = 'Щомісячний платіж'
    additional: str = 'Додаткові нарахування'
    consumption: str = "За спожитий об'єм"


@dataclass
class UnitType:
    volume: str = 'м3'
    electricity: str = 'кВт*год'


def prev_date(date_: date) -> date:
    return date_ - timedelta(days=1)


if __name__ == '__main__':
    print(TariffTypeValue.subscription)
