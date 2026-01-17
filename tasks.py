# tasks.py
"""
Módulo de domínio para o TaskTrack-AP.
Implementa:
- Factory Method para criar diferentes tipos de tarefas
- Repository Pattern para armazenamento (refatorização do antipadrão The Blob)
"""

from datetime import datetime, timedelta


# ----------- Classe base (Produto abstrato) --------------

class Task:
    def __init__(self, title: str):
        self.title = title
        self.created_at = datetime.utcnow()
        self.done = False

    def to_dict(self):
        """Representação simples em dicionário (para devolver em JSON)."""
        return {
            "type": self.__class__.__name__,
            "title": self.title,
            "created_at": self.created_at.isoformat() + "Z",
            "done": self.done,
        }


# ----------- Produtos concretos --------------------------

class SimpleTask(Task):
    """Tarefa simples, sem prioridade nem prazo."""
    pass


class PriorityTask(Task):
    """Tarefa com nível de prioridade."""
    def __init__(self, title: str, priority: int):
        super().__init__(title)
        self.priority = priority

    def to_dict(self):
        data = super().to_dict()
        data["priority"] = self.priority
        return data


class DeadlineTask(Task):
    """Tarefa com prazo (deadline)."""
    def __init__(self, title: str, minutes_from_now: int):
        super().__init__(title)
        self.deadline = self.created_at + timedelta(minutes=minutes_from_now)

    def to_dict(self):
        data = super().to_dict()
        data["deadline"] = self.deadline.isoformat() + "Z"
        return data


# ----------- Factory Method -------------------------------

class TaskFactory:
    """
    Factory Method responsável por criar objetos Task.
    Encapsula a lógica de decisão do tipo concreto de tarefa.
    """

    def create_task(self, task_type: str, **kwargs) -> Task:
        task_type = (task_type or "").lower()

        if task_type == "simple":
            return SimpleTask(kwargs["title"])

        if task_type == "priority":
            return PriorityTask(
                kwargs["title"],
                int(kwargs.get("priority", 1))
            )

        if task_type == "deadline":
            return DeadlineTask(
                kwargs["title"],
                int(kwargs.get("minutes_from_now", 30))
            )

        # fallback padrão
        return SimpleTask(kwargs["title"])


# ============================================================================
# REFATORIZAÇÃO 2: Eliminação do antipadrão "The Blob"
# ============================================================================
# ANTES: TaskManager tinha múltiplas responsabilidades (criação + armazenamento)
# DEPOIS: Responsabilidades divididas em classes específicas
#
# TaskRepository: Responsável APENAS por armazenamento e recuperação de tarefas
# TaskManager: Responsável APENAS por coordenar criação e delegação
#
# Benefícios:
# - Single Responsibility Principle (SRP) respeitado
# - Cada classe tem uma única razão para mudar
# - Facilita testes unitários
# - Melhora manutenibilidade
# ============================================================================


class TaskRepository:
    """
    Repository Pattern: Responsável exclusivamente pelo armazenamento de tarefas.
    
    Refatorização do antipadrão "The Blob":
    - ANTES: TaskManager fazia criação + armazenamento
    - DEPOIS: TaskRepository só armazena, TaskManager só coordena
    
    Responsabilidade única: Gerir a coleção de tarefas (CRUD básico)
    """
    
    def __init__(self):
        self._tasks: list[Task] = []
    
    def add(self, task: Task) -> None:
        """Adiciona uma tarefa ao repositório."""
        self._tasks.append(task)
    
    def get_all(self) -> list[Task]:
        """Retorna todas as tarefas armazenadas."""
        return self._tasks.copy()
    
    def count(self) -> int:
        """Retorna o número de tarefas armazenadas."""
        return len(self._tasks)


class TaskManager:
    """
    Coordena a criação e gestão de tarefas.
    
    REFATORADO: Agora delega armazenamento ao TaskRepository.
    Responsabilidade única: Coordenar criação de tarefas via Factory.
    """

    def __init__(self):
        self.factory = TaskFactory()
        self.repository = TaskRepository()

    def create_task(self, task_type: str, **kwargs) -> Task:
        """
        Cria uma nova tarefa usando Factory Method e armazena no Repository.
        
        Refatoração:
        - Criação: Delegada ao TaskFactory
        - Armazenamento: Delegado ao TaskRepository
        - TaskManager apenas coordena ambos
        """
        task = self.factory.create_task(task_type, **kwargs)
        self.repository.add(task)
        return task

    def list_tasks(self) -> list[dict]:
        """Retorna todas as tarefas em formato dicionário."""
        return [t.to_dict() for t in self.repository.get_all()]
    
    @property
    def tasks(self) -> list[Task]:
        """
        Property para manter compatibilidade com código existente.
        Retorna todas as tarefas do repositório.
        """
        return self.repository.get_all()


# Instância global usada pelo AP
task_manager = TaskManager()