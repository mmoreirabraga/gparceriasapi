'''
Created on 8 de abr. de 2023

@author: Matheus
'''

from validate_docbr import CNPJ
from model.empresa.tipo_empresa import TipoEmpresa
from model.empresa.empresa import Empresa
from typing import List
from pydantic import BaseModel, Field, validator
#from typing import Dict
#import json
#from dataclasses import fields
   
def apresenta_empresa(empresa:Empresa):
    '''
        Retorna uma representação de uma empresa se for 1 privado e 2 publico(prefeitura)
    '''
    #tipo_empresa = {'tipo': empresa.tipo_empresa, 'descricao': str(TipoEmpresa(empresa.tipo_empresa))}
    #tipo_empresa_json = json.dumps(tipo_empresa, default=tipo_empresa_serializer)
    return {
        "id": empresa.id,
        "nome": empresa.nome,
        "cnpj": CNPJ().mask(empresa.cnpj),
        "email": empresa.email,
        "responsavel": empresa.responsavel,
        "tipoEmpresa": {
            "tipo": empresa.tipo_empresa,
            "descricao": str(TipoEmpresa(empresa.tipo_empresa)),
        }  #TipoEmpresaSchema.from_tipo_empresa(empresa.tipo_empresa, str(TipoEmpresa(empresa.tipo_empresa)))
    }
    '''empresa_vis = EmpresaVisualiacaoSchema.from_orm(empresa)
    print(empresa_vis.json())
    return empresa_vis.json()'''

def apresenta_empresas(empresas: List[Empresa]):
    """ Retorna uma representação de empresas que podem ser tanto privadas ou públicas
    
    """
    result = []

    for empresa in empresas:
        result.append(apresenta_empresa(empresa))
    
    return {"empresas": result}


'''def tipo_empresa_serializer(obj):
    if isinstance(obj, TipoEmpresa):
        return str(obj)
    return obj'''