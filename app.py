from flask import Flask, jsonify, request
from facade import tasktrack_facade


# ============================================================================
# REFATORIZAÇÃO 1: Eliminação do antipadrão "Cut-and-Paste Programming"
# ============================================================================

def get_request_json():
    """
    Helper function para extrair JSON do request.
    
    Refatorização do antipadrão Cut-and-Paste Programming:
    - Elimina duplicação de código
    - Centraliza lógica de parsing de JSON
    - Facilita manutenção (DRY principle)
    
    Returns:
        dict: JSON do request ou dicionário vazio se inválido
    """
    return request.get_json(silent=True) or {}


# ============================================================================
# REFATORIZAÇÃO 3: Eliminação do antipadrão "Functional Decomposition"
# ============================================================================
# ANTES: Funções procedimentais soltas (programação procedimental em OOP)
# DEPOIS: Classe Controller com métodos (programação orientada a objetos)
#
# Benefícios:
# - Segue paradigma OOP (não procedimental)
# - Facilita injeção de dependências (testabilidade)
# - Agrupa lógica relacionada numa classe coesa
# - Permite reutilização e herança se necessário
# ============================================================================


class TaskTrackController:
    """
    Controller responsável pela lógica de controlo dos endpoints.
    
    Refatorização do antipadrão "Functional Decomposition":
    - ANTES: Funções procedimentais soltas (config_page, deploy_activity, etc)
    - DEPOIS: Métodos organizados numa classe Controller (OOP)
    
    Responsabilidades:
    - Receber pedidos HTTP
    - Validar/processar inputs
    - Delegar lógica de negócio à Facade
    - Formatar respostas
    """
    
    def __init__(self, facade):
        """
        Inicializa o controller com a facade.
        
        Args:
            facade: Instância da TaskTrackFacade
        """
        self.facade = facade
    
    def home(self):
        """Retorna página inicial do AP."""
        return "<h1>TaskTrack-AP esta a correr!</h1><p>Use os endpoints /tasktrack/... para testar.</p>"
    
    def config_page(self):
        """Retorna página de configuração (mock para Inven!RA)."""
        html = """
        <html>
          <head>
            <title>TaskTrack-AP - Configuracao</title>
          </head>
          <body>
            <h1>Configuracao da atividade TaskTrack-AP (TESTE)</h1>
            <p>Esta pagina e apenas um mock para integracao com a Inven!RA.</p>
          </body>
        </html>
        """
        return html
    
    def json_params(self):
        """Retorna parâmetros configuráveis da atividade."""
        data = {
            "activity": "TaskTrack-AP",
            "description": "Mini aplicacao de gestao de tarefas com tempo limite.",
            "params": [
                {"name": "max_tasks", "type": "integer", "label": "Numero maximo de tarefas", "default": 5, "min": 1, "max": 20},
                {"name": "time_limit_minutes", "type": "integer", "label": "Tempo limite (minutos)", "default": 30, "min": 5, "max": 180},
                {"name": "allow_reorder", "type": "boolean", "label": "Permitir reordenar tarefas", "default": True}
            ]
        }
        return data
    
    def deploy_activity(self):
        """
        Deploy de atividade para um aluno.
        Usa helper get_request_json() (refatorização Cut-and-Paste).
        """
        data = get_request_json()
        response = self.facade.deploy_activity(data)
        return response
    
    def analytics_list(self):
        """Lista tipos de analytics disponíveis."""
        return self.facade.analytics_list()
    
    def analytics(self):
        """
        Gera analytics para atividade/utilizador.
        Usa helper get_request_json() (refatorização Cut-and-Paste).
        """
        body = get_request_json()
        response = self.facade.generate_analytics(
            activity_id=body.get("activityID", "activity-123"),
            user_id=body.get("userID", "user-abc")
        )
        return response
    
    def list_tasks(self):
        """Lista tarefas com ordenação via Strategy Pattern."""
        sort_by = request.args.get("sort_by", "default")
        response = self.facade.list_tasks(sort_by=sort_by)
        return response
    
    def sort_strategies(self):
        """Lista estratégias de ordenação disponíveis."""
        return self.facade.get_sort_strategies()


# ============================================================================
# Inicialização da aplicação Flask
# ============================================================================

app = Flask(__name__)

# Instanciar o controller (injeção de dependência)
controller = TaskTrackController(tasktrack_facade)


# ============================================================================
# Definição de rotas (endpoints)
# ============================================================================
# As rotas agora delegam para métodos do Controller
# Mantém-se a estrutura Flask mas com lógica encapsulada em OOP
# ============================================================================

@app.route("/")
def home():
    return controller.home()


@app.route("/tasktrack/config", methods=["GET"])
def config_page():
    return controller.config_page()


@app.route("/tasktrack/json-params", methods=["GET"])
def json_params():
    return jsonify(controller.json_params())


@app.route("/tasktrack/deploy", methods=["POST"])
def deploy_activity():
    return jsonify(controller.deploy_activity())


@app.route("/tasktrack/analytics-list", methods=["GET"])
def analytics_list():
    return jsonify(controller.analytics_list())


@app.route("/tasktrack/analytics", methods=["POST"])
def analytics():
    return jsonify(controller.analytics())


@app.route("/tasktrack/tasks", methods=["GET"])
def list_tasks():
    return jsonify(controller.list_tasks())


@app.route("/tasktrack/sort-strategies", methods=["GET"])
def sort_strategies():
    return jsonify(controller.sort_strategies())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)