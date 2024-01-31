import datetime

from sqlalchemy import String, Integer, Column, Float, DateTime, UUID
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    def __getitem__(self, field):
        return self.__dict__[field]

    def __setitem__(self, key, value):
        return self.__setattr__(key, value)

    pass


class DOI(Base):
    __tablename__ = "doi"
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str] = mapped_column(String(1000), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"DOI(id={self.id}, value={self.value})"


class Ocean(Base):
    __tablename__ = "ocean"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"Ocean(id={self.id}, name={self.name})"


class Unit(Base):
    __tablename__ = "unit"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"Unit(id={self.id}, name={self.name})"


class SampleMethod(Base):
    __tablename__ = "sample_method"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"SampleMethod(id={self.id}, name={self.name})"


class Region(Base):
    __tablename__ = "region"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"Region(id={self.id}, name={self.name})"


class Subregion(Base):
    __tablename__ = "subregion"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"Subregion(id={self.id}, name={self.name})"


class Organization(Base):
    __tablename__ = "organization"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"Organization(id={self.id}, name={self.name})"


class Reference(Base):
    __tablename__ = "reference"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(1000), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"Reference(id={self.id}, title={self.title})"


class Measurement(Base):
    __tablename__ = "measurement"
    id = Column(Integer, primary_key=True)
    longitude = Column("longitude", Float, nullable=False)
    latitude = Column("latitude", Float, nullable=False)
    date = Column("date", DateTime(timezone=True))
    value = Column("value", Float, nullable=False)
    density_min = Column("density_min", Float)
    density_max = Column("density_max", Float)
    global_id = Column("global_id", String(30))
    access_link = Column("access_link", String(1024))
    ocean = Column("ocean", Integer)
    doi = Column("doi", Integer)
    unit = Column("unit", Integer)
    sample_method = Column("sample_method", Integer)
    region = Column("region", Integer)
    subregion = Column("subregion", Integer)
    organization = Column("organization", Integer)
    reference = Column("reference", Integer)

    def __repr__(self) -> str:
        return (f"Measurement(id={self.id}, "
                f"longitude={self.longitude}, "
                f"latitude={self.latitude}, "
                f"date={self.date}, "
                f"value={self.value}, "
                f"density_min={self.density_min}, "
                f"density_max={self.density_max}, "
                f"global_id={self.global_id}, "
                f"access_link={self.access_link}, "
                f"doi={self.doi}, "
                f"ocean={self.ocean}, "
                f"unit={self.unit}, "
                f"sample_method={self.sample_method}, "
                f"region={self.region}, "
                f"subregion={self.subregion}, "
                f"organization={self.organization}, "
                f"reference={self.reference})")
