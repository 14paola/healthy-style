from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import requests  # Asegúrate de tenerlo instalado

app = Flask(__name__)
app.secret_key = "clave_secreta_flask"

# Crear DB de usuarios si no existe
def init_db():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historial (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            edad INTEGER,
            sexo TEXT,
            peso REAL,
            altura REAL,
            actividad TEXT,
            imc REAL,
            categoria TEXT,
            calorias REAL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
            conn.commit()
            conn.close()
            return redirect("/login")
        except:
            return "El usuario ya existe."
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            session["user"] = email
            return redirect("/historial")
        else:
            return "Credenciales inválidas"
    return render_template("login.html")

@app.route("/historial", methods=["GET", "POST"])
def historial():
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        edad = int(request.form["edad"])
        sexo = request.form["sexo"]
        peso = float(request.form["peso"])
        altura = float(request.form["altura"])
        actividad = request.form["actividad"]

        # Cálculo del IMC
        imc = round(peso / ((altura / 100) ** 2), 2)

        # Clasificación del IMC
        if imc < 18.5:
            categoria = "Bajo peso"
        elif 18.5 <= imc < 25:
            categoria = "Normal"
        elif 25 <= imc < 30:
            categoria = "Sobrepeso"
        else:
            categoria = "Obesidad"

        # Cálculo calórico con fórmula de Harris-Benedict
        if sexo == "masculino":
            tmb = 10 * peso + 6.25 * altura - 5 * edad + 5
        else:
            tmb = 10 * peso + 6.25 * altura - 5 * edad - 161

        niveles = {
            "sedentario": 1.2,
            "ligero": 1.375,
            "moderado": 1.55,
            "intenso": 1.725,
            "muy_intenso": 1.9
        }
        calorias = round(tmb * niveles.get(actividad, 1.2))

        resultado = {
            "imc": imc,
            "categoria": categoria,
            "calorias": calorias
        }
  # Guardar en la base de datos
        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO historial (user_email, edad, sexo, peso, altura, actividad, imc, categoria, calorias)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (session["user"], edad, sexo, peso, altura, actividad, imc, categoria, calorias))
        conn.commit()
        conn.close()


        return render_template("historial.html", user=session["user"], resultado=resultado)

    # Si método GET, simplemente muestra el formulario sin resultados
    return render_template("historial.html", user=session["user"], resultado=None)


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

@app.route("/admin")
def admin():
    if "user" not in session or session["user"] != "paola.perez2@utp.ac.pa":
        return "Acceso denegado"

    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM historial ORDER BY fecha DESC")
    historiales = cursor.fetchall()
    conn.close()

    return render_template("admin.html", historiales=historiales)

@app.route("/mi_historial")
def mi_historial():
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()
    cursor.execute("SELECT edad, sexo, peso, altura, actividad, imc, categoria, calorias, fecha FROM registros WHERE user_email = ? ORDER BY fecha DESC", (session["user"],))
    historial = cursor.fetchall()
    conn.close()

    return render_template("mi_historial.html", historial=historial, user=session["user"])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
