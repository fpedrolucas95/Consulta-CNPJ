import logging

def extrair_dados(data: dict) -> dict:
    try:
        estabelecimento = data.get('estabelecimento', {})
        inscricoes_estaduais = estabelecimento.get('inscricoes_estaduais', [])
        inscricao_estadual = (
            inscricoes_estaduais[0]['inscricao_estadual'] if inscricoes_estaduais else None
        )
        telefone = f"{estabelecimento.get('ddd1', '')}{estabelecimento.get('telefone1', '')}"
        dados_extraidos = {
            'cnpj': estabelecimento.get('cnpj'),
            'inscricao_estadual': inscricao_estadual,
            'razao_social': data.get('razao_social'),
            'nome': data.get('nome_fantasia'),
            'nome_fantasia': estabelecimento.get('nome_fantasia'),
            'logradouro': f"{estabelecimento.get('tipo_logradouro', '')} {estabelecimento.get('logradouro', '')}, {estabelecimento.get('numero', '')}",
            'cep': estabelecimento.get('cep'),
            'uf': estabelecimento.get('estado', {}).get('sigla'),
            'telefone': telefone,
            'email': estabelecimento.get('email'),
        }
        logging.info(f'Dados extraídos para o CNPJ {dados_extraidos["cnpj"]}.')
        return dados_extraidos
    except Exception as e:
        logging.error(f'Erro ao extrair dados: {e}')
        raise
