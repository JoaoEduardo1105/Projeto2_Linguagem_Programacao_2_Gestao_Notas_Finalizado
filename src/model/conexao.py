import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

class Conexao:
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.database = os.getenv('DB_NAME', 'sistema_notas')
        self.user = os.getenv('DB_USER', 'postgres')
        self.password = os.getenv('DB_PASSWORD', 'postgres')
        self.port = os.getenv('DB_PORT', '5432')
        self.conn = None
    
    def conectar(self):
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            return self.conn
        except psycopg2.Error as e:
            print(f"❌ Erro ao conectar: {e}")
            return None
    
    def desconectar(self):
        if self.conn:
            self.conn.close()

def conectar():
    """Função para conexão direta (usada nos controllers)"""
    conexao_obj = Conexao()
    return conexao_obj.conectar()