from typing import Dict, List
from enum import Enum
from datetime import datetime
import asyncio

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

    async def add_task(self, task_id: str, data: Dict, priority: TaskPriority = TaskPriority.MEDIUM):
        """
        Dodaje nowe zadanie do orkiestratora.
        Zadania są dodawane do słownika i czekają na przetworzenie.
        """
        task = Task(task_id, data, priority)        # Tworzymu instancję klasy Task z zadaniem
        self.tasks[task_id] = task                  # Dodajemy zadanie do słownika
        print(f"Dodano zadanie: {task_id} z priorytetem {priority.name}")
        return task_id                              # Zwracamy task_id

    async def process_tasks(self):
        while True:
            pending_tasks = self._get_peding_tasks()    # Pobranie listy z taskami ze statusem PENDING

            for task in pending_tasks:                          # Przetworzenie listy z taskami
                if task.task_id not in self.processing_tasks:   # Sprawdzenie czy dany task nie znajduje się w rzetwarzanym zbiorze
                    self.processing_tasks.add(task.task_id)     # Dodanie task_id do zbioru przetwarzanych tasków
                    await self._process_single_task(task)       # Uruchomienie przetwarzania taska

    async def _process_single_task(self, task: Task):                   # Metoda przetwarzająca zadanie
        try:
            print(f"Rozpoczynam przetwarzanie zadania: {task.task_id}")
            task.status = TaskStatus.PROCESSING                             # Ustawienie statusu

            measurment = task.data
            if measurment.get("temperature") > 30:                       # Logika biznesowa - sprawdzenie temp
                print(f"Wykryto wysoką temperaturę: {measurment['temperature']} 'C")    # Ale może być dodanie do bazy danych
            #await asyncio.sleep(2)

            task.status = TaskStatus.COMPLETING                             # Zakończenie przetwarzania i ustawienie statusu na COMPLETING
            print(f"Zakończono przetwarzanie zadania: {task.task_id}")

            self.processing_tasks.remove(task.task_id)                      # Usunięcie z zbioru przetwarzanych tasków
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            print(f"Błąd podczas przetwarzania zadania {task.task_id}: {e}")

    def get_task_status(self, task_id: str) -> Dict:
        task = self.tasks.get(task_id)

        return {
            "task_id": task.task_id,
            "status": task.status.name,
            "priority": task.priority.name,
            "created_at": task.created_at,
            "error": task.error
        }

    def _get_peding_tasks(self) -> List[Task]:
        pending_task = []                               # Pusta lista na początek
        for task in self.tasks.values():
            if task.status == TaskStatus.PENDING:       # Wyszukujemy taski ze statusem PENDING
                pending_task.append(task)               # Dodajemy taski do list
        def sort_key(task):                                 # Dodatkowa metoda do posortowania
            return (task.priority.value, task.created_at)   # zgodnie z priorytetem oraz czasem stworzenia
        pending_task.sort(key=sort_key, reverse=True)       # Sortowanie
        return pending_task                                 # Zwrócenie listy




# Metoda asynchroniczna main
async def main():
    orchestrator = SimlpeOrchestrator()         # Tworzymy orkiestrator

    processing_task = asyncio.create_task(orchestrator.process_tasks())

    task_id = await orchestrator.add_task(      # Dodajemy statyczne dane do zadania
        "task1",
        {
            "station_id": "STATION001",
            "temperature": 32.5,
            "humanity": 80
         },
        TaskPriority.HIGH
    )



if __name__ == "__main__":
    asyncio.run(main())