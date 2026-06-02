import asyncpg
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

async def get_db_connection():
    return await asyncpg.connect(
        user="postgres",
        password="sql",
        database="postgres",
        host="localhost"
    )

@app.get("/pets")
async def get_pets():
    conn = await get_db_connection()
    try:
        rows = await conn.fetch("SELECT * FROM pets")
        pets = []
        for row in rows:
            pets.append({"id": row["id_pet"], "nome": row["nome_pet"]})
        return {"users": pets}
    finally:
        await conn.close()


@app.get("/tutor")
async def get_tutor():
    conn = await get_db_connection()
    try:
        rows = await conn.fetch("SELECT * FROM tutor")
        pets = []
        for row in rows:
            tutor.append({"id": row["id_tutor"], "nome": row["nome"]})
        return {"users": tutor}
    finally:
        await conn.close()































































@app.get("/pets/{id_pet}")
async def get_pet(id_pet: int):
    conn = await get_db_connection()
    # Buscamos o pet pelo ID
    row = await conn.fetchrow("SELECT * FROM pets WHERE id_pet = $1", id_pet)
    await conn.close()

    # Verificamos se o pet foi encontrado para evitar erro de 'None'
    if row is None:
        return {"error": "Pet não encontrado"}

    # Criamos o dicionário com os dados que vieram do banco
    pet_data = {"id": row["id_pet"], "nome": row["nome_pet"]}
    
    return {"pet": pet_data}


# POST

class Funcionario(BaseModel):
    id_funcionario: int
    nome: str
    telefone: str
    salario: float

@app.post("/funcionario")
async def create_funcionario(funcionario: Funcionario):
    conn = await get_db_connection()
    await conn.execute(
            "INSERT INTO funcionario (id_funcionario, nome, telefone, salario) VALUES ($1, $2, $3, $4)",
            funcionario.id_funcionario, 
            funcionario.nome, 
            funcionario.telefone, 
            funcionario.salario
    )
    await conn.close()
    return {"message": "Ator criado com sucesso!"}


# UPDATE

class FuncionarioUpdate(BaseModel):
    nome: str
    salario: float

@app.put("/funcionario/{id_funcionario}")
async def update_funcionario(id_funcionario: int, funcionario_data: FuncionarioUpdate):
    conn = await get_db_connection()
    # Executar atualização
    result = await conn.execute(
        """
        UPDATE funcionario
        SET nome = $1, salario = $2 WHERE id_funcionario = $3
        """,
        funcionario_data.nome, funcionario_data.salario, id_funcionario
        )
    await conn.close()
    # Verificar se a atualização afetou algum registro
    if result == "UPDATE 1":
        return {"message": f"Funcionario atualizado com sucesso! ID do funcionario: {id_funcionario}"}
    else:
        return {"message": "Funcionario não foi atualizado"}


# DELETE

@app.delete("/funcionario/{id_funcionario}")
async def delete_funcionario(id_funcionario: int):
    conn = await get_db_connection()
    result = await conn.execute(
        "DELETE FROM funcionario WHERE id_funcionario = $1", id_funcionario
    )
    await conn.close()
    if result == "DELETE 1":
        return {"message": f"Funcionario deletado com sucesso! ID do funcionario: {id_funcionario}"}
    else:
        return {"message": "Funcionario não foi deletado"} 