'''
Created on 7 de abr. de 2023

@author: Matheus
'''
from config.db_connection_handler import DBConnectionHandler
from model.area.area_intencao import AreaIntencao
from typing import List

class AreaIntencaoRepository(object):
    '''
         Classe de repositorio que representa o modelo AreaIntencao
    '''


    def select(self) -> List[AreaIntencao]:
        """
            Seleciona todas as áreas de intenção cadastradas no sistema em ordem crescente pela descrição
        """

        with DBConnectionHandler.get_instancia() as db:
            data = db.session.query(AreaIntencao).order_by(AreaIntencao.descricao).all()
            return data
    
    def insert(self, area_intencao:AreaIntencao):
        """
            Inserir uma área de intenção na base de dados
        """

        with DBConnectionHandler.get_instancia() as db:
            try:
                db.session.add(area_intencao)
                db.session.commit()
                db.session.refresh(area_intencao)
                return area_intencao
            except Exception as e:
                raise e
    
    def delete(self, id:int):
        """
            Deletar uma área de intenção pelo id
        """

        with DBConnectionHandler.get_instancia() as db:
            try:
                db.session.query(AreaIntencao).filter(AreaIntencao.id == id).delete()
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e