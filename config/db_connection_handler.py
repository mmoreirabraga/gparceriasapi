'''
Created on 7 de abr. de 2023

@author: Matheus
'''
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
import os

class DBConnectionHandler:
    '''
        Essa classe é um padrão de projeto chamado Singleton, pois garante que uma determinada classe
        possua apenas uma instância em toda a aplicação e entregando um ponto de acesso global a essa
        instância.
        No caso de uma conexão com o banco de dados é interessante ter uma única fonte de um recurso
        compartilhado.
    '''
    
    __DB_URL = 'sqlite:///%s/gparcerias_db.sqlite3'
    __DB_PATH = 'database/'
    
    __instancia = None


    def __init__(self):
        if DBConnectionHandler.__instancia is not None:
            raise Exception("Esta é uma classe Singleton e já existe uma instância.")
        else:
            self.__criar_pasta()
            # url de acesso ao banco (essa é uma url de acesso ao sqlite local)
            self.__conexao_string = DBConnectionHandler.__DB_URL % DBConnectionHandler.__DB_PATH
            self.__engine = self.__criar_database_engine()
            self.__session = None
            self.__criar_database()
    
    
    @staticmethod
    def get_instancia():
        if DBConnectionHandler.__instancia is None:
            DBConnectionHandler.__instancia = DBConnectionHandler()
        
        return DBConnectionHandler.__instancia
    
    
    @property
    def session(self):
        """
            Forma em python de definir o método getter
        """
        return self.__session
    
    
    @property
    def engine(self):
        return self.__engine
    
    
    def __criar_pasta(self):
        """
            Só vai criar a pasta caso não exista no diretorio
        """

        # verifica se o diretorio existe
        if not os.path.exists(DBConnectionHandler.__DB_PATH):
            # então cria o diretorio
            os.makedirs(DBConnectionHandler.__DB_PATH)
    
    
    def __criar_database_engine(self):
        """
            Cria a engine de conexão com o banco
        """
        
        engine = create_engine(self.__conexao_string)
        return engine
    
    def __criar_database(self):
        """
           Cria o banco se ele não existir 
        """

        if not database_exists(self.__engine.url):
            create_database(self.__engine.url)
    
    def __enter__(self):
        session_make = sessionmaker(bind=self.__engine)
        self.__session = session_make()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__session.close()