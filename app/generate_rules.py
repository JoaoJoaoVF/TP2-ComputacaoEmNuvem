import pandas as pd
from fpgrowth_py import fpgrowth
import pickle
import time
from mlxtend.preprocessing import TransactionEncoder
import datetime
import os
import logging

# Configuração do logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Constantes
MIN_SUP_RATIO = 0.05  # Reduzido para facilitar a detecção de conjuntos frequentes
MIN_CONF = 0.1
DATA_PATH = 'data/2023_spotify_ds1.csv'
MODEL_PATH = 'association_rules.pkl'

class CustomModel:
    def __init__(self, rules):
        self.rules = rules
        self.model_date = None

def print_time_elapsed(start_time, message):
    elapsed_time = time.time() - start_time
    logging.info(f"{message} - Tempo decorrido: {elapsed_time:.2f} segundos")

def load_data(file_path):
    """
    Carrega e valida o arquivo CSV.
    """
    if not os.path.exists(file_path):
        logging.error(f"Arquivo não encontrado: {file_path}")
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

    logging.info(f"Carregando dados de {file_path}...")
    df = pd.read_csv(file_path)

    if 'pid' not in df.columns or 'track_name' not in df.columns:
        raise ValueError("O DataFrame deve conter as colunas 'pid' e 'track_name'.")
    
    return df

def generate_playlists(df):
    """
    Gera listas de playlists agrupando por 'pid'.
    """
    playlists = df.groupby('pid')['track_name'].apply(list).tolist()
    logging.info(f"Total de playlists geradas: {len(playlists)}")
    return playlists

def train_model(playlists):
    """
    Executa o algoritmo FP-Growth e retorna as regras encontradas.
    """
    logging.info("Executando o algoritmo FP-Growth...")
    _itemSet, rules = fpgrowth(playlists, MIN_SUP_RATIO, MIN_CONF)

    if rules is None or _itemSet is None:
        logging.warning("Nenhum conjunto frequente ou regra encontrada.")
        return None

    return rules

def save_model(rules, model_path):
    """
    Salva o modelo treinado em um arquivo pickle.
    """
    logging.info("Salvando modelo...")
    custom_model = CustomModel(rules)
    custom_model.model_date = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

    with open(model_path, 'wb') as file:
        pickle.dump(custom_model, file)

def main():
    start_time = time.time()
    try:
        # Carregando dados
        df = load_data(DATA_PATH)
        print_time_elapsed(start_time, "Dados carregados")

        # Gerando playlists
        playlists = generate_playlists(df)
        print_time_elapsed(start_time, "Playlists geradas")

        # Treinando o modelo
        rules = train_model(playlists)
        print_time_elapsed(start_time, "Modelo treinado")

        if rules is None:
            logging.error("Nenhuma regra encontrada. Encerrando execução.")
            return

        # Salvando o modelo
        save_model(rules, MODEL_PATH)
        logging.info(f"Modelo salvo em {MODEL_PATH}")

    except Exception as e:
        logging.error(f"Erro durante a execução: {e}")
    finally:
        print_time_elapsed(start_time, "Execução concluída")

if __name__ == "__main__":
    main()
