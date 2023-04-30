'''
Created on 16 de abr. de 2023

@author: Matheus
'''
from sqlalchemy import Column, String, Integer, ForeignKey
from model.base import Base

class EmpresaArea(Base):
    '''
        Classe que faz o relacionamento entre Empresa e Area de intenção
    '''
    
    __tablename__ = 'empresa_area'
    
    empresa_id = Column(Integer, ForeignKey('empresa.id'), primary_key=True)
    area_intencao_id = Column(Integer, ForeignKey('area_intencao.id'), primary_key=True)
    

    def __init__(self, empresa_id:int, area_intencao_id:int):
        '''
        Constructor
        '''
        self.empresa_id = empresa_id
        self.area_intencao_id = area_intencao_id
        