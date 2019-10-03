'''
Biblioteca para centralizar requisições recorrentes às bases de dados
'''

import pandas as pd
from math import modf, inf
from statistics import mean, median, mode, stdev, variance

def retorna_caminho():
    '''
    retorna o caminho para acessar as bases de dados
    '''
    return 'bd/2019_02_COMPUTACAO_CONCLUINTES/'

def retorna_discentes():
    '''
    retorna o dataframe de discentes
    '''
    return pd.read_csv(retorna_caminho() + 'discentes.csv')

def retorna_componentes():
    '''
    retorna o dataframe de componentes
    '''
    return pd.read_csv(retorna_caminho() + 'componentes_curriculares.csv')

def retorna_componentes_com_semestre():
    '''
    retorna o dataframe de componentes
    '''
    return pd.read_csv(retorna_caminho() + 'componentes_curriculares_com_semestre.csv')

def retorna_matriculas():
    '''
    retorna o dataframe de matriculas
    '''
    return pd.read_csv(retorna_caminho() + 'matriculas.csv')

def retorna_discentes_antes(discentes=pd.DataFrame):
    '''
    retorna um dataframe com os alunos que ingressaram antes da reforma da matriz curricular de 2006
    o parâmetro pedido é o dataframe dos discentes, mas, caso não seja passado, ele acessa pela função retorna_discentes()
    '''
    
    if discentes.empty: #se o parâmetro for vazio
        discentes = retorna_discentes()
        return discentes[discentes['periodo_ingresso'] < 2006]

    else: #caso contrário, o dataframe foi passado como parâmetro
        return discentes[discentes['periodo_ingresso'] < 2006]

def retorna_discentes_depois(discentes=pd.DataFrame):
    '''
    retorna um dataframe com os alunos que ingressaram depois da reforma da matriz curricular de 2006
    o parâmetro pedido é o dataframe dos discentes, mas, caso não seja passado, ele acessa pela função retorna_discentes()
    '''

    if discentes.empty: #se o parâmetro for vazio
        discentes = retorna_discentes()
        return discentes[discentes['periodo_ingresso'] > 2006]

    else: #caso contrário, o dataframe foi passado como parâmetro
        return discentes[discentes['periodo_ingresso'] > 2006]

def retorna_tempo_graduacao(ingresso, conclusao):
    '''
    dados os semestres de ingresso e conclusão de um aluno, retorna o tempo, em semestres, que ele levou para finalizar o curso
    '''

    anos = int(conclusao) - int(ingresso)
    tempo_semestres = anos*2
    
    periodo_inicial = round(modf(ingresso)[0], 1) #pega a "parte flutuante" do semestre, por exemplo, em 2015.1, pega o 0.1
    periodo_final = round(modf(conclusao)[0], 1) #pega a "parte flutuante" do semestre, por exemplo, em 2019.1, pega o 0.1
    
    #print(periodo_inicial, periodo_final)
    
    if periodo_inicial == periodo_final:
        tempo_semestres += 1
        
    elif periodo_inicial > periodo_final:
        pass
    
    elif periodo_inicial < periodo_final:
        tempo_semestres += 2
        
    return tempo_semestres

def retorna_lista_tempo_graduacao(discentes=pd.DataFrame()):
    '''
    dado um dataframe de discentes, retorna a lista de tempo que cada discente levou para se graduar
    o parâmetro pedido é o dataframe dos discentes, mas, caso não seja passado, ele acessa pela função retorna_discentes()
    '''

    if discentes.empty: #se o parâmetro for vazio
        discentes = retorna_discentes()
    
    auxDF = pd.DataFrame() #dataframe auxiliar para a iteração
    auxDF['ingresso'] = discentes['periodo_ingresso'] #vai possuir a coluna de semestre de ingresso
    auxDF['conclusao'] = discentes['periodo_conclusao'] #vai possuir a coluna de semestre de conclusao

    tempos = [] #lista que amazenará os tempos para conclusão e será retornada ao final da função

    for index, row in auxDF.iterrows():
        ingresso = row[0]
        conclusao = row[1]
        tempos.append(retorna_tempo_graduacao(ingresso=ingresso, conclusao=conclusao))

    return tempos

def exibe_estatisticas(conteudo):
    '''
    dada uma lista de dados, por exemplo, tempo ou cra, exibe os dados estatísticos
    '''
    print('mínimo: {} \nmáximo: {}'.format(min(conteudo), max(conteudo)))
    
    try:
        print('média: {} \nmediana: {}  \nmoda: {} \ndesvia padrão: {} \nvariância: {}'.format(mean(conteudo), median(conteudo), mode(conteudo), stdev(conteudo), variance(conteudo)))
    except:
        print('!mais de um valor pra moda!')
        print('média: {} \nmediana: {}  \ndesvio padrão: {} \nvariância: {}'.format(mean(conteudo), median(conteudo), stdev(conteudo), variance(conteudo)))

def funcao_filtro_intervalo(elemento):
    '''
    funcao auxiliar para a função filtra_tempo_valido
    '''
    return (elemento >= 6 and elemento <= 12)

def funcao_filtro_exato(elemento):
    '''
    funcao auxiliar para a função filtra_tempo_valido
    '''
    return (elemento == 8)

def filtra_tempo_valido(tempos, tipo):
    '''
    dada uma lista de tempos para conclusão de curso por discentes, filtra essa lista
    seguindo o tipo do filtro e, consequentemente, a função de filtro associada
    '''

    if tipo == 'exato':
        return list(filter(funcao_filtro_exato, tempos))

    elif tipo == 'intervalo':
        return list(filter(funcao_filtro_intervalo, tempos))

def calcula_porcentagem(universo, amostra):
    '''
    função "genérica" para calcular a porcentagem
    '''
    
    return amostra/universo

def checa_disciplinas_duplicadas(componentes):
    '''
    dado o dataframe de disciplinas/componentes, checa se existe disciplinas com o mesmo código
    '''

    codigos = componentes['codigo']

    disciplinas_duplicadas = codigos.duplicated()

    if any(disciplinas_duplicadas):
        disciplinas_duplicadas = disciplinas_duplicadas.tolist()

        lista_aux = []
        for i in range(0, len(disciplinas_duplicadas)):
            if disciplinas_duplicadas[i]:
                lista_aux.append(i)

        disciplinas_duplicadas = lista_aux
        codigo_duplicadas = []

        for i in disciplinas_duplicadas:
            cod = codigos.iloc[i]
            codigo_duplicadas.append(cod)
            #print(cod)
            print(componentes[componentes['codigo'] == cod])

    else:
        print('Sem disciplinas duplicadas')

def mapeia_disciplina(lista_codigos, matriculas):

    '''
    dada uma lista de codigos de componentes "iguais", exemplo CL de 90 e 60 horas,
    abstrai para apenas um código, o do componente com menor carga horária
    substituindo todas as ocorrências dos outros códigos por esse
    e retornando o código final escolhido
    '''
    
    #print(lista_codigos)

    componentes = retorna_componentes()
    #matriculas = retorna_matriculas()
    ch_min = inf
    codigo_final = ''
    
    for codigo in lista_codigos:
        
        componente = componentes[componentes['codigo'] == codigo]
        
        ch = componente['ch_total'].iloc[0]
        
        if ch < ch_min:
            codigo_final = codigo
            ch_min = ch
    
    lista_codigos.remove(codigo_final)
    
    for codigo in lista_codigos:
        
        #print(matriculas[matriculas['codigo_componente'] == codigo])
        matriculas.loc[matriculas['codigo_componente'] == codigo, ['codigo_componente']] = codigo_final
        #print(matriculas[matriculas['codigo_componente'] == codigo])
    
    print('Disciplina(s) {} mapeadas para o código {}'.format(lista_codigos, codigo_final))
    
    return codigo_final, matriculas

def checa_sucesso(aluno_matricula):

    '''
    Função que checa se o aluno obteve sucesso na primeira vez que cursou a disciplina
    Retorna uma tupla de dois elementos:
    o primeiro elemento indica se o aluno obteve sucesso (True) ou insucesso (False)
    o segundo indica o tipo de sucesso, 1 para aprovado e 0 para dispensado; em caso de insucesso, retorna None
    '''
    #print(aluno_matricula['descricao'].iloc[0])
    
    descricao = aluno_matricula['descricao'].iloc[0]
    
    if (descricao == 'APROVADO'):
        return (True, 1)
    
    elif (descricao == 'DISPENSADO'):
        return (True, 0)
    
    else:
        return (False, None)

def agrupa_situacao_aluno(matriculas_alunos, matriculas, cod_disciplina):

    '''
    dado um código de disciplina, checa o sucesso do conjunto de alunos nessa disciplina
    e os agrupa em dicinário nas categorias aprovado, dispensado, insucesso e sem cursar
    a função retorna esse discionário
    '''

    #matriculas = retorna_matriculas()

    aluno_cursou_aprovado = []
    aluno_cursou_dispensado = []
    aluno_cursou_insucesso = []
    aluno_sem_cursar = []

    disciplina_dict = {}

    for matricula in matriculas_alunos:
        
        matriculas_aluno = matriculas[matriculas['matricula'] == matricula]
    
        aluno_matricula = matriculas_aluno[matriculas_aluno['codigo_componente'] == cod_disciplina]

        if not aluno_matricula.empty: #se não for vazio, significa que o aluno curso
            retorno_sucesso = checa_sucesso(aluno_matricula)

            if retorno_sucesso[0]:
                
                if retorno_sucesso[1]:
                    aluno_cursou_aprovado.append(aluno_matricula)
                else:
                    aluno_cursou_dispensado.append(aluno_matricula)
                
            else:
                aluno_cursou_insucesso.append(aluno_matricula)

        else:
            print(aluno_matricula)
            aluno_sem_cursar.append(matricula)

    disciplina_dict['aprovado'] = aluno_cursou_aprovado
    disciplina_dict['dispensado'] = aluno_cursou_dispensado
    disciplina_dict['insucesso'] = aluno_cursou_insucesso
    disciplina_dict['sem cursar'] = aluno_sem_cursar

    return disciplina_dict

def mapeia_ordem_disciplinas(matriculas_alunos, matriculas_a_analisar, codigo_primeira_disciplina, codigo_segunda_disciplina):
    '''
    checa qual disciplina foi cursada primeiro
    retornando um dicinário com as chaves sendo 'codigo_primeira_disciplinaxcodigo_segunda_disciplina' e 'codigo_segunda_disciplinaxcodigo_primeira_disciplina'
    e os valores as listas de alunos que se enquadram em cada grupo
    '''

    chave1x2 = codigo_primeira_disciplina+'x'+codigo_segunda_disciplina
    chave2x1 = codigo_segunda_disciplina+'x'+codigo_primeira_disciplina

    alunos_dict = {}
    alunos_dict[chave1x2] = []
    alunos_dict[chave2x1] = []

    for matricula in matriculas_alunos:

        matriculas_aluno = matriculas_a_analisar[matriculas_a_analisar['matricula'] == matricula]
    
        matricula_primeira_disciplina = matriculas_aluno[matriculas_aluno['codigo_componente'] == codigo_primeira_disciplina]
        matricula_segunda_disciplina = matriculas_aluno[matriculas_aluno['codigo_componente'] == codigo_segunda_disciplina]
        
        #print(matricula)
        #print(matricula_primeira_disciplina['periodo_matricula'])

        if matricula_primeira_disciplina['periodo_matricula'].iloc[0] < matricula_segunda_disciplina['periodo_matricula'].iloc[0]:
            alunos_dict[chave1x2].append(matricula)

        else:
            alunos_dict[chave2x1].append(matricula)

    return alunos_dict

def remove_alunos(discentes, matriculas, matriculas_a_remover):
    '''
    dada uma lista de matrículas, remove as ocorrências dessas matrículas nas bases de dados
    '''

    for matricula in matriculas_a_remover:
        matriculas = matriculas.query('matricula != {}'.format(matricula))
        discentes = discentes.query('matricula != {}'.format(matricula))

    return discentes, matriculas

def trata_insucesso(lista_insucesso, lista_sucesso):
    """Função que trata casos em que o aluno obteve insucesso (reprovação/trancamento) na sua primeira
    matrícula na disciplina, adicionando a lista de sucesso, sua última matrícula na disciplina, na qual ele
    obteve sucesso.
    
    Arguments:
        lista_insucesso {list} -- lista onde cada elemento é um dataframe de matrículas do aluno em uma disciplina, na qual na primeira matrícula ele obteve insucesso.
        lista_sucesso {list} -- lista onde cada elemento é um dataframe com matrícula com sucesso do aluno em uma disciplina.
    
    Returns:
        {list} -- retorna a lista_sucesso atualizada
    """

    aux = list(map(lambda df: df.iloc[-1], lista_insucesso)) #acessando a última matrícula na disciplina
    aux = list(map(lambda df: df.to_frame().T, aux)) #tranpondo para ficar no formato correto

    return (lista_sucesso + aux) #somando as duas listas

def filtra_alunos(aprovacoes_primeira_disciplina, aprovacoes_segunda_disciplina):
    
    aux = []
    
    df_aprovacoes_primeira_disciplina = pd.concat(aprovacoes_primeira_disciplina)
    df_aprovacoes_segunda_disciplina = pd.concat(aprovacoes_segunda_disciplina)

    matriculas_primeira_disciplina = df_aprovacoes_primeira_disciplina['matricula'].to_list()
    matriculas_segunda_disciplina = df_aprovacoes_segunda_disciplina['matricula'].to_list()

    if len(matriculas_primeira_disciplina) > len(matriculas_segunda_disciplina):
        for matricula in matriculas_segunda_disciplina:
            aux.append(df_aprovacoes_primeira_disciplina.query('matricula == {}'.format(matricula)))

        aprovacoes_primeira_disciplina = aux

        return aprovacoes_primeira_disciplina, aprovacoes_segunda_disciplina

    elif len(aprovacoes_primeira_disciplina) < len(aprovacoes_segunda_disciplina):
        for matricula in matriculas_primeira_disciplina:
            aux.append(df_aprovacoes_segunda_disciplina.query('matricula == {}'.format(matricula)))

        aprovacoes_segunda_disciplina = aux

        return aprovacoes_primeira_disciplina, aprovacoes_segunda_disciplina

    else:
        return aprovacoes_primeira_disciplina, aprovacoes_segunda_disciplina