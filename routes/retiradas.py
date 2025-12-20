from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from database import SessionLocal
from models import RetiradaMensal

router = APIRouter(prefix="/retiradas", tags=["Retiradas"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/definir-data")
def definir_data_prevista(
    paciente_id: int,
    ano: int,
    mes: int,
    data_prevista: date,
    db: Session = Depends(get_db)
):
    retirada = (
        db.query(RetiradaMensal)
        .filter(
            RetiradaMensal.paciente_id == paciente_id,
            RetiradaMensal.ano == ano,
            RetiradaMensal.mes == mes
        )
        .first()
    )

    if retirada:
        retirada.data_prevista = data_prevista
    else:
        retirada = RetiradaMensal(
            paciente_id=paciente_id,
            ano=ano,
            mes=mes,
            data_prevista=data_prevista
        )
        db.add(retirada)

    db.commit()
    return {"status": "ok"}

@router.put("/{retirada_id}/marcar")
def marcar_retirada(retirada_id: int, db: Session = Depends(get_db)):
    retirada = db.query(RetiradaMensal).filter(RetiradaMensal.id == retirada_id).first()

    if not retirada:
        raise HTTPException(status_code=404, detail="Retirada não encontrada")

    retirada.data_retirada = date.today()
    db.commit()

    return {"status": "ok"}

