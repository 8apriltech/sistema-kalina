from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
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


@router.delete("/{paciente_id}")
def excluir_paciente(paciente_id: int, db: Session = Depends(get_db)):
    sucesso = crud.excluir_paciente(db, paciente_id)

    if not sucesso:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    return {"status": "ok"}
