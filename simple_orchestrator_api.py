from enum import Enum
from datetime import datetime
from typing import Dict, List
import asyncio
import aiohttp


class TaskStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class Task:
    def __init__(self, task_id: str, station_id: str, priority: TaskPriority = TaskPriority.MEDIUM):
        self.task_id = task_id
        self.station_id = station_id  # Zmieniamy data na station_id
        self.status = TaskStatus.PENDING
        self.priority = priority
        self.created_at = datetime.now()
        self.error = None
        self.weather_data = None  # Dodajemy miejsce na dane pogodowe


class WeatherOrchestrator:
    def __init__(self, api_url: str = "http://127.0.0.1:8000"):
        self.tasks: Dict[str, Task] = {}
        self.processing_tasks: set = set()
        self.api_url = api_url

    async def add_task(self, task_id: str, station_id: str, priority: TaskPriority = TaskPriority.MEDIUM) -> str:
        """Dodaj nowe zadanie do monitorowania stacji pogodowej"""
        task = Task(task_id, station_id, priority)
        self.tasks[task_id] = task
        print(f"Dodano zadanie: {task_id} dla stacji {station_id}")
        return task_id

    async def process_tasks(self):
        """Główna pętla przetwarzania zadań"""
        async with aiohttp.ClientSession() as session:  # Tworzymy sesję HTTP
            while True:
                pending_tasks = self._get_pending_tasks()

                for task in pending_tasks:
                    if task.task_id not in self.processing_tasks:
                        self.processing_tasks.add(task.task_id)
                        await self._process_single_task(session, task)

                await asyncio.sleep(1)

    async def _process_single_task(self, session: aiohttp.ClientSession, task: Task):
        """Przetwórz pojedyncze zadanie - pobierz dane pogodowe"""
        try:
            print(f"Rozpoczynam przetwarzanie zadania: {task.task_id}")
            task.status = TaskStatus.PROCESSING


            # Pobieramy dane ze stacji pogodowej
            async with session.get(f"{self.api_url}/weather/{task.station_id}") as response:
                task.weather_data = await response.json()
            await asyncio.sleep(3)
            # Sprawdzamy temperaturę
            if float(task.weather_data["temperature"]) > 30:
                print(f"Wykryto wysoką temperaturę: {task.weather_data['temperature']}°C")

            task.status = TaskStatus.COMPLETED
            print(f"Zakończono przetwarzanie zadania: {task.task_id}")

        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            print(f"Błąd podczas przetwarzania zadania {task.task_id}: {e}")
        finally:
            self.processing_tasks.remove(task.task_id)

    def _get_pending_tasks(self) -> List[Task]:
        """Pobierz zadania oczekujące, posortowane według priorytetu"""
        return sorted(
            [task for task in self.tasks.values() if task.status == TaskStatus.PENDING],
            key=lambda x: (x.priority.value, x.created_at),
            reverse=True
        )

    def get_task_status(self, task_id: str) -> Dict:
        """Pobierz status zadania"""
        task = self.tasks.get(task_id)
        if not task:
            return {"error": "Task not found"}

        status_data = {
            "task_id": task.task_id,
            "station_id": task.station_id,
            "status": task.status.name,
            "priority": task.priority.name,
            "created_at": task.created_at.isoformat(),
            "error": task.error
        }

        if task.weather_data:
            status_data["weather_data"] = task.weather_data

        return status_data


# Przykład użycia
async def main():
    orchestrator = WeatherOrchestrator()

    # Uruchom proces przetwarzania w tle
    processing_task = asyncio.create_task(orchestrator.process_tasks())

    # Dodaj przykładowe zadanie monitorowania stacji
    task_id = await orchestrator.add_task(
        "task1",
        "STAT001",  # ID stacji z API
        TaskPriority.HIGH
    )

    # Poczekaj chwilę i sprawdź status
    #await asyncio.sleep(1)
    print(orchestrator.get_task_status(task_id))

    # Poczekaj na zakończenie zadania
    await asyncio.sleep(3)
    print(orchestrator.get_task_status(task_id))
    await asyncio.sleep(3)
    print(orchestrator.get_task_status(task_id))
    # Zakończ
    processing_task.cancel()
    try:
        await processing_task
    except asyncio.CancelledError:
        pass


if __name__ == "__main__":
    asyncio.run(main())