'''
Created on 7 de abr. de 2023

@author: Matheus
'''
from sqlalchemy import Column, String, Integer, SmallInteger
from sqlalchemy.orm import relationship
from model.base import Base
from .tipo_empresa import TipoEmpresa
from .empresa_area import EmpresaArea


class Empresa(Base):
    '''
    Classe que representa as empresas que podem ser privados ou públicas(que são as prefeituras). Se for 1 é privado se for 2 é publica
    '''
    
    __tablename__ = 'empresa'
    
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    cnpj = Column(String(14), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    responsavel = Column(String(255), nullable=False)
    tipo_empresa = Column(SmallInteger, nullable=False)
    areas_intencoes = relationship('AreaIntencao', secondary='empresa_area', backref='empresa')
    
    def __init__(self, id:int, nome:str, cnpj:str, email:str, responsavel:str, tipo_empresa: TipoEmpresa):
        '''
            atributos:
            nome: se o tipo_empresa for 1: vai ser o nome de uma empresa privada, se for o tipo_empresa 2: vai ser nome de uma prefeitura
            cnpj: cnpj da empresa
            email: aqui vai ser o email da empresa
            responsavel: é o responsavel da empresa privada ou da prefeitura
            tipo_empresa: se é 1 privado e se é 2 publico(prefeitura)
        '''
        self.id = id
        self.nome = nome
        self.cnpj = cnpj
        self.email = email
        self.responsavel = responsavel
        self.tipo_empresa = tipo_empresa.value
    
    def as_dict(self):
        return {
            'nome': self.nome,
            'cnpj': self.cnpj,
            'email': self.email,
            'responsavel': self.responsavel,
            'tipo_empresa': self.tipo_empresa
        }
        