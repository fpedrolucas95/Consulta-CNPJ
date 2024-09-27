import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from database import DatabaseConnection
from leitor_cnpj import ler_cnpjs
from api_cliente import consultar_api_com_retries
from extrator_dados import extrair_dados

logging.basicConfig(
    filename='cnpj_consulta.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

def processar_cnpjs(arquivo_cnpjs: str):
    lista_cnpjs = ler_cnpjs(arquivo_cnpjs)
    batch_size = 3
    total_cnpjs = len(lista_cnpjs)
    for i in range(0, total_cnpjs, batch_size):
        batch = lista_cnpjs[i:i+batch_size]
        with ThreadPoolExecutor(max_workers=batch_size) as executor:
            future_to_cnpj = {executor.submit(processar_cnpj, cnpj): cnpj for cnpj in batch}
            for future in as_completed(future_to_cnpj):
                cnpj = future_to_cnpj[future]
                try:
                    future.result()
                except Exception as e:
                    logging.error(f'Erro ao processar o CNPJ {cnpj}: {e}')
        if i + batch_size < total_cnpjs:
            logging.info('Aguardando 60 segundos para respeitar o limite da API.')
            time.sleep(60)

def processar_cnpj(cnpj: str):
    try:
        data = consultar_api_com_retries(cnpj)
        if data:
            dados_extraidos = extrair_dados(data)
            db = DatabaseConnection()
            db.criar_tabela()
            try:
                db.inserir_no_banco(dados_extraidos)
            finally:
                db.close()
        else:
            logging.error(f'Falha na consulta do CNPJ {cnpj}.')
    except Exception as e:
        logging.error(f'Erro ao processar o CNPJ {cnpj}: {e}')

if __name__ == '__main__':
    from gui import AppGUI
    app = AppGUI()
    app.run()
