from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, Enum, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    ...


class Category(Base):
    __tablename__ = 'categories'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    provider: Mapped['Provider'] = relationship(back_populates='category')
    counters: Mapped[List['Counter']] = relationship(back_populates='categories', secondary='category_counter',
                                                     lazy='selectin')


class Provider(Base):
    __tablename__ = 'providers'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime]
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    category: Mapped['Category'] = relationship(back_populates='provider', lazy='selectin')
    tariffs: Mapped[List['Tariff']] = relationship(back_populates='provider', lazy='selectin')


class Tariff(Base):
    __tablename__ = 'tariffs'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    provider_id: Mapped[int] = mapped_column(ForeignKey('providers.id'))
    tariff_type_id: Mapped[int] = mapped_column(ForeignKey('tariff_types.id'))
    # counter_id: Mapped[int] = mapped_column(ForeignKey('counters.id'), nullable=True)
    tariff_values: Mapped[List['TariffValue']] = relationship(back_populates='tariff', lazy='selectin')
    provider: Mapped['Provider'] = relationship(back_populates='tariffs', lazy='selectin')
    tariff_type: Mapped['TariffType'] = relationship(back_populates='tariffs', lazy='selectin')
    # counter: Mapped['Counter'] = relationship(back_populates='tariffs', lazy='selectin')


class TariffValue(Base):
    __tablename__ = 'tariff_values'
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[float]
    start_date: Mapped[datetime]
    end_date: Mapped[datetime] = mapped_column(nullable=True)
    tariff_id: Mapped[int] = mapped_column(ForeignKey('tariffs.id'))
    tariff: Mapped['Tariff'] = relationship(back_populates='tariff_values', lazy='selectin')


class TariffType(Base):
    __tablename__ = 'tariff_types'
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(unique=True)
    tariffs: Mapped[List['Tariff']] = relationship(back_populates='tariff_type', lazy='selectin')


class Counter(Base):
    __tablename__ = 'counters'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    unit_id: Mapped[int] = mapped_column(ForeignKey('units.id'))
    categories: Mapped[List['Category']] = relationship(back_populates='counters', secondary='category_counter',
                                                        lazy='selectin')
    indicators: Mapped[List['Indicator']] = relationship(back_populates='counter', lazy='selectin')
    unit: Mapped['Unit'] = relationship(back_populates='counters', lazy='selectin')
    # tariffs: Mapped[List['Tariff']] = relationship(back_populates='counter', lazy='selectin')


class CategoryCounter(Base):
    __tablename__ = 'category_counter'
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'), primary_key=True)
    counter_id: Mapped[int] = mapped_column(ForeignKey('counters.id'), primary_key=True)


class Indicator(Base):
    __tablename__ = 'indicators'
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[int]
    date: Mapped[datetime] = mapped_column(server_default=func.current_date())
    counter_id: Mapped[int] = mapped_column(ForeignKey('counters.id'))
    counter: Mapped['Counter'] = relationship(back_populates='indicators', lazy='selectin')


class Unit(Base):
    __tablename__ = 'units'
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str] = mapped_column(unique=True)
    counters: Mapped[List['Counter']] = relationship(back_populates='unit', lazy='selectin')

    def __repr__(self):
        return f'<Unit(id={self.value})>'
