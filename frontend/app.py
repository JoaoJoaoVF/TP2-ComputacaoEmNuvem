from flask import Flask, request, jsonify
from flask_cors import CORS
import dill as pickle
import logging

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['JSON_SORT_KEYS'] = False

MODEL_PATH = '/data/association_rules.pkl'

# Configuração do logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Função para carregar o modelo usando `dill`
def load_model(path):
    print('1')
    try:
        with open(path, 'rb') as file:
            model_data = pickle.load(file)
        logging.info("Modelo carregado com sucesso.")
        return model_data.get("rules", [])
    except Exception as e:
        logging.error(f"Erro ao carregar o modelo: {e}")
        return None

@app.route('/api/recommender', methods=['POST'])
def recommender():
    try:
        # Carregar o modelo
        rules_model = load_model(MODEL_PATH)
        if not rules_model:
            return jsonify({"error": "Erro ao carregar o modelo"}), 500

        # Validar entrada
        data = request.get_json()
        if not data or 'songs' not in data:
            raise ValueError("Dados inválidos: 'songs' é obrigatório.")

        songs = data['songs']
        if not isinstance(songs, list) or not all(isinstance(song, str) for song in songs):
            raise ValueError("A entrada 'songs' deve ser uma lista de strings.")

        # Gerar recomendações
        recommended_playlist = set()
        for rule in rules_model:
            rule_song_0 = list(rule[0])[0]
            rule_song_1 = list(rule[1])[0]

            for song in songs:
                if song == rule_song_0:
                    recommended_playlist.add(rule_song_1)
                elif song == rule_song_1:
                    recommended_playlist.add(rule_song_0)

        # Retornar resposta
        return jsonify({"playlist": list(recommended_playlist)}), 200

    except ValueError as ve:
        logging.warning(f"Erro de validação: {ve}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        logging.error(f"Erro interno do servidor: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=52035,
        debug=True
    )
