'''
Created on 8 de abr. de 2023

@author: Matheus
'''

import string


mensagem_integrity_error = ''

def contem_numero(value:str) -> bool:
    return any(p in value for p in string.digits)

def contem_pontuacao(value:str) -> bool:
    return any(p in value for p in string.punctuation)

def retornar_digitos(value:str) -> str:
    return ''.join(v for v in value if v in string.digits)

def separar_msg_virgula(values:list[str]) -> str:
    """
        Separar mensagem por virgula
    """
    return ",".join([str(n) for n in values])