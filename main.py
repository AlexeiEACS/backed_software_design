"""
Punto de entrada de la app
Creación de instancias y creación del modelo usuarios y bases de datos
"""

from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.models.user import User
from app.models.db import DB
from ruamel.yaml import YAML

app = FastAPI()
db = DB('data_base_file.db')


class CreateUserRequest(BaseModel):
    username: str = 'user_test1'
    email: str = 'email_test1'
    password: str = 'pass_test1'


class TransactionRequest(BaseModel):
    type: str
    amount: float


@app.get("/", tags=['SAIE - sistema de administracion de ingresos y egresos'])
def index():
    return "Backed User's transactions"


@app.post("/users", tags=['Users table'])
def create_user(user: CreateUserRequest):
    user = User(username=user.username,
                email=user.email, password=user.password)

    db.insert_user(user)
    return user


@app.put("/users/{id}", tags=['Users table'])
def update_user(id: int, user: User):
    db.update_user(id, user)
    return user


@app.delete("/users/{id}", tags=['Users table'])
def delete_user(id: int):
    db.delete_user(id)
    return {"message": "Usuario eliminado"}


# Use response_model to specify the model for the response
@app.get("/users", tags=['Users table'])
def get_all_users():
    users = db.get_users()
    user_list = [{"id": user.id, "username": user.username, "email": user.email,
                  "created_at": user.created_at, "updated_at": user.updated_at} for user in users]
    return user_list


@app.post("/transactions/add", tags=['Transactions table'])
def add_transaction(user_id: int, transaction: TransactionRequest):
    db.add_transaction(user_id, transaction.type, transaction.amount)
    return {"message": "Transaction added"}


@app.get("/transactions/total", tags=['Transactions table'])
def get_total_transactions(user_id: int):
    total_transactions = db.get_total_transactions(user_id)
    return total_transactions


@app.delete("/transactions/delete", tags=['Transactions table'])
def delete_transaction(id: int):
    db.delete_transaction(id)
    return {"message": "Transaccion eliminada"}


def generate_openapi_yaml():
    openapi_schema = get_openapi(
        title="SAIE", version="1.0.0", routes=app.routes)
    yaml = YAML()
    with open("openapi.yaml", "w") as file:
        yaml.dump(openapi_schema, file)


generate_openapi_yaml()
if __name__ == "__main__":
    db.create_tables()
    generate_openapi_yaml()
    # app.run(debug=True)
