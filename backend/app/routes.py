from fastapi import APIRouter
from app.logic import calculate_calories, calculate_imc
from app.schemas import UserInput, CaloriasResponse, IMCResponse

router = APIRouter()

@router.post("/calcular", response_model=CaloriasResponse)
def calcular_calorias(data: UserInput):
    return calculate_calories(data)

@router.post("/imc", response_model=IMCResponse)
def calcular_imc(data: UserInput):
    return calculate_imc(data)
