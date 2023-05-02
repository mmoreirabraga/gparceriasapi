'''
Created on 7 de abr. de 2023

@author: Matheus
'''

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError
from schema.empresa.empresa_schema import EmpresaSchema
from schema.empresa.empresa_area_schema import EmpresaAreaSchema
from schema.empresa.response_empresa import apresenta_empresa, apresenta_empresas
from model.empresa.empresa import Empresa, TipoEmpresa
from model.empresa.empresa_area import EmpresaArea
from repository.empresa.empresa_repository import EmpresaRepository
from schema.area.response_area import apresenta_areas
from repository.area.area_intencao_repository import AreaIntencaoRepository
from repository.empresa.empresa_area_repository import EmpresaAreaRepository
import uvicorn
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from schema.empresa.response_empresa_area import apresenta_empresa_area
from utils.collection_util import is_empty

app = FastAPI()

# Configurações do CORS
origins = ["*"]

# Adicionando o middleware do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


empresa_tag = 'Empresa(privado ou prefeitura): Inserção, atualização, visualização e remoção de empresas na base'
area_intencao_tag = 'Area Intenção: visualização das areas de intenções na base'
empresa_area_tag = 'Empresa área: inserir e remover uma empresa que possui area intenção na base'
listar_area_empresa_tag = 'Listar areas da empresa: listar todas as areas vinculada a empresa'
match_tag = "Listar match: Listar todos os matches que ocorreram entre os privados e prefeituras"

@app.put('/empresa', tags=[empresa_tag])
@app.post('/empresa', tags=[empresa_tag])
def adicionar_empresa(form: EmpresaSchema):
    """
        Cadastra ou editar uma empresa(privado ou prefeitura) na base de dados

        Retorna uma representação da empresa(Privado ou Prefeitura)
    """

    empresa = Empresa(
        id= form.id,
        nome= form.nome,
        cnpj= form.cnpj,
        email=form.email,
        responsavel=form.responsavel,
        tipo_empresa= TipoEmpresa(form.tipo_empresa)
    )



    try:

        repo = EmpresaRepository()
        emp =  repo.insert(empresa) if empresa.id is None else repo.update(empresa)
      
        return  apresenta_empresa(emp), 200

    except IntegrityError as e:
        # como a duplicidade do cnpj e email é a provavel razão do IntegrityError
        # verifica se o erro se deve à violação de uma restrição de chave única
        error_msg = f"O email ou cnpj já existem na base de dados."
        return {"mensagem", error_msg}, 409
    
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possivel salvar nova empresa :/"
        print(e.args)
        return {"mensagem": error_msg}, 400


@app.get('/empresa', tags=[empresa_tag]) 
def retornar_empresa(id:int): 
    '''
        Retorna uma representação da empresa(Privado ou Prefeitura)
    '''
    
    try:
        
        repo = EmpresaRepository()
        emp = repo.select_id_empresa(id)
        
        if emp is None:
            return {"empresa": {}}, 200
        
        return apresenta_empresa(emp),200
    
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possivel consultar nova empresa"
        print(e.args)
        return {"mensagem": error_msg}, 400
    

@app.delete('/empresa', tags=[empresa_tag])
def excluir_empresa(id:int):
    '''
        Excluir uma empresa(Privado ou Prefeitura)
    '''
    
    try:
        repo = EmpresaRepository()
        repo.delete(id)
        msg_sucesso = 'Empresa Excluida com sucesso'
        return {"mensagem": msg_sucesso}, 200
    except Exception:
        error_msg = 'Não foi possivel deletar a empresa'
        return {"mensagem": error_msg}, 400


@app.get('/empresas', tags=[empresa_tag]) # responses={"200": ListagemEmpresasSchema}
def listar_empresas():
    """ Faz busca por todas as empresas cadastradas(Publicas ou Privadas)

    Retorna uma representação da listagem de empresas
    
    """

    repo = EmpresaRepository()
    empresas = repo.select()

    if not empresas:
        # se não há empresas cadastrados
        return {"empresas": []}, 200
    
    # retorna a representação de empresas
    
    return apresenta_empresas(empresas), 200
    
@app.get("/areasIntencoes", tags=[area_intencao_tag])
def listar_areas_intencoes():
    '''Faz busca por todas as áreas de intenções cadastradas
       Retorna uma representação da listagem de áreas de intenções
    '''
    
    repo = AreaIntencaoRepository()
    areas = repo.select()
    
    if not areas:
        # se não há empresas cadastrados
        return {"areasIntencoes": []}, 200
    
    # retorna a representação de empresas
    return apresenta_areas(areas), 200


@app.get('/listarAreasEmpresa', tags=[listar_area_empresa_tag])
def listar_areas_empresa(id:int): # query:EmpresaBuscaSchema
    '''
        Listar todas as áreas da empresa, ou seja, listar as áreas que estão vinculada as empresas, deve passar o id da empresa
    '''
    try:
        
        repo = EmpresaRepository()
        areas = repo.select_areas_empresas(id)
        
        if is_empty(areas):
            return {"areasIntencoes": {}}, 200
        
        return apresenta_areas(areas), 200
    
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possivel trazer as áreas de intenções"
        print(e.args)
        return {"mensagem": error_msg}, 400
    
    

@app.post("/empresaArea", tags=[empresa_area_tag])
def adicionar_empresa_area(form:EmpresaAreaSchema):
    '''
        Cadastra uma empresa com sua area de intenção na base de dados
    '''
    
    emp_area = EmpresaArea(
        empresa_id = form.empresa_id, area_intencao_id = form.area_intencao_id
    )
    
    try:

        repo = EmpresaAreaRepository()
        empresa_area = repo.insert(emp_area)
        
        return  apresenta_empresa_area(empresa_area), 200

    except IntegrityError as e:
        # como a duplicidade do cnpj e email é a provavel razão do IntegrityError
        # verifica se o erro se deve à violação de uma restrição de chave única
        error_msg = f"Essa empresa já possui essa área de intenção."
        return {"mensagem", error_msg}, 409
    
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possivel vincular a área de intenção a empresa."
        
        return {"mensagem": error_msg}, 400

@app.delete('/empresaArea', tags=[empresa_area_tag])
def excluir_empresa_area(id_empresa:int, id_area_intencao:int): # query: EmpresaAreaSchema
    '''
        Excluir uma empresa area da base
    '''
    
    try:
        repo = EmpresaAreaRepository()
        repo.delete(id_empresa=id_empresa, id_area_intencao=id_area_intencao)
        msg_sucesso = 'A área de intenção foi desvinculada da empresa ou prefeitura com sucesso'
        return {"mensagem": msg_sucesso}, 200
    except Exception:
        error_msg = 'Não foi possivel deletar a empresa'
        return {"mensagem": error_msg}, 400

@app.get("/matches", tags=[match_tag])
def matches():
    """
        Matches entre privado e prefeitura que possuem a mesma área de intenção.
    """
    repo = EmpresaAreaRepository()
    combinacao = repo.select()
    if  is_empty(combinacao):
        return {'matchesEmpresas': []}, 200
    
    return {'matchesEmpresas': combinacao}, 200
    

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_messages = []
    for error in exc.errors():
        error_messages.append({error["loc"][1] : error["msg"]})
    return JSONResponse(
        status_code=422,
        content={"detail": error_messages},
    )

app.exception_handler(RequestValidationError)(validation_exception_handler)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)







