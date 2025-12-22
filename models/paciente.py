from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    ativo = Column(Boolean, default=True)
    observacao = Column(String)