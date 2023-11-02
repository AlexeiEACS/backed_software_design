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


@app.get("/")
def index():
    return "Backed User's transactions"


@app.post("/users")
def create_user(user: CreateUserRequest):
    user = User(username=user.username,
                email=user.email, password=user.password)

    db.insert_user(user)
    return user


@app.put("/users/{id}")
def update_user(id: int, user: User):
    db.update_user(id, user)
    return user


@app.delete("/users/{id}")
def delete_user(id: int):
    db.delete_user(id)
    return {"message": "Usuario eliminado"}


# Use response_model to specify the model for the response
@app.get("/users")
def get_all_users():
    users = db.get_users()
    user_list = [{"id": user.id, "username": user.username, "email": user.email,
                  "created_at": user.created_at, "updated_at": user.updated_at} for user in users]
    return user_list


@app.post("/users/{user_id}/transactions")
def add_transaction(user_id: int, transaction: TransactionRequest):
    db.add_transaction(user_id, transaction.type, transaction.amount)
    return {"message": "Transaction added"}


@app.get("/users/{user_id}/transactions/total")
def get_total_transactions(user_id: int):
    total_transactions = db.get_total_transactions(user_id)
    return total_transactions


def generate_openapi_yaml():
    openapi_schema = get_openapi(title="Your API Title", version="1.0.0")
    yaml = YAML()
    with open("openapi.yaml", "w") as file:
        yaml.dump(openapi_schema, file)


if __name__ == "__main__":
    db.create_tables()
    app.run(debug=True)
