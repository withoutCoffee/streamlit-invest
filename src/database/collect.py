# fazer download de arquivo de ações da bolsa por link https://sistemaswebb3-listados.b3.com.br/indexPage/day/IBOV?language=pt-br
# fazer download apenas se já fez 5 dias que fez o último download

# salvar na pasta data/IBOVDia_03-10-25.csv
import os
import datetime
import requests

def download_ibov_tickers(url, save_path):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica se a requisição foi bem-sucedida

        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Arquivo baixado com sucesso e salvo em: {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar o arquivo: {e}")
