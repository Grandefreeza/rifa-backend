from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import sqlite3
import qrcode
import os

app = Flask(__name__)
CORS(app)

DB = "database.db"

def conectar():
    return sqlite3.connect(DB)

def criar_tabelas():
    con = conectar()
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT,
        senha TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS rifas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        quantidade INTEGER,
        valor REAL,
        data TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS participantes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        contato TEXT,
        numero INTEGER,
        rifa_id INTEGER
    )
    """)

    con.commit()
    con.close()

criar_tabelas()

# LOGIN
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    con = conectar()
    cur = con.cursor()

    cur.execute("SELECT * FROM usuarios WHERE usuario=? AND senha=?", (data["usuario"], data["senha"]))
    user = cur.fetchone()

    return jsonify({"logado": bool(user)})

# CRIAR RIFA
@app.route("/rifa", methods=["POST"])
def criar_rifa():
    d = request.json
    con = conectar()
    cur = con.cursor()

    cur.execute("INSERT INTO rifas (nome, quantidade, valor, data) VALUES (?,?,?,?)",
                (d["nome"], d["quantidade"], d["valor"], d["data"]))

    con.commit()
    return jsonify({"msg": "Rifa criada"})

# LISTAR RIFAS
@app.route("/rifas")
def listar_rifas():
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM rifas")
    return jsonify(cur.fetchall())

# COMPRAR
@app.route("/comprar", methods=["POST"])
def comprar():
    d = request.json
    con = conectar()
    cur = con.cursor()

    cur.execute("""
    INSERT INTO participantes (nome, contato, numero, rifa_id)
    VALUES (?,?,?,?)
    """, (d["nome"], d["contato"], d["numero"], d["rifa_id"]))

    con.commit()
    return jsonify({"msg": "Comprado"})

# GERAR PIX QR CODE
@app.route("/pix/<valor>")
def pix(valor):
    img = qrcode.make(f"PIX:{valor}")
    caminho = "pix.png"
    img.save(caminho)
    return send_file(caminho, mimetype="image/png")

# SORTEIO
@app.route("/sortear/<rifa_id>")
def sortear(rifa_id):
    con = conectar()
    cur = con.cursor()

    cur.execute("SELECT numero FROM participantes WHERE rifa_id=?", (rifa_id,))
    numeros = [n[0] for n in cur.fetchall()]

    import random
    vencedor = random.choice(numeros) if numeros else None

    return jsonify({"vencedor": vencedor})

app.run(debug=True)
