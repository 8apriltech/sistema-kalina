from pydantic import BaseModel
from datetime import date
from typing import Optional

class PacienteBase(BaseModel):
    nome: str
    ativo: bool = True
    observacao: Optional[str] = None

class PacienteCreate(PacienteBase):
    pass

class PacienteResponse(PacienteBase):
    id: int

    class Config:
        from_attributes = True


class RetiradaBase(BaseModel):
    paciente_id: int
    ano: int
    mes: int
    data_prevista: date
    data_retirada: Optional[date] = None

class RetiradaCreate(RetiradaBase):
    pass

class RetiradaResponse(RetiradaBase):
    id: int

    class Config:
        from_attributes = True