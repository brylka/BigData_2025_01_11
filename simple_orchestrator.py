from typing import Dict
from enum import Enum
from datetime import datetime

# Definicja statusów zadań
class TaskStatus(Enum):
    PENDING = "pending"         # Zadanie oczekujące na przetworzenie
    PROCESSING = "processing"   # Zadanie w trakcie przetwarzania
    COMPLETING = "completing"   # Zadanie przetworzone poprawnie
    FAILED = "failed"           # Zadanie zakończone błędem

# Definicja priorytetów zadań - wyższy numer = wyższy priorytet
class TaskPriority(Enum):
    LOW = 1         # Niski
    MEDIUM = 2      # Średni
    HIGH = 3        # Wysoki

class Task:
    def __init__(self, task_id: str, data: Dict, priority: TaskPriority = TaskPriority.MEDIUM):
        self.task_id = task_id              # Unikalny identyfikator zadania
        self.data = data                    # Dane wejściowe
        self.status = TaskStatus.PENDING    # Początkowy status
        self.priority = priority            # Priorytet zadania
        self.created_at = datetime.now()    # Odcisk czasu utworzenia zadania
        self.error = None                   # Miejsce na przechowywanie ewentualnych błędów


class SimlpeOrchestrator:
    def __init__(self):
        # Słownik przechowujący wszystkie zadania
        self.tasks: Dict[str, Task] = {}
        # Zbiór zadań aktualnie przetwarzanych
        self.processing_tasks: set = set()


# task = Task("test", {"pole1": 3, "pole2": "alamakota"})
# print(task.priority)