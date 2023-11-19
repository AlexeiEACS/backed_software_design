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
from fastapi.middleware.cors import CORSMiddleware

import datetime

app = FastAPI()
db = DB('data_base_file.db')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # Orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"], # Métodos permitidos
    allow_headers=["*"], # Cabeceras permitidas
)
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


@app.put("/transactions/update_type", tags=['Transactions table'])
def update_transaction_type(user_id: int, transaction_id: int, new_type: str):
    db.update_transaction_type(user_id, transaction_id, new_type)
    return {"message": f"Transaccion {transaction_id} modificada"}


@app.delete("/transactions/delete", tags=['Transactions table'])
def delete_transaction(user_id: int, transaction_id: int):
    db.delete_transaction(user_id, transaction_id)
    return {"message": "Transaccion eliminada"}


@app.get("/budget_planification", tags=['Budget'])
def get_planification_budget(amount: float, number_months: float):
    amount,number_months = float(amount), float(number_months)
    by_month = amount / number_months
    start_date = datetime.datetime.today()
    dicts = {}
    for i in range(int(number_months)):
        date_str = (start_date + datetime.timedelta(days=30*i)
                    ).strftime('%Y-%m-%d')
        dicts[date_str] = by_month
    return dicts


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
    #app.run(debug=True)
