from sqlalchemy import Column, Integer, Date, ForeignKey
from database import Base

class RetiradaMensal(Base):
    __tablename__ = "retiradas_mensais"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    ano = Column(Integer)
    mes = Column(Integer)
    data_prevista = Column(Date)
    data_retirada = Column(Date)
