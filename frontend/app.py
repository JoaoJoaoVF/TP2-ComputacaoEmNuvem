from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import dill as pickle
from dataclasses import dataclass
import logging

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['JSON_SORT_KEYS'] = False

MODEL_PATH = '/data/association_rules.pkl'

# Configuração do logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@dataclass
class CustomModel:
    rules: list
    model_date: str = None

def load_model(path):
    print('a')
    try:
        with open(model_path, 'wb') as file:
            pickle.dump(custom_model, file) 
    except Exception as e:
        logging.error(f"Erro ao carregar o modelo: {e}")
        return None

# Carregando o modelo no início da aplicação
custom_model = load_model(MODEL_PATH)

def get_recommendations(songs, custom_model):
    if not custom_model or not custom_model.rules:
        raise ValueError("Modelo não está disponível ou é inválido.")

    recommended_playlist = set()
    model = custom_model.rules

    for rule in model:
        rule_song_0 = list(rule[0])[0]
        rule_song_1 = list(rule[1])[0]

        for song in songs:
            if song == rule_song_0:
                recommended_playlist.add(rule_song_1)
            elif song == rule_song_1:
                recommended_playlist.add(rule_song_0)

    return list(recommended_playlist)

@app.route('/api/recommender', methods=['POST'])
def recommender():
    try:
        data = request.get_json()

        if not data or 'songs' not in data:
            raise ValueError("Dados inválidos: 'songs' é obrigatório.")

        songs = data['songs']
        if not isinstance(songs, list) or not all(isinstance(song, str) for song in songs):
            raise ValueError("A entrada 'songs' deve ser uma lista de strings.")

        recommended_playlist = get_recommendations(songs, custom_model)

        response = {
            "playlist": recommended_playlist,
        }

        return make_response(jsonify(response), 200)

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
