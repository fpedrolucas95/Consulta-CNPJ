import logging
import requests
from typing import Optional
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

API_URL = 'https://publica.cnpj.ws/cnpj/{}'

def consultar_api_com_retries(cnpj: str, max_retries: int = 3) -> Optional[dict]:
    session = requests.Session()
    retries = Retry(
        total=max_retries,
        backoff_factor=60,
        status_forcelist=[429],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('https://', adapter)
    url = API_URL.format(cnpj)
    try:
        response = session.get(url)
        if response.status_code == 200:
            logging.info(f'Sucesso na consulta do CNPJ {cnpj}.')
            return response.json()
        else:
            logging.error(f'Erro {response.status_code} na consulta do CNPJ {cnpj}: {response.text}')
            return None
    except Exception as e:
        logging.error(f'Erro ao consultar a API para o CNPJ {cnpj}: {e}')
        return None
