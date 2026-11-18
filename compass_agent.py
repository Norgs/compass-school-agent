import os
import json
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Literal

DATA_DIR = Path.expanduser(Path("~/.hermes/data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "compass_todo.json"

class CompassItem(BaseModel):
    id: str
    child: str
    date: str
    title: str
    category: Literal["Informational", "Action Required", "Payment Needed", "Excursion"]
    deadline: Optional[str] = None
    cost: Optional[str] = None
    summary: str
    status: Literal["pending", "completed"] = "pending"

def load_store() -> List[dict]:
    if DB_PATH.exists():
        try:
            return json.loads(DB_PATH.read_text())
        except Exception:
            return []
    return []

def save_store(items: List[dict]):
    DB_PATH.write_text(json.dumps(items, indent=2))

if __name__ == "__main__":
    print("Compass agent schema & store initialized at:", DB_PATH)
