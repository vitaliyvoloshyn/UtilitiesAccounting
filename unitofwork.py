from abc import ABC, abstractmethod

from db.database import db_session_maker
from repositories.SQLAlchemyRepository import SQLAlchemyRepository, CategoryRepository, ProviderRepository, \
    UnitRepository, TariffTypeRepository, TariffRepository, CounterRepository, IndicatorRepository, \
    TariffValueRepository


class IUnitOfWork(ABC):

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    def __enter__(self):
        ...

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        ...

    @abstractmethod
    def commit(self):
        ...

    @abstractmethod
    def rollback(self):
        ...


class UnitOfWork(IUnitOfWork):

    def __init__(self):
        self.session_factory = db_session_maker

    def __enter__(self):
        self.session = self.session_factory()
        self.category: SQLAlchemyRepository = CategoryRepository(self.session)
        self.provider: SQLAlchemyRepository = ProviderRepository(self.session)
        self.unit: SQLAlchemyRepository = UnitRepository(self.session)
        self.tariff_type: SQLAlchemyRepository = TariffTypeRepository(self.session)
        self.tariff: SQLAlchemyRepository = TariffRepository(self.session)
        self.counter: SQLAlchemyRepository = CounterRepository(self.session)
        self.indicator: SQLAlchemyRepository = IndicatorRepository(self.session)
        self.tariff_value: SQLAlchemyRepository = TariffValueRepository(self.session)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.rollback()
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
