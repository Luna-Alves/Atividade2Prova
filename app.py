from json import dumps, loads
from flask import Flask, jsonify, request
from marshmallow import Schema, fields, ValidationError

# Objetivo do código: Cadastrar novos alunos e novos relatórios dentro de uma lista

alunos = [] # Cria uma lista de alunos. Os dados de alunos são gravados aqui, mas as informações se perdem ao reiniciar a página. Seria ideal utilizar um banco de dados como o SQLite
relatorios = [] # Cria uma lista de relatórios. Os dados de relatórios são gravados aqui, mas as informações se perdem ao reiniciar a página. Seria ideal utilizar um banco de dados como o SQLite pois assim a persistência dos dados seria garantida mesmo com a reinicializaçao da aplicação.

class AlunoSchema(Schema): # Define os tipos de dados de entrada para Alunos
    idade = fields.Integer(required=True) # usando o marshmallow, garante que idade receba um valor do tipo int
    disciplina = fields.String(required=True) # usando o marshmallow, garante que disciplina receba um valor do tipo string
    # O marshmallow está sendo usando ao termos Schema como parâmetro de AlunoSchema pois um schema é usado para garantir o tipo de entrada esperada e os campos obrigatórios. Nesse caso, ele obriga que idade seja obrigatório e que receba int e que disciplina seja obrigatório e que receba string Ex.: required = True


class RelatorioSchema(Schema): # Define os tipos de dados de entrada para Relatórios
    titulo = fields.Str() # Garante que titulo receba uma string, mas não é obrigatório
    criacao = fields.Date() # garante que criacao receba um tipo date, mas não é obrigatório
    aluno = fields.Nested(AlunoSchema()) # recebe um objeto validado em AlunoSchema


def cadastrarAluno(json_str: str): #função que cadastra um novo aluno
    aluno = loads(json_str) # recebe um tipo JSON em aluno e transforma em dicionário
    alunos.append(aluno) # adiciona um novo aluno na lista 'alunos'
    return aluno # retorna aluno


def cadastrarRelatorio(json_str: str): # função que cadastra um novo relatório
    relatorio = loads(json_str) # recebe um tipo JSON em relatório e transforma em dicionário
    relatorios.append(relatorio)  # adiciona um novo relatório na lista 'relatorios'
    return relatorio #retorna relatorio


app = Flask(__name__) # criação da instância dentro da aplicação flask

# Endpoint REST: POST - Esse endpoint vai permitir criar um novo aluno na aplicação
@app.post('/aluno')
def aluno_post():
    
    request_data = request.json # request_data precisa receber um dado json com idade e disciplina

    schema = AlunoSchema() #recebe os dados já validados pelo schema de AlunoSchema
    try:
        result = schema.load(request_data) # a função load(request_data) valida os dados de acordo com o que foi definido em AlunoSchema (schema)

        data_now_json_str = dumps(result) # se result for validado, é transformado em JSON

        response_data = cadastrarAluno(data_now_json_str) # aqui o aluno vai ser adicionado

    except ValidationError as err: # retorna o erro 400 caso a validação dÊ errado
        return jsonify(err.messages), 400

    return jsonify(response_data), 200 #retorna o status 200 se não houver erro

# Endpoint REST: POST - Esse endpoint vai permitir criar um novo relatorio na aplicação
@app.post('/relatorio')
def relatorio_post():

    request_data = request.json # request_data precisa receber um dado json de entrada com titulo, data de criação (opcionais), idade e disciplina do aluno (obrigatórios)

    schema = RelatorioSchema() # #recebe os dados já validados pelo schema de RelatorioSchema
    try:
        result = schema.load(request_data) # a função load(request_data) valida os dados de acordo com o que foi definido em RelatorioSchema (schema)

        data_now_json_str = dumps(result) # se result for validado, é transformado em JSON

        response_data = cadastrarRelatorio(data_now_json_str) # aqui o relatorio vai ser adicionado e retornado

    except ValidationError as err: # retorna o erro 400 caso a validação dÊ errado
        return jsonify(err.messages), 400

    return jsonify(response_data), 200 #retorna o status 200 se não houver erro
