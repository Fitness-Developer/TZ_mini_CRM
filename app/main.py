"""
main.py

mini crm для управления операторами, источниками, контактами и лидами.
"""
from fastapi import FastAPI, HTTPException
from typing import List
from .database import Base, engine, SessionLocal
from .schemas import OperatorCreate, SourceCreate, WeightCreate, ContactCreate
from .models import Operator, Source, SourceOperatorWeight, Lead, Contact
from .utils import choose_operator

# Создаем все таблицы в базе данных
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mini-CRM", description="API для работы с лидами, контактами и операторами", version="1.0")

# ==========================
# Операторы
# ==========================

@app.post("/operators", summary="Создать нового оператора")
def create_operator(data: OperatorCreate):
    db = SessionLocal()
    op = Operator(name=data.name, active=data.active, load_limit=data.load_limit)
    db.add(op)
    db.commit()
    db.refresh(op)
    return op


@app.get("/operators", summary="Получить список всех операторов")
def list_operators():
    db = SessionLocal()
    return db.query(Operator).all()

@app.patch("/operators/{operator_id}", summary="Обновить оператора")
def update_operator(operator_id: int, data: OperatorCreate):
    """
    Обновляет активность и лимит нагрузки оператора.
    """
    db = SessionLocal()
    operator = db.query(Operator).filter_by(id=operator_id).first()
    if not operator:
        raise HTTPException(status_code=404, detail="Operator not found")
    operator.name = data.name
    operator.active = data.active
    operator.load_limit = data.load_limit
    db.commit()
    db.refresh(operator)
    return operator

# ==========================
# Источники
# ==========================

@app.post("/sources", summary="Создать новый источник")
def create_source(data: SourceCreate):
    db = SessionLocal()
    s = Source(name=data.name)
    db.add(s)
    db.commit()
    db.refresh(s)
    return s


@app.post("/sources/{source_id}/weights", summary="Назначить веса операторам для источника")
def assign_weights(source_id: int, weights: List[WeightCreate]):

    db = SessionLocal()
    for w in weights:
        db.add(SourceOperatorWeight(source_id=source_id, operator_id=w.operator_id, weight=w.weight))
    db.commit()
    return {"status": "ok"}

@app.patch("/sources/{source_id}/weights/{operator_id}", summary="Обновить вес оператора для источника")
def update_weight(source_id: int, operator_id: int, weight: int):
    db = SessionLocal()
    assignment = db.query(SourceOperatorWeight).filter_by(source_id=source_id, operator_id=operator_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Weight assignment not found")
    assignment.weight = weight
    db.commit()
    db.refresh(assignment)
    return assignment


@app.delete("/sources/{source_id}/weights/{operator_id}", summary="Удалить вес оператора для источника")
def delete_weight(source_id: int, operator_id: int):
    db = SessionLocal()
    assignment = db.query(SourceOperatorWeight).filter_by(source_id=source_id, operator_id=operator_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Weight assignment not found")
    db.delete(assignment)
    db.commit()
    return {"status": "deleted"}

# ==========================
# Контакты и лиды
# ==========================

@app.post("/contacts", summary="Создать контакт")
def create_contact(data: ContactCreate):
    """
    Создает контакт и автоматически назначает оператора на основе весов.
    Если лид с указанным external_id не найден, создается новый.
    """
    db = SessionLocal()

    # Поиск лида по внешнему ID
    lead = db.query(Lead).filter_by(external_id=data.external_id).first()
    if not lead:
        lead = Lead(external_id=data.external_id)
        db.add(lead)
        db.commit()
        db.refresh(lead)

    # Выбор оператора на основе весов
    operator = choose_operator(db, data.source_id)

    contact = Contact(
        lead_id=lead.id,
        source_id=data.source_id,
        operator_id=operator.id if operator else None,
        text=data.text,
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)

    return {
        "contact_id": contact.id,
        "operator": operator.name if operator else None,
        "lead_id": lead.id,
    }


@app.get("/leads", summary="Получить список всех лидов")
def list_leads():
    db = SessionLocal()
    return db.query(Lead).all()


@app.get("/contacts", summary="Получить список всех контактов")
def list_contacts():
    db = SessionLocal()
    return db.query(Contact).all()


# ==========================
# Отчёты
# ==========================

@app.get("/reports", summary="Отчёт по распределению контактов")
def contacts_report():
    """
    Возвращает количество контактов по операторам и источникам.
    """
    db = SessionLocal()
    report = []
    contacts = db.query(Contact).all()
    for contact in contacts:
        report.append({
            "contact_id": contact.id,
            "lead_id": contact.lead_id,
            "source": contact.source.name if contact.source else None,
            "operator": contact.operator.name if contact.operator else None
        })
    return report