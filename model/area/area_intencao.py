'''
Created on 7 de abr. de 2023

@author: Matheus
'''
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from model.base import Base
from model.empresa.empresa_area import EmpresaArea

class AreaIntencao(Base):
    
    __tablename__ = 'area_intencao'
    
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(255), nullable=True)


    def __init__(self, descricao:str):
        '''
            descricao: é a descrição da área de intenção
        '''
        self.descricao = descricao
        