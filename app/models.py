"""
models.py

Краткое описание моделей:
- Operator: Оператор, выполняющий контакты.
- Lead: Лид с уникальным внешним идентификатором.
- Source: Источник контактов.
- SourceOperatorWeight: Вес оператора для конкретного источника.
- Contact: Контакт, связанный с лидом, источником и оператором.
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Operator(Base):
    """
    Модель оператора.
    - id: PK
    - name: имя оператора
    - active: активен ли оператор
    - load_limit: максимальная нагрузка оператора
    """
    __tablename__ = "operators"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    active = Column(Boolean, default=True)
    load_limit = Column(Integer, default=5)

    assignments = relationship("SourceOperatorWeight", back_populates="operator")
    contacts = relationship("Contact", back_populates="operator")


class Lead(Base):
    """
    Модель лида.
    - id: PK
    - external_id: уникальный внешний идентификатор
    """
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True)
    external_id = Column(String, unique=True, index=True, nullable=False)

    contacts = relationship("Contact", back_populates="lead")


class Source(Base):
    """
    - id: PK
    - name: имя источника
    """
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    assignments = relationship("SourceOperatorWeight", back_populates="source")
    contacts = relationship("Contact", back_populates="source")


class SourceOperatorWeight(Base):
    """
    Модель веса оператора для источника.
    - id: PK
    - source_id: FK на источник
    - operator_id: FK на оператора
    - weight: вес оператора для данного источника
    """
    __tablename__ = "source_operator_weights"

    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=False)
    operator_id = Column(Integer, ForeignKey("operators.id"), nullable=False)
    weight = Column(Integer, nullable=False)

    source = relationship("Source", back_populates="assignments")
    operator = relationship("Operator", back_populates="assignments")


class Contact(Base):
    """
    - id: PK
    - lead_id: FK на лид
    - source_id: FK на источник
    - operator_id: FK на оператора (nullable)
    - text: текст контакта (nullable)
    """
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=False)
    operator_id = Column(Integer, ForeignKey("operators.id"), nullable=True)
    text = Column(String, nullable=True)

    lead = relationship("Lead", back_populates="contacts")
    source = relationship("Source", back_populates="contacts")
    operator = relationship("Operator", back_populates="contacts")