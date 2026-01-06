from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from datetime import datetime

from database import SessionLocal
from models.retiradas import RetiradaMensal

router = APIRouter(prefix="/retiradas", tags=["Retiradas"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ===============================
# DEFINIR / ATUALIZAR DATA PREVISTA
# ===============================
@router.put("/{retirada_id}/data-prevista")
def atualizar_data_prevista(
    retirada_id: int,
    payload: dict = Body(...),
    db: Session = Depends(get_db),
):
    retirada = db.query(RetiradaMensal).filter(
        RetiradaMensal.id == retirada_id
    ).first()

    if not retirada:
        raise HTTPException(404, "Retirada não encontrada")

    try:
        retirada.data_prevista = datetime.strptime(
            payload["data_prevista"], "%Y-%m-%d"
        ).date()
    except Exception:
        raise HTTPException(400, "Data inválida")

    db.commit()
    return {"status": "ok"}


# ===============================
# ATUALIZAR DATA DE RETIRADA (SEM OK)
# ===============================
@router.put("/{retirada_id}/data-retirada")
def atualizar_data_retirada(
    retirada_id: int,
    payload: dict = Body(...),
    db: Session = Depends(get_db),
):
    retirada = db.query(RetiradaMensal).filter(
        RetiradaMensal.id == retirada_id
    ).first()

    if not retirada:
        raise HTTPException(404, "Retirada não encontrada")

    try:
        retirada.data_retirada = datetime.strptime(
            payload["data_retirada"], "%Y-%m-%d"
        ).date()
    except Exception:
        raise HTTPException(400, "Data inválida")

    db.commit()
    return {"status": "ok"}


# ===============================
# MARCAR OK (CONFIRMAÇÃO HUMANA)
# ===============================
@router.put("/{retirada_id}/marcar")
def marcar_ok(
    retirada_id: int,
    payload: dict = Body(...),
    db: Session = Depends(get_db),
):
    retirada = db.query(RetiradaMensal).filter(
        RetiradaMensal.id == retirada_id
    ).first()

    if not retirada:
        raise HTTPException(404, "Retirada não encontrada")

    try:
        retirada.data_retirada = datetime.strptime(
            payload["data_retirada"], "%Y-%m-%d"
        ).date()
    except Exception:
        raise HTTPException(400, "Data inválida")

    retirada.ok = True
    db.commit()

    return {"status": "ok"}

@router.post("/definir-data")
def definir_data_prevista(
    payload: dict = Body(...),
    db: Session = Depends(get_db)
):
    try:
        data_prevista = datetime.strptime(
            payload["data_prevista"], "%Y-%m-%d"
        ).date()
    except Exception:
        raise HTTPException(400, "Data inválida")

    # 🔥 mês/ano derivados da data
    ano = data_prevista.year
    mes = data_prevista.month

    retirada = (
        db.query(RetiradaMensal)
        .filter(
            RetiradaMensal.paciente_id == payload["paciente_id"],
            RetiradaMensal.ano == ano,
            RetiradaMensal.mes == mes,
        )
        .first()
    )

    if retirada:
        retirada.data_prevista = data_prevista
    else:
        retirada = RetiradaMensal(
            paciente_id=payload["paciente_id"],
            ano=ano,
            mes=mes,
            data_prevista=data_prevista,
        )
        db.add(retirada)

    db.commit()
    return {"status": "ok"}
