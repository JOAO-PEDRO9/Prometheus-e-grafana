from flask import Flask, request, jsonify
from prometheus_client import Counter, Summary, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Métricas Prometheus
REQUEST_COUNT = Counter('request_count', 'Contagem de requisições', ['method', 'endpoint', 'http_status'])
REQUEST_LATENCY = Summary('request_latency_seconds', 'Tempo de resposta por rota', ['endpoint'])
ERROR_COUNT = Counter('error_count', 'Contador de erros', ['endpoint'])

# Endpoints
@app.route('/health', methods=['GET'])
def health():
    REQUEST_COUNT.labels(method='GET', endpoint='/health', http_status='200').inc()
    return jsonify({"status": "ok"})

@app.route('/books', methods=['GET'])
@REQUEST_LATENCY.labels(endpoint='/books').time()
def get_books():
    books = [{"id": 1, "title": "1984"}, {"id": 2, "title": "Brave New World"}]
    REQUEST_COUNT.labels(method='GET', endpoint='/books', http_status='200').inc()
    return jsonify(books)

@app.route('/books', methods=['POST'])
@REQUEST_LATENCY.labels(endpoint='/books').time()
def add_book():
    if not request.is_json:
        ERROR_COUNT.labels(endpoint='/books').inc()
        REQUEST_COUNT.labels(method='POST', endpoint='/books', http_status='400').inc()
        return jsonify({"error": "Invalid input"}), 400

    REQUEST_COUNT.labels(method='POST', endpoint='/books', http_status='201').inc()
    return jsonify({"message": "Livro adicionado com sucesso!"}), 201

@app.route('/metrics', methods=['GET'])
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
