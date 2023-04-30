'''
Created on 16 de abr. de 2023

@author: Matheus
'''
from model.empresa.empresa_area import EmpresaArea

def apresenta_empresa_area(empresa_area:EmpresaArea):
    '''
        Retorna uma representação de uma EmpresaArea
    '''
    
    return {
        "empresaId": empresa_area.empresa_id,
        "areaIntencaoId": empresa_area.area_intencao_id
    }