# strategies.py
"""
Padrao de Comportamento: Strategy
----------------------------------
Implementa diferentes estrategias de ordenacao de tarefas.

O padrao Strategy permite selecionar um algoritmo em tempo de execucao
sem que o cliente precise conhecer os detalhes de implementacao.

Referencia: GoF "Behavioral Patterns" - Strategy (p.315-323)
"""

from abc import ABC, abstractmethod
from datetime import datetime


# ----------- Interface Strategy (abstrata) --------------

class SortStrategy(ABC):
    """
    Interface abstrata para estrategias de ordenacao.
    Define o contrato que todas as estrategias concretas devem seguir.
    """
    
    @abstractmethod
    def sort(self, tasks: list) -> list:
        """
        Ordena uma lista de tarefas segundo a estrategia implementada.
        
        Args:
            tasks: Lista de objetos Task
            
        Returns:
            Lista de tarefas ordenada
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Retorna o nome da estrategia."""
        pass


# ----------- Estrategias Concretas --------------------------

class PrioritySortStrategy(SortStrategy):
    """
    Estrategia: Ordena tarefas por prioridade (maior prioridade primeiro).
    
    Tarefas com prioridade aparecem primeiro.
    Tarefas sem prioridade (SimpleTask, DeadlineTask) aparecem depois.
    """
    
    def sort(self, tasks: list) -> list:
        def priority_key(task):
            # Se tem atributo priority, usa-o; senao, prioridade 0
            return getattr(task, 'priority', 0)
        
        # Ordena descendente (maior prioridade primeiro)
        return sorted(tasks, key=priority_key, reverse=True)
    
    def get_name(self) -> str:
        return "priority"


class DeadlineSortStrategy(SortStrategy):
    """
    Estrategia: Ordena tarefas por deadline (mais urgente primeiro).
    
    Tarefas com deadline aparecem primeiro (ordenadas por urgencia).
    Tarefas sem deadline aparecem depois.
    """
    
    def sort(self, tasks: list) -> list:
        def deadline_key(task):
            # Se tem deadline, usa-o; senao, data muito distante (aparece no fim)
            if hasattr(task, 'deadline'):
                return task.deadline
            else:
                # Data muito no futuro para aparecer no fim
                return datetime(2099, 12, 31)
        
        # Ordena ascendente (deadline mais proximo primeiro)
        return sorted(tasks, key=deadline_key)
    
    def get_name(self) -> str:
        return "deadline"


class CreationSortStrategy(SortStrategy):
    """
    Estrategia: Ordena tarefas por data de criacao (mais recente primeiro).
    
    Tarefas criadas mais recentemente aparecem primeiro.
    """
    
    def sort(self, tasks: list) -> list:
        # Ordena descendente (mais recente primeiro)
        return sorted(tasks, key=lambda task: task.created_at, reverse=True)
    
    def get_name(self) -> str:
        return "creation"


class DefaultSortStrategy(SortStrategy):
    """
    Estrategia: Sem ordenacao especifica (ordem de insercao).
    
    Retorna tarefas na ordem em que foram criadas/adicionadas.
    """
    
    def sort(self, tasks: list) -> list:
        # Retorna lista sem alterar ordem
        return list(tasks)
    
    def get_name(self) -> str:
        return "default"


# ----------- Context (Gerenciador de Estrategias) --------------

class TaskSorter:
    """
    Context do padrao Strategy.
    
    Permite selecionar e aplicar diferentes estrategias de ordenacao
    sem que o cliente precise conhecer detalhes de implementacao.
    """
    
    # Mapeamento de nome -> estrategia
    _strategies = {
        "priority": PrioritySortStrategy(),
        "deadline": DeadlineSortStrategy(),
        "creation": CreationSortStrategy(),
        "default": DefaultSortStrategy()
    }
    
    def __init__(self, strategy_name: str = "default"):
        """
        Inicializa o sorter com uma estrategia.
        
        Args:
            strategy_name: Nome da estrategia ("priority", "deadline", "creation", "default")
        """
        self.set_strategy(strategy_name)
    
    def set_strategy(self, strategy_name: str):
        """
        Define a estrategia de ordenacao a ser usada.
        
        Args:
            strategy_name: Nome da estrategia
        """
        strategy = self._strategies.get(strategy_name.lower())
        
        if strategy is None:
            # Se estrategia nao existe, usa default
            strategy = self._strategies["default"]
        
        self._strategy = strategy
    
    def sort(self, tasks: list) -> list:
        """
        Aplica a estrategia atual para ordenar tarefas.
        
        Args:
            tasks: Lista de tarefas
            
        Returns:
            Lista ordenada segundo estrategia atual
        """
        return self._strategy.sort(tasks)
    
    def get_current_strategy_name(self) -> str:
        """Retorna nome da estrategia atual."""
        return self._strategy.get_name()
    
    @classmethod
    def get_available_strategies(cls) -> list:
        """
        Retorna lista de estrategias disponiveis.
        
        Returns:
            Lista com nomes das estrategias
        """
        return list(cls._strategies.keys())