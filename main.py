import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import os

app = FastAPI()

class LoginData(BaseModel):
    email: str
    senha: str

@app.post("/login")
def login(data: LoginData):

    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))

        caminho_banco  = os.path.join(base_dir, "banco_teste.db")

        conexao_banco = sqlite3.connect(caminho_banco)
        cursor = conexao_banco.cursor()

        cursor.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (data.email, data.senha))
        resultado =  cursor.fetchone()

        if resultado:
            return{"mesagem": "Login realizado com sucesso!"}
        else:
            raise HTTPException(status_code=401, detail="email ou senha incorretos.")
        
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {str(e)}")
    
    finally:
        conexao_banco.close()

if __name__ == "__main__":
    uvicorn.run(app, port=8001)
