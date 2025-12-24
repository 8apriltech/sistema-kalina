from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from datetime import datetime, date

from database import SessionLocal
from models import RetiradaMensal
from schemas import DefinirDataRequest

router = APIRouter(prefix="/retiradas", tags=["Retiradas"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/definir-data")
def definir_data_prevista(
    payload: DefinirDataRequest = Body(...),
    db: Session = Depends(get_db)
):
    try:
        data_prevista = datetime.strptime(
            payload.data_prevista, "%Y-%m-%d"
        ).date()
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Formato de data inválido. Use YYYY-MM-DD."
        )

    retirada = (
        db.query(RetiradaMensal)
        .filter(
            RetiradaMensal.paciente_id == payload.paciente_id,
            RetiradaMensal.ano == payload.ano,
            RetiradaMensal.mes == payload.mes
        )
        .first()
    )

    if retirada:
        retirada.data_prevista = data_prevista
    else:
        retirada = RetiradaMensal(
            paciente_id=payload.paciente_id,
            ano=payload.ano,
            mes=payload.mes,
            data_prevista=data_prevista
        )
        db.add(retirada)

    db.commit()
    return {"status": "ok"}


@router.put("/{retirada_id}/marcar")
def marcar_retirada(
    retirada_id: int,
    db: Session = Depends(get_db)
):
    retirada = (
        db.query(RetiradaMensal)
        .filter(RetiradaMensal.id == retirada_id)
        .first()
    )

    if not retirada:
        raise HTTPException(
            status_code=404,
            detail="Retirada não encontrada"
        )

    retirada.data_retirada = date.today()
    db.commit()

    return {"status": "ok"}