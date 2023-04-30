'''
Created on 7 de abr. de 2023

@author: Matheus
'''
from enum import Enum

class TipoEmpresa(Enum):
    
    PRIVADO = 1
    PUBLICO = 2
    
    def __str__(self) -> str:
        if self == TipoEmpresa.PRIVADO:
            return "Privado"
        else:
            return "Prefeitura"
        