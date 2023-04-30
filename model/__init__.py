from model.base import Base
from config.db_connection_handler import DBConnectionHandler
from model.empresa.empresa import Empresa
from model.area.area_intencao import AreaIntencao
from repository.area.area_intencao_repository import AreaIntencaoRepository
 
# cria as tabelas do banco, caso não existem
with DBConnectionHandler.get_instancia() as db:
    Base.metadata.create_all(db.engine)

repo = AreaIntencaoRepository();
if len(repo.select()) == 0:
    areas = [
        AreaIntencao('Energia e Inovação (Iluminação Pública)'), AreaIntencao('Saneamento (Água e Esgoto)'),
        AreaIntencao('Saneamento (Resíduos Sólidos)'), AreaIntencao('Infraestrutura Social (Sistema Funerário)'),
        AreaIntencao('Mobilidade (Rodovias)'), AreaIntencao('Infraestrutura Social (Parques Urbanos)'),
        AreaIntencao('Infraestrutura Social (Habitacional)'), AreaIntencao('Infraestrutura Social (Educação)'),
        AreaIntencao('Infraestrutura Social (Saúde)'), AreaIntencao('Mobilidade (Portos)'),
        AreaIntencao('Mobilidade (Ferrovias)'), AreaIntencao('Mobilidade (Aeroportos)'),
        AreaIntencao('Energia e Inovação (Eficiência Energética e Tecnologia)'), AreaIntencao('Infraestrutura Social (Matadouros Públicos)'),
        AreaIntencao('Infraestrutura Social (Shopping Popular)'), AreaIntencao('Infraestrutura Social (Unidades de Atendimento Popular)'),
        AreaIntencao('Infraestrutura Social (Centrais de Abastecimento)'), AreaIntencao('Infraestrutura Social (Ginásios Esportivos)'),
        AreaIntencao('Infraestrutura Social (Terminais Rodoviários)'), AreaIntencao('Infraestrutura Social (Hoteis Turisticos)'),
        AreaIntencao('Infraestrutura Social (Fomento Agricultura)'), AreaIntencao('Infraestrutura Social (Prédios Administração Pública)'),
        AreaIntencao('Energia e Inovação (Tecnologia da Informação)'), AreaIntencao('Infraestrutura Social (Pontes Municipais)'),
        AreaIntencao('Mobilidade (Transporte Urbano)')     
    ]
    
    for a in areas:
        repo.insert(a)