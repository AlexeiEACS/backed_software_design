from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class User:
    id: int = field(init=False)
    username: str
    email: str
    password: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    def __post_init__(self):
        self.id = None

    def __repr__(self):
        return f"User {self.id} {self.username} {self.email}"
