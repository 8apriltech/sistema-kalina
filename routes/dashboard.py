from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from database import SessionLocal
from models.retiradas import RetiradaMensal
from models.paciente import Paciente

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def dashboard_mensal(
    ano: int,
    mes: int,
    db: Session = Depends(get_db)
):
    hoje = date.today()

    retiradas = (
        db.query(RetiradaMensal)
        .filter(
            RetiradaMensal.ano == ano,
            RetiradaMensal.mes == mes,
        )
        .all()
    )

    resultado = []

    for retirada in retiradas:
        paciente = (
            db.query(Paciente)
            .filter(Paciente.id == retirada.paciente_id)
            .first()
        )

        if not paciente:
            continue

        if retirada.data_retirada:
            status = "OK"
            cor = "verde"

        elif retirada.data_prevista:
            if retirada.data_prevista < hoje:
                status = "Em Atraso"
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

    return {
        "ano": ano,
        "mes": mes,
        "dados": resultado
    }