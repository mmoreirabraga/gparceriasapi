'''
Created on 16 de abr. de 2023

@author: Matheus
'''
from model.empresa.empresa_area import EmpresaArea
from model.empresa.tipo_empresa import TipoEmpresa
from config.db_connection_handler import DBConnectionHandler
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text

class EmpresaAreaRepository:
    '''
        Classe de repositorio que representa o modelo EmpresaAreaRepository
    '''
    
    def select(self):
        '''
            Buscar todas as áreas de intenção vinculada as empresas(privada uo prefeitura
        '''
        with DBConnectionHandler.get_instancia() as db:
            sql = text('SELECT priv.nome as nomePrivado, priv.cnpj as cnpjPrivado, priv.tipo_empresa as tipoEmpPriv, ai.descricao as descAreaPriv, ' \
            'pref.nome as nomePrefeitura, pref.cnpj as cnpjPrefeitura, pref.tipo_empresa as tipoEmpPref, aipref.descricao as descAreaPref ' \
            'FROM empresa priv ' \
            'INNER JOIN empresa_area eapriv ON priv.id = eapriv.empresa_id and priv.tipo_empresa = 1 ' \
            'INNER JOIN area_intencao ai ON eapriv.area_intencao_id = ai.id ' \
            'INNER JOIN empresa_area eapref ON eapriv.area_intencao_id  = eapref.area_intencao_id ' \
            'INNER JOIN empresa pref ON eapref.empresa_id = pref.id and pref.tipo_empresa = 2 ' \
            'INNER JOIN area_intencao aipref ON eapref.area_intencao_id = aipref.id;')
            result = db.engine.connect().execute(sql).fetchall()
            result_dict = []
            for row in result:
                
                result_dict.append({
                    'nomePrivado': row[0],
                    'cnpjPrivado': row[1],
                    'tipoEmpPriv': str(TipoEmpresa(row[2])),
                    'descAreaPriv': row[3],
                    'nomePrefeitura': row[4],
                    'cnpjPrefeitura': row[5],
                    'tipoEmpPref': str(TipoEmpresa(row[6])),
                    'descAreaPref': row[7]
                })
                
                    
            return result_dict
            
    
    def insert(self, empesa_area:EmpresaArea):
        '''
            Inseri uma empresa com sua area de intenção
        '''
        with DBConnectionHandler.get_instancia() as db:
            try:
                db.session.add(empesa_area);
                db.session.commit();
                db.session.refresh(empesa_area)
                return empesa_area
            except IntegrityError as i:
                db.session.rollback()
                raise i
            
            except Exception as e:
                db.session.rollback()
                raise e
    
    def delete(self, id_empresa:int, id_area_intencao:int):
        """
            Deletar uma empresa area
        """

        with DBConnectionHandler.get_instancia() as db:
            try:
                db.session.query(EmpresaArea).filter(EmpresaArea.empresa_id == id_empresa, EmpresaArea.area_intencao_id == id_area_intencao).delete()
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e    
        