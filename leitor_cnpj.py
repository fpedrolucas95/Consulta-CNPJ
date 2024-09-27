import logging
import pandas as pd
import re

def ler_cnpjs(arquivo_excel: str) -> list:
    try:
        df = pd.read_excel(arquivo_excel, header=0, dtype=str)
        cnpj_coluna = df.columns[0]
        cnpjs_raw = df[cnpj_coluna].astype(str).tolist()
        cnpjs_normalizados = []
        for cnpj in cnpjs_raw:
            cnpj_normalizado = normalizar_cnpj(cnpj)
            if validar_cnpj(cnpj_normalizado):
                cnpjs_normalizados.append(cnpj_normalizado)
            else:
                logging.warning(f'CNPJ inválido ignorado: {cnpj}')
        logging.info('Planilha de CNPJs carregada e normalizada com sucesso.')
        return cnpjs_normalizados
    except Exception as e:
        logging.error(f'Erro ao ler a planilha de CNPJs: {e}')
        raise

def normalizar_cnpj(cnpj_str: str) -> str:
    cnpj_str = re.sub(r'\D', '', cnpj_str)
    if 'E' in cnpj_str.upper():
        try:
            cnpj_float = float(cnpj_str.replace(',', '.'))
            cnpj_int = int(cnpj_float)
            cnpj_str = str(cnpj_int)
        except ValueError:
            logging.error(f'Erro ao converter CNPJ de notação científica: {cnpj_str}')
            cnpj_str = ''
    cnpj_str = cnpj_str.zfill(14)
    cnpj_str = cnpj_str[:14]
    return cnpj_str

def validar_cnpj(cnpj_str: str) -> bool:
    return len(cnpj_str) == 14 and cnpj_str.isdigit()
