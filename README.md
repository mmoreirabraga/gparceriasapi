# Gestão de Parcerias Minha Api

Este pequeno projeto faz parte de um projeto maior(para mais detalhes entre em contato comigo) que foi desenvolvido por mim durante 1 ano e que esta em fase de teste.

## Começando
Para executar esse projeto é necessário ter o python versão 3.11.0. Será necessário ter todas as libs python listadas no requirements.txt instaladas. Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo:

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```
(env)$ uvicorn app:app --reload
```

Abra o [http://localhost:8000/docs](http://localhost:8000/docs) ou [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) no navegador para verificar a api swagger
