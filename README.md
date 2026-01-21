TaskTrack-AP - Activity Provider

Sistema de gestão de tarefas para plataforma Inven!RA desenvolvido no âmbito da unidade curricular de Arquitetura e Padrões de Software.

Padrões de Design Implementados

Padrões GoF
- Factory Method (Criação): Criação polimórfica de diferentes tipos de tarefas
- Facade Pattern (Estrutural): Interface simplificada para coordenação de subsistemas
- Strategy Pattern (Comportamental): Algoritmos intercambiáveis de ordenação de tarefas

Padrões Adicionais (Refatorização)
- Repository Pattern: Separação de responsabilidades entre lógica de negócio e persistência

Antipadrões Refatorizados

1. The Blob (tasks.py)
Problema Identificado:
- TaskManager acumulava múltiplas responsabilidades (criação + armazenamento + coordenação)
- Violação do Single Responsibility Principle (SRP)

olução Aplicada:
- Criação da classe `TaskRepository` dedicada exclusivamente ao armazenamento
- `TaskManager` refatorado para responsabilidade única de coordenação
- Delegação explícita de armazenamento ao Repository

Benefícios:
-  SRP respeitado
-  Testabilidade melhorada (Repository mockável)
-  Facilita substituição do mecanismo de persistência

2. Functional Decomposition (app.py)
Problema Identificado:
- Estrutura puramente procedimental (funções globais soltas)
- Impossibilidade de injeção de dependências
- Dificuldade de testes unitários

Solução Aplicada:
- Criação da classe `TaskTrackController` (padrão MVC)
- Encapsulamento da lógica de controlo em métodos organizados
- Injeção de dependência da Facade via construtor

Benefícios:
-  Paradigma OOP respeitado
-  Testável sem servidor Flask ativo
-  Coesão melhorada

3. Cut-and-Paste Programming (app.py)
Problema Identificado:
- Código duplicado: `request.get_json(silent=True) or {}` repetido em múltiplos endpoints
- Violação do princípio DRY (Don't Repeat Yourself)

Solução Aplicada:
- Extração de função helper `get_request_json()`
- Reutilização em todos os endpoints que necessitam parsing JSON

Benefícios:
-  DRY respeitado
-  Manutenção centralizada
-  Consistência garantida

Instalação e Execução

Requisitos
- Python 3.8+
- pip

Setup
bash
Clonar repositório
git clone https://github.com/singletrack83/tasktrack-ap.git
cd tasktrack-ap

Criar ambiente virtual (opcional mas recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

Instalar dependências
pip install -r requirements.txt

Executar servidor de desenvolvimento
flask --app app run --debug
```

O servidor estará disponível em `http://localhost:5000`

Endpoints API

Configuração

GET  /                              - Página inicial
GET  /tasktrack/config              - Interface de configuração
GET  /tasktrack/json-params         - Parâmetros configuráveis em JSON


Operações de Tarefas

POST /tasktrack/deploy              - Criar nova tarefa
     Body: {
       "task_type": "simple|priority|deadline",
       "title": "Nome da tarefa",
       "priority": 1-5,              (opcional, para PriorityTask)
       "minutes_from_now": 30        (opcional, para DeadlineTask)
     }

GET  /tasktrack/tasks               - Listar todas as tarefas (ordenação default)
GET  /tasktrack/tasks?sort_by=X     - Listar com ordenação específica
     Valores de X: priority | deadline | creation | default


Strategy Pattern

GET  /tasktrack/sort-strategies     - Listar estratégias de ordenação disponíveis

Analytics

GET  /tasktrack/analytics-list      - Tipos de analytics disponíveis
POST /tasktrack/analytics           - Gerar analytics para atividade
     Body: {
       "activityID": "...",
       "userID": "..."
     }


Validação

Todos os endpoints foram testados após refatorização:
-  Factory Method funcional (criação de 3 tipos de tarefas)
-  Facade Pattern funcional (coordenação de subsistemas)
-  Strategy Pattern funcional (4 estratégias de ordenação)
-  Repository Pattern funcional (armazenamento isolado)
-  Sem regressões detectadas
-  100% dos testes funcionais passaram

Estrutura do Projeto

tasktrack-ap/
├── app.py              # Endpoints Flask + Controller (refatorizado)
├── facade.py           # Facade Pattern (coordenação)
├── strategies.py       # Strategy Pattern (algoritmos de ordenação)
├── tasks.py            # Factory Method + Repository (refatorizado)
├── requirements.txt    # Dependências Python
└── README.md          # Este ficheiro


Princípios SOLID Aplicados

- S - Single Responsibility: Cada classe tem uma única responsabilidade
- O - Open/Closed: Extensível sem modificação (novos tipos de Task, novas Strategies)
- L - Liskov Substitution: Subclasses substituíveis (Tasks, Strategies)
- I - Interface Segregation: Interfaces específicas e coesas
- D - Dependency Inversion: Dependências via abstração (injeção de Facade, Repository)

Referências

- Brown, W. H., et al. (1998). *AntiPatterns: Refactoring Software, Architectures, and Projects in Crisis*. Wiley.
- Gamma, E., et al. (1995). *Design Patterns: Elements of Reusable Object-Oriented Software*. Addison-Wesley.
- Fowler, M. (1999). *Refactoring: Improving the Design of Existing Code*. Addison-Wesley.
- Martin, R. C. (2008). *Clean Code: A Handbook of Agile Software Craftsmanship*. Prentice Hall.

Autor

Pedro Miguel de Almeida Neves Pires  
Estudante nº 2202741  
Mestrado em Engenharia Informática e Tecnologia Web  
Universidade Aberta  
Unidade Curricular: Arquitetura e Padrões de Software (22304)
