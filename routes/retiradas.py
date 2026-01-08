from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from datetime import datetime

from database import SessionLocal
from models.retiradas import RetiradaMensal

router = APIRouter(prefix="/retiradas", tags=["Retiradas"])


# ---------- DEPENDÊNCIA DB ----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================================================
# ATUALIZAR DATA PREVISTA (PODE LIMPAR)
# =========================================================
@router.put("/{retirada_id}/data-prevista")
def atualizar_data_prevista(
    retirada_id: int,
    payload: dict = Body(...),
    db: Session = Depends(get_db),
):
    retirada = (
        db.query(RetiradaMensal)
        .filter(RetiradaMensal.id == retirada_id)
        .first()
    )

    if not retirada:
        raise HTTPException(404, "Retirada não encontrada")

    # 🔥 permite limpar a data
    if payload.get("data_prevista"):
        try:
            retirada.data_prevista = datetime.strptime(
                payload["data_prevista"], "%Y-%m-%d"
            ).date()
        except Exception:
            raise HTTPException(400, "Formato inválido de data (YYYY-MM-DD)")
    else:
        retirada.data_prevista = None

    db.commit()
    return {"status": "ok"}


# =========================================================
# ATUALIZAR DATA DE RETIRADA (PODE LIMPAR)
# =========================================================
@router.put("/{retirada_id}/data-retirada")
def atualizar_data_retirada(
    retirada_id: int,
    payload: dict = Body(...),
    db: Session = Depends(get_db),
):
    retirada = (
        db.query(RetiradaMensal)
        .filter(RetiradaMensal.id == retirada_id)
        .first()
    )

    if not retirada:
        raise HTTPException(404, "Retirada não encontrada")

    if payload.get("data_retirada"):
        try:
            retirada.data_retirada = datetime.strptime(
                payload["data_retirada"], "%Y-%m-%d"
            ).date()
        except Exception:
            raise HTTPException(400, "Formato inválido de data (YYYY-MM-DD)")
    else:
        retirada.data_retirada = None
        retirada.ok = False

    db.commit()
    return {"status": "ok"}


# =========================================================
# MARCAR OK (CONFIRMAÇÃO FINAL HUMANA)
# =========================================================
@router.put("/{retirada_id}/marcar")
def marcar_ok(
    retirada_id: int,
    payload: dict = Body(...),
    db: Session = Depends(get_db),
):
    retirada = (
        db.query(RetiradaMensal)
        .filter(RetiradaMensal.id == retirada_id)
        .first()
    )

    if not retirada:
        raise HTTPException(404, "Retirada não encontrada")

    if not payload.get("data_retirada"):
        raise HTTPException(400, "data_retirada é obrigatória para marcar OK")

    try:
        retirada.data_retirada = datetime.strptime(
            payload["data_retirada"], "%Y-%m-%d"
        ).date()
    except Exception:
        raise HTTPException(400, "Formato inválido de data (YYYY-MM-DD)")

    retirada.ok = True
    db.commit()
    return {"status": "ok"}


# =========================================================
# CADASTRO INICIAL — DEFINE DATA PREVISTA
# (ano/mês vêm da própria data)
# =========================================================
@router.post("/definir-data")
def definir_data_prevista(
    payload: dict = Body(...),
    db: Session = Depends(get_db),
):
    if not payload.get("paciente_id") or not payload.get("data_prevista"):
        raise HTTPException(
            400, "paciente_id e data_prevista são obrigatórios"
        )

    try:
        data_prevista = datetime.strptime(
            payload["data_prevista"], "%Y-%m-%d"
        ).date()
    except Exception:
        raise HTTPException(400, "Formato inválido de data (YYYY-MM-DD)")

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
            data_retirada=None,
            ok=False,
        )
        db.add(retirada)

    db.commit()
    return {"status": "ok"}
