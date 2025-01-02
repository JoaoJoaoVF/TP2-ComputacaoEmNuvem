import requests
import json

def make_request():
    url = "http://localhost:52035/api/recommender"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "songs": ["Closer", "Let Me Love You", "Stronger"]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            print("Resposta da API:")
            print(response.json())
        else:
            print(f"Erro: {response.status_code}")
            print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer a requisição: {e}")

if __name__ == "__main__":
    make_request()
