from pydantic import BaseModel

class UserInput(BaseModel):
    edad: int
    sexo: str
    peso: float
    altura: float
    actividad: str

class CaloriasResponse(BaseModel):
    mantener: int
    subir: int
    bajar: int

class IMCResponse(BaseModel):
    valor_imc: float
    categoria: str
