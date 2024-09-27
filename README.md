# Consulta CNPJ

**Consulta CNPJ** é um aplicativo em Python que permite consultar, processar e exibir dados detalhados de empresas a partir de seus CNPJs. Ele utiliza uma API pública para extrair informações como razão social, endereço, telefone, e-mail e muito mais, exibindo os resultados em uma interface gráfica fácil de usar.

## Funcionalidades

- Seleção de arquivo com lista de CNPJs em Excel.
- Consulta de CNPJs em lotes, utilizando uma API pública de CNPJ.
- Extração de dados importantes, como telefone, e-mail, razão social e endereço.
- Exibição dos resultados em uma tabela visual na interface gráfica.
- Opção de copiar e excluir registros diretamente da tabela.

## Como Usar

1. Abra o aplicativo e clique em "Selecionar Arquivo" para escolher um arquivo Excel contendo uma lista de CNPJs.
2. Após a seleção do arquivo, clique em "Iniciar Consulta". O processamento iniciará, e um indicador de carregamento será exibido.
    - **Observação**: A API utilizada possui uma limitação de 3 requisições por minuto. Portanto, dependendo do tamanho da lista, o processo pode demorar um pouco para ser concluído.
4. Quando o processamento for concluído, os dados serão exibidos em uma tabela.
5. Clique com o botão direito em uma linha da tabela para copiar informações ou excluir um registro.

## Requisitos

- Python 3.8 ou superior
- MySQL
- Bibliotecas Python:
  - `mysql-connector-python`
  - `pandas`
  - `requests`
  - `tkinter`

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/usuario/consulta-cnpj.git
   ```
2. Crie um ambiente virtual e instale as dependências:

   ```bash
   python -m venv venv
   source venv/bin/activate   # No Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```
3. Configure o MySQL:
   - Crie um banco de dados chamado `cnpj_database`.
   - Defina as credenciais de conexão ao MySQL no arquivo `database.py`.

4. Execute o aplicativo:
   ```bash
   python main.py
   ```

## Estrutura do Projeto

```
├── main.py                 # Arquivo principal para rodar o aplicativo
├── gui.py                  # Interface gráfica construída com Tkinter
├── database.py             # Conexão e interações com o banco de dados MySQL
├── api_client.py           # Módulo para lidar com as requisições à API de CNPJ
├── cnpj_reader.py          # Leitura dos CNPJs do arquivo Excel
├── data_extractor.py       # Extração de dados relevantes da resposta da API
└── requirements.txt        # Dependências do projeto
```

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença

Este projeto é licenciado sob a GNU General Public License v3.0 (GPL-3.0). Isso garante a você as seguintes liberdades:

- Utilizar o software para qualquer propósito.
- Modificar o software conforme suas necessidades.
- Compartilhar o software com outras pessoas.
- Distribuir suas próprias modificações.

Para mais detalhes, consulte o arquivo [LICENSE](https://github.com/usuario/consulta-cnpj/blob/main/LICENSE) no repositório do projeto.
