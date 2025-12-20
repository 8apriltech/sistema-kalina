from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    ativo = Column(Boolean, default=True)
    observacao = Column(String, nullable=True)

    retiradas = relationship("RetiradaMensal", back_populates="paciente")


class RetiradaMensal(Base):
    __tablename__ = "retiradas_mensais"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    ano = Column(Integer, nullable=False)
    mes = Column(Integer, nullable=False)
    data_prevista = Column(Date, nullable=False)
    data_retirada = Column(Date, nullable=True)

    paciente = relationship("Paciente", back_populates="retiradas")
