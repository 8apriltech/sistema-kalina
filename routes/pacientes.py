from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from database import SessionLocal
from models.retiradas import RetiradaMensal
from models.paciente import Paciente
import crud, schemas

router = APIRouter(prefix="/pacientes", tags=["Pacientes"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.PacienteResponse)
def criar(paciente: schemas.PacienteCreate, db: Session = Depends(get_db)):
    return crud.criar_paciente(db, paciente.nome, paciente.observacao)


@router.get("/", response_model=list[schemas.PacienteResponse])
def listar(db: Session = Depends(get_db)):
    return crud.listar_pacientes(db)


@router.get("/{paciente_id}/historico")
def historico_paciente(paciente_id: int, ano: int = None, db: Session = Depends(get_db)):
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    query = db.query(RetiradaMensal).filter(RetiradaMensal.paciente_id == paciente_id)
    if ano:
        query = query.filter(RetiradaMensal.ano == ano)

    retiradas = query.order_by(RetiradaMensal.ano.desc(), RetiradaMensal.mes.asc()).all()
    hoje = date.today()

    historico = []
    for r in retiradas:
        if r.data_retirada:
            status = "OK"
            cor = "verde"
        elif r.data_prevista:
            if r.data_prevista < hoje:
                status = "Em Atraso"
                cor = "vermelho"
            else:
                status = "Dentro do Prazo"
                cor = "azul"
        else:
            status = "Sem Registro"
            cor = "cinza"

        historico.append({
            "retirada_id": r.id,
            "ano": r.ano,
            "mes": r.mes,
            "data_prevista": str(r.data_prevista) if r.data_prevista else None,
            "data_retirada": str(r.data_retirada) if r.data_retirada else None,
            "status": status,
            "cor": cor
        })

    return {
        "paciente_id": paciente.id,
        "nome": paciente.nome,
        "observacao": getattr(paciente, "observacao", None),
        "historico": historico
    }


@router.delete("/{paciente_id}")
def excluir_paciente(paciente_id: int, db: Session = Depends(get_db)):
    sucesso = crud.excluir_paciente(db, paciente_id)

    if not sucesso:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    return {"status": "ok"}
