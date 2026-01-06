from sqlalchemy import Column, Integer, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class RetiradaMensal(Base):
    __tablename__ = "retiradas_mensais"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)

    ano = Column(Integer, nullable=False)
    mes = Column(Integer, nullable=False)

    data_prevista = Column(Date, nullable=True)
    data_retirada = Column(Date, nullable=True)

    ok = Column(Boolean, default=False)

    # 🔥 ESTA LINHA RESOLVE TUDO
    paciente = relationship("Paciente")