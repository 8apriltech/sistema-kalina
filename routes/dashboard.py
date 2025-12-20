from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from database import SessionLocal
from models import Paciente, RetiradaMensal

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def dashboard_mensal(ano: int, mes: int, db: Session = Depends(get_db)):
    hoje = date.today()
    ano_atual = hoje.year
    mes_atual = hoje.month

    pacientes = db.query(Paciente).filter(Paciente.ativo == True).all()
    resultado = []

    for paciente in pacientes:
        retirada = (
            db.query(RetiradaMensal)
            .filter(
                RetiradaMensal.paciente_id == paciente.id,
                RetiradaMensal.ano == ano,
                RetiradaMensal.mes == mes
            )
            .first()
        )

        # 🔹 SEM REGISTRO
        if not retirada:
            status = "Sem Registro"
            cor = "cinza"
            data_prevista = None
            data_retirada = None

        # 🟢 OK
        elif retirada.data_retirada:
            status = "OK"
            cor = "verde"
            data_prevista = retirada.data_prevista
            data_retirada = retirada.data_retirada

        else:
            data_prevista = retirada.data_prevista
            data_retirada = None

            # 🔴 mês/ano anterior ao atual → atrasado
            if (ano < ano_atual) or (ano == ano_atual and mes < mes_atual):
                status = "Atrasado"
                cor = "vermelho"

            # 🔵 mês atual → compara com hoje
            elif ano == ano_atual and mes == mes_atual:
                if retirada.data_prevista < hoje:
                    status = "Atrasado"
                    cor = "vermelho"
                else:
                    status = "Dentro do Prazo"
                    cor = "azul"

            # 🔵 mês futuro
            else:
                status = "Dentro do Prazo"
                cor = "azul"

        resultado.append({
            "paciente_id": paciente.id,
            "retirada_id": retirada.id if retirada else None,
            "nome": paciente.nome,
            "data_prevista": data_prevista,
            "data_retirada": data_retirada,
            "status": status,
            "cor": cor
        })

    # 🔴 CONTADOR DE ATRASADOS
    total_atrasados = sum(
        1 for item in resultado if item["status"] == "Atrasado"
    )

    return {
        "ano": ano,
        "mes": mes,
        "total_pacientes": len(resultado),
        "total_atrasados": total_atrasados,
        "dados": resultado
    }
