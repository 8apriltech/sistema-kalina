from pydantic import BaseModel
from typing import Optional


class DefinirDataRequest(BaseModel):
    paciente_id: int
    ano: int
    mes: int
    data_prevista: str


class PacienteCreate(BaseModel):
    nome: str
    observacao: Optional[str] = None


class PacienteResponse(BaseModel):
    id: int
    nome: str
    observacao: Optional[str]

    class Config:
        orm_mode = True
