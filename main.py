"""
Punto de entrada de la app
Creación de instancias y creación del modelo usuarios y bases de datos
"""

from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.models.user import User
from app.models.db import DB

app = FastAPI()
db = DB('data_base_file.db')


class CreateUserRequest(BaseModel):
    username: str = 'user_test1'
    email: str = 'email_test1'
    password: str = 'pass_test1'


@app.get("/")
def index():
    return "Backed usuarios database"


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


if __name__ == "__main__":
    app.run(debug=True)
