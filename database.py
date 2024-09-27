import logging
import mysql.connector
from mysql.connector import Error
 
DB_HOST = 'localhost'
DB_USER = 'cnpj_user' # atualize com o seu user da database
DB_PASSWORD = 'senha_segura123' # atualize com a senha da sua database
DB_DATABASE = 'cnpj_database' # altere para a database a ser utilizada

class DatabaseConnection:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        if self.connection is None or not self.connection.is_connected():
            try:
                self.connection = mysql.connector.connect(
                    host=DB_HOST,
                    user=DB_USER,
                    password=DB_PASSWORD,
                    database=DB_DATABASE
                )
                logging.info('Conexão com o banco de dados estabelecida.')
            except Error as e:
                logging.error(f'Erro ao conectar ao banco de dados: {e}')
                raise

    def close(self):
        if self.connection is not None and self.connection.is_connected():
            self.connection.close()
            self.connection = None
            logging.info('Conexão com o banco de dados fechada.')

    def criar_tabela(self):
        tabela_sql = """
        CREATE TABLE IF NOT EXISTS cnpj_dados (
            id INT AUTO_INCREMENT PRIMARY KEY,
            cnpj VARCHAR(14),
            inscricao_estadual VARCHAR(255),
            razao_social VARCHAR(255),
            nome VARCHAR(255),
            nome_fantasia VARCHAR(255),
            logradouro VARCHAR(255),
            cep VARCHAR(10),
            uf VARCHAR(2),
            telefone VARCHAR(20),
            email VARCHAR(255)
        )
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(tabela_sql)
            self.connection.commit()
            logging.info('Tabela criada ou já existente.')
        except Error as e:
            logging.error(f'Erro ao criar a tabela: {e}')
            self.connection.rollback()
            raise
        finally:
            cursor.close()

    def inserir_no_banco(self, dados: dict):
        cursor = self.connection.cursor()
        insert_sql = """
        INSERT INTO cnpj_dados (
            cnpj,
            inscricao_estadual,
            razao_social,
            nome,
            nome_fantasia,
            logradouro,
            cep,
            uf,
            telefone,
            email
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores = (
            dados['cnpj'],
            dados['inscricao_estadual'],
            dados['razao_social'],
            dados['nome'],
            dados['nome_fantasia'],
            dados['logradouro'],
            dados['cep'],
            dados['uf'],
            dados['telefone'],
            dados['email'],
        )
        try:
            cursor.execute(insert_sql, valores)
            self.connection.commit()
            logging.info(f'Dados inseridos no banco para o CNPJ {dados["cnpj"]}.')
        except Exception as e:
            logging.error(f'Erro ao inserir dados no banco para o CNPJ {dados["cnpj"]}: {e}')
            self.connection.rollback()
        finally:
            cursor.close()

    def excluir_linha_por_cnpj(self, cnpj: str):
        try:
            cursor = self.connection.cursor()
            delete_sql = "DELETE FROM cnpj_dados WHERE cnpj = %s"
            cursor.execute(delete_sql, (cnpj,))
            self.connection.commit()
            logging.info(f'CNPJ {cnpj} excluído com sucesso.')
        except Error as e:
            logging.error(f'Erro ao excluir o CNPJ {cnpj}: {e}')
            self.connection.rollback()
            raise
        finally:
            cursor.close()

    def load_data(self):
        cursor = self.connection.cursor()
        select_sql = """
        SELECT
            cnpj,
            inscricao_estadual,
            razao_social,
            nome_fantasia,
            logradouro,
            cep,
            uf,
            telefone,
            email
        FROM cnpj_dados
        """
        try:
            cursor.execute(select_sql)
            rows = cursor.fetchall()
            logging.info('Dados carregados do banco de dados.')
            return rows
        except Error as e:
            logging.error(f'Erro ao carregar dados do banco: {e}')
            raise
        finally:
            cursor.close()
