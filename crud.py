from sqlalchemy.orm import Session
from models import Paciente, RetiradaMensal
from datetime import date

def criar_paciente(db: Session, nome: str, observacao: str = None):
    paciente = Paciente(nome=nome, observacao=observacao)
    db.add(paciente)
    db.commit()
    db.refresh(paciente)
    return paciente

def listar_pacientes(db: Session):
    return db.query(Paciente).filter(Paciente.ativo == True).all()

def criar_retirada(db: Session, retirada: RetiradaMensal):
    db.add(retirada)
    db.commit()
    db.refresh(retirada)
    return retirada

def excluir_paciente(db, paciente_id: int):
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()

    if not paciente:
        return False

    db.query(RetiradaMensal).filter(
        RetiradaMensal.paciente_id == paciente_id
    ).delete()

    db.delete(paciente)
    db.commit()
    return True