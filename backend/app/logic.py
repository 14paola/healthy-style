def calculate_calories(data):
    if data.sexo == "masculino":
        bmr = 66 + (13.7 * data.peso) + (5 * data.altura) - (6.8 * data.edad)
    else:
        bmr = 655 + (9.6 * data.peso) + (1.8 * data.altura) - (4.7 * data.edad)

    factores = {
        "sedentario": 1.2,
        "ligero": 1.375,
        "moderado": 1.55,
        "intenso": 1.725,
        "muy_intenso": 1.9
    }

    tdee = bmr * factores[data.actividad]

    return {
        "mantener": round(tdee),
        "subir": round(tdee + 500),
        "bajar": round(tdee - 500)
    }

def calculate_imc(data):
    imc = data.peso / ((data.altura / 100) ** 2)

    if imc < 18.5:
        categoria = "Bajo peso"
    elif imc < 25:
        categoria = "Normal"
    elif imc < 30:
        categoria = "Sobrepeso"
    elif imc < 35:
        categoria = "Obesidad I"
    elif imc < 40:
        categoria = "Obesidad II"
    else:
        categoria = "Obesidad III"

    return {"valor_imc": round(imc, 2), "categoria": categoria}
