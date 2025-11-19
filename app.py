from flask import Flask, jsonify, request

app = Flask(__name__)

# Rota simples para testar se o servidor está vivo
@app.route("/")
def home():
    return "<h1>TaskTrack-AP está a correr!</h1><p>Use os endpoints /tasktrack/... para testar.</p>"


# 1) CONFIG - página de configuração (HTML simples de teste)
@app.route("/tasktrack/config", methods=["GET"])
def config_page():
    # Nesta fase basta devolver HTML de teste
    html = """
    <html>
      <head>
        <title>TaskTrack-AP - Configuração</title>
      </head>
      <body>
        <h1>Configuração da atividade TaskTrack-AP (TESTE)</h1>
        <p>Esta é apenas uma página de exemplo para a Inven!RA verificar que o serviço responde.</p>
        <p>Num projeto completo, aqui estaria o formulário real de configuração.</p>
      </body>
    </html>
    """
    return html


# 2) JSON PARAMS - descrição dos parâmetros de configuração
@app.route("/tasktrack/json-params", methods=["GET"])
def json_params():
    data = {
        "activity": "TaskTrack-AP",
        "description": "Mini aplicação de gestão de tarefas com tempo limite.",
        "params": [
            {
                "name": "max_tasks",
                "type": "integer",
                "label": "Número máximo de tarefas",
                "default": 5,
                "min": 1,
                "max": 20,
            },
            {
                "name": "time_limit_minutes",
                "type": "integer",
                "label": "Tempo limite (minutos)",
                "default": 30,
                "min": 5,
                "max": 180,
            },
            {
                "name": "allow_reorder",
                "type": "boolean",
                "label": "Permitir reordenar tarefas",
                "default": True,
            },
        ]
    }
    return jsonify(data)


# 3) DEPLOY - criar instância da atividade para um aluno/plano
@app.route("/tasktrack/deploy", methods=["POST"])
def deploy_activity():
    # Nesta fase, apenas fazemos eco dos dados recebidos
    body = request.get_json(silent=True) or {}

    # Valores que a Inven!RA normalmente enviaria (exemplo)
    activity_id = body.get("activityID", "activity-123")
    user_id = body.get("userID", "user-abc")
    plan_id = body.get("planID", "plan-xyz")

    response = {
        "status": "ok",
        "message": "Instância de TaskTrack-AP criada (exemplo).",
        "activityID": activity_id,
        "userID": user_id,
        "planID": plan_id,
        # Nesta fase ainda não implementamos o user_url
        "user_url": "https://example.com/tasktrack/user-not-implemented-yet"
    }
    return jsonify(response)


# 4) LISTA DE ANALYTICS DISPONÍVEIS
@app.route("/tasktrack/analytics-list", methods=["GET"])
def analytics_list():
    data = {
        "activity": "TaskTrack-AP",
        "analytics": [
            {
                "name": "tasks_created",
                "label": "Número de tarefas criadas",
                "type": "integer"
            },
            {
                "name": "tasks_completed",
                "label": "Número de tarefas concluídas",
                "type": "integer"
            },
            {
                "name": "tasks_completed_on_time",
                "label": "Tarefas concluídas dentro do prazo",
                "type": "integer"
            },
            {
                "name": "total_time_minutes",
                "label": "Tempo total gasto (minutos)",
                "type": "number"
            },
            {
                "name": "completion_rate",
                "label": "Taxa de conclusão (%)",
                "type": "number"
            }
        ]
    }
    return jsonify(data)


# 5) PEDIDO DE ANALYTICS
@app.route("/tasktrack/analytics", methods=["POST"])
def analytics():
    body = request.get_json(silent=True) or {}

    activity_id = body.get("activityID", "activity-123")
    user_id = body.get("userID", "user-abc")

    # Dados de exemplo (mock) – depois podem ser reais
    data = {
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
    return jsonify(data)


# Código para correr localmente em modo de desenvolvimento
if __name__ == "__main__":
    # host="0.0.0.0" permite que Render/containers acedam
    app.run(host="0.0.0.0", port=5000, debug=True)