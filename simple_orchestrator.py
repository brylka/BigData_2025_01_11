from typing import Dict
from enum import Enum
from datetime import datetime

class TaskStatus(Enum):
    PENDING = "pending"         # Zadanie oczekujące na przetworzenie
    PROCESSING = "processing"   # Zadanie w trakcie przetwarzania
    COMPLETING = "completing"   # Zadanie przetworzone poprawnie
    FAILED = "failed"           # Zadanie zakończone błędem

class TaskPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class Task:
    def __init__(self, task_id: str, data: Dict, priority: TaskPriority = TaskPriority.MEDIUM):
        self.task_id = task_id
        self.data = data
        self.status = TaskStatus.PENDING
        self.priority = priority
        self.createt_at = datetime.now()
        self.error = None


# task = Task("test", {"pole1": 3, "pole2": "alamakota"})
# print(task.priority)