from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from database import SessionLocal
from models.retiradas import RetiradaMensal
from models.paciente import Paciente

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


# ---------- DEPENDÊNCIA DB ----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------- DASHBOARD MENSAL ----------
@router.get("/")
def dashboard_mensal(
    ano: int,
    mes: int,
    db: Session = Depends(get_db)
):
    hoje = date.today()

    # 🔥 REGRA DE OURO:
    # O dashboard nasce da tabela retiradas_mensais
    retiradas = (
        db.query(RetiradaMensal)
        .join(Paciente, Paciente.id == RetiradaMensal.paciente_id)
        .filter(
            RetiradaMensal.ano == ano,
            RetiradaMensal.mes == mes,
            RetiradaMensal.data_prevista.isnot(None)
        )
        .all()
    )

    resultado = []

    for retirada in retiradas:
        paciente = retirada.paciente  # relacionamento direto

        # ---------- STATUS ----------
        if retirada.data_retirada:
            status = "OK"
            cor = "verde"

        elif retirada.data_prevista:
            if retirada.data_prevista < hoje:
                status = "Atrasado"
                cor = "vermelho"
            else:
                status = "Dentro do Prazo"
                cor = "azul"

        else:
            status = "Sem Registro"
            cor = "cinza"

        resultado.append({
            "paciente_id": paciente.id,
            "retirada_id": retirada.id,
            "nome": paciente.nome,
            "data_prevista": retirada.data_prevista,
            "data_retirada": retirada.data_retirada,
            "status": status,
            "cor": cor
        })

    total_pacientes = len(resultado)
    total_atrasados = sum(
        1 for r in resultado if r["status"] == "Atrasado"
    )

    return {
        "ano": ano,
        "mes": mes,
        "total_pacientes": total_pacientes,
        "total_atrasados": total_atrasados,
        "dados": resultado
    }