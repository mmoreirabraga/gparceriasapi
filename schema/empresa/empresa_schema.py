'''
Created on 8 de abr. de 2023

@author: Matheus
'''

from pydantic import BaseModel, validator, Field
from utils.string_util import contem_numero, contem_pontuacao, retornar_digitos, separar_msg_virgula
from utils.collection_util import is_empty
from validate_docbr import CNPJ
from model.empresa.empresa import TipoEmpresa
from string_utils.validation import is_email
from repository.empresa.empresa_repository import EmpresaRepository

class EmpresaSchema(BaseModel):
    '''
        Define como uma nova empresa a ser inserida deve ser representado
    '''
    id:int = Field(default=None)
    nome: str = Field(default=..., max_length=255)
    cnpj: str = Field(default=..., min_length=14, max_length=18)
    email:str = Field(default=..., max_length=255)
    responsavel: str = Field(default=..., max_length=255)
    tipo_empresa: int = Field(default=..., alias="tipoEmpresa")
    
    
    @validator('email')
    @classmethod
    def validar_email(cls, value:str, values:dict):

        if not is_email(value):
            raise ValueError("E-mail não é valido")
        
        if values.get('id') is None:
            repo = EmpresaRepository()
            empresa = repo.select_email_empresa(value)
            if empresa is not None:
                raise ValueError("E-mail informado já existe na base de dados")
                   
        return value.lower()

    @validator('nome')
    @classmethod
    def validar_nome(cls, value:str):

        mensagens = []

        if contem_numero(value):
            mensagens.append('Responsavel não deve possuir número')
        
        if contem_pontuacao(value):
            mensagens.append('Responsavel não deve possuir pontuação')
        
        if not is_empty(mensagens):
            raise ValueError(separar_msg_virgula(mensagens))

        return value
    
    @validator('cnpj')
    @classmethod
    def validar_cnpj(cls, value:str, values:dict):
        
        cnpj = retornar_digitos(value)

        if not CNPJ().validate(cnpj):
            raise ValueError('CNPJ Inválido')
        
        if values.get('id') is None:
            repo = EmpresaRepository()
            empresa = repo.select_cnpj_empresa(value)
            if empresa is not None:
                raise ValueError('CNPJ informado já existe na base de dados')
        
        return cnpj
    

    @validator('tipo_empresa')
    @classmethod
    def validar_tipo_empresa(cls, value:int):
        
        if not any(value == item.value for item in TipoEmpresa):
            raise ValueError('Você selecionou um item que não existe.')

        return value         