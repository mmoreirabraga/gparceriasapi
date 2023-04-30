'''
Created on 7 de abr. de 2023

@author: Matheus
'''
from config.db_connection_handler import DBConnectionHandler
from model.empresa.empresa import Empresa
from typing import List
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from model.empresa.empresa_area import EmpresaArea

class EmpresaRepository:
    '''
        Classe de repositorio que representa o modelo Empresa
    '''
    
    def select(self) -> List[Empresa]:
        """
            Seleciona todas as empresas cadastradas no sistema
        """

        with DBConnectionHandler.get_instancia() as db:
            data = db.session.query(Empresa).order_by(Empresa.id).all()
            return data
    
    def select_cnpj_empresa(self, cnpj:str) -> Empresa:
        """
            Buscar empresa pelo cnpj
        """

        with DBConnectionHandler.get_instancia() as db:
            try:
                data = db.session.query(Empresa).filter(Empresa.cnpj == cnpj).one()
                return data
            except NoResultFound:
                return None
            except Exception as e:
                raise e
    
    def select_id_empresa(self, id:int) -> Empresa:
        '''
            Seleciona a empresa passando o id dela
        '''
        
        with DBConnectionHandler.get_instancia() as db:
            try:
                data = db.session.query(Empresa).filter(Empresa.id == id).first()
                return data
            except NoResultFound:
                return None
            except Exception as e:
                raise e
     
    def select_areas_empresas(self, id:int):
        '''
            Retorna as áreas de intenções da empresa
        '''
        
        with DBConnectionHandler.get_instancia() as db:
            try:
                data = db.session.query(Empresa).filter(Empresa.id == id).first()
                return data.areas_intencoes
            except Exception as e:
                raise e
    
    def select_email_empresa(self, email:str) -> Empresa:
        '''
            Buscar empresa pelo email
        '''
        
        with DBConnectionHandler.get_instancia() as db:
            try:
                data = db.session.query(Empresa).filter(func.lower(Empresa.email) == email.lower()).one()
                return data
            except NoResultFound:
                return None
            except Exception as e:
                raise e
    
    def insert(self, empresa:Empresa):
        """
            Inserir uma empresa na base de dados
        """
        with DBConnectionHandler.get_instancia() as db:
            try:
                db.session.add(empresa)
                db.session.commit()
                db.session.refresh(empresa)
                return empresa
            
            except IntegrityError as i:
                db.session.rollback()
                raise i
            
            except Exception as e:
                db.session.rollback()
                raise e
    
    def update(self, empresa:Empresa):
        '''
            Atualizar uma empresa na base de dados
        '''
        with DBConnectionHandler.get_instancia() as db:
            try:
                db.session.query(Empresa).filter_by(id = empresa.id).update(dict(empresa.as_dict()))
                db.session.commit()
                #db.session.refresh(empresa)
                return empresa
            except IntegrityError as i:
                db.session.rollback()
                raise i
            
            except Exception as e:
                db.session.rollback()
                raise e
            
    
    def delete(self, id:int):
        """
            Deletar uma empresa pelo id
        """

        with DBConnectionHandler.get_instancia() as db:
            try:
                db.session.query(Empresa).filter(Empresa.id == id).delete()
                db.session.query(EmpresaArea).filter(EmpresaArea.empresa_id == id).delete()
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e    