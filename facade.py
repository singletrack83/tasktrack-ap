# facade.py
"""
Padrao Estrutural: Facade com Strategy Pattern
"""

from tasks import task_manager
from strategies import TaskSorter


class TaskTrackFacade:
    
    def __init__(self):
        self.sorter = TaskSorter()

    def deploy_activity(self, request_data: dict) -> dict:
        title = request_data.get("title", "Tarefa inicial do plano")
        task_type = request_data.get("task_type", "simple")

        task = task_manager.create_task(
            task_type,
            title=title,
            priority=request_data.get("priority", 1),
            minutes_from_now=request_data.get("minutes_from_now", 30),
        )

        return {
            "status": "ok",
            "message": "Deploy realizado via Facade + Factory Method.",
            "created_task": task.to_dict(),
        }

    def list_tasks(self, sort_by: str = "default") -> dict:
        self.sorter.set_strategy(sort_by)
        all_tasks = task_manager.tasks
        sorted_tasks = self.sorter.sort(all_tasks)
        tasks_dict = [task.to_dict() for task in sorted_tasks]
        
        return {
            "tasks": tasks_dict,
            "count": len(tasks_dict),
            "sorted_by": self.sorter.get_current_strategy_name()
        }

    def get_sort_strategies(self) -> dict:
        return {
            "available_strategies": TaskSorter.get_available_strategies(),
            "description": {
                "priority": "Ordena por prioridade (maior primeiro)",
                "deadline": "Ordena por deadline (mais urgente primeiro)",
                "creation": "Ordena por data de criacao (mais recente primeiro)",
                "default": "Ordem de insercao (sem ordenacao)"
            }
        }

    def analytics_list(self) -> dict:
        return {
            "activity": "TaskTrack-AP",
            "analytics": [
                {"name": "tasks_created", "label": "Tarefas criadas", "type": "integer"},
                {"name": "tasks_completed", "label": "Tarefas concluidas", "type": "integer"},
                {"name": "tasks_completed_on_time", "label": "Concluidas dentro do prazo", "type": "integer"},
                {"name": "total_time_minutes", "label": "Tempo total (minutos)", "type": "number"},
                {"name": "completion_rate", "label": "Taxa de conclusao (%)", "type": "number"}
            ]
        }

    def generate_analytics(self, activity_id: str, user_id: str) -> dict:
        return {
            "activityID": activity_id,
            "userID": user_id,
            "metrics": {
                "tasks_created": 5,
                "tasks_completed": 4,
                "tasks_completed_on_time": 3,
                "total_time_minutes": 27.5,
                "completion_rate": 80.0
            }
        }


tasktrack_facade = TaskTrackFacade()