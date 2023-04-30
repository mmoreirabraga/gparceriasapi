'''
Created on 16 de abr. de 2023

@author: Matheus
'''
from pydantic import BaseModel, Field
from _ast import alias

class EmpresaAreaSchema(BaseModel):
    '''
        Define como uma empresa_area a ser inserida e excluida deve ser representado 
    '''

    empresa_id:int = Field(default=..., alias='empresaId')
    area_intencao_id:int = Field(default=..., alias='areaIntencaoId')        