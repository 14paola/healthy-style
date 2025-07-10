@app.post("/calcular")
def calcular(data: DatosEntrada):
    imc = calcular_imc(data.peso, data.altura)
    categoria = obtener_categoria_imc(imc)
    calorias = calcular_calorias(data)
    return {
        "imc": round(imc, 2),
        "categoria": categoria,
        "calorias": round(calorias)
    }
