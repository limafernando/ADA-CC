# Biblioteca para centralizar requisições recorrentes à base de dados, como filtro de parte da base e cálculo de tempo de conclusão

import pandas as pd
from math import modf, inf

import sys

sys.path.insert(1, '/home/luiz/ufpb/tcc/ADA.CC/src/')

from model import gerenciador_dados

def retorna_discentes_antes(discentes):
    """Função que filtra os alunos que ingressaram antes da reforma da matriz curricular de 2006
    
    Arguments:
        discentes {DataFrame} -- DataFrame dos alunos em geral
    
    Returns:
        DataFrame -- DataFrame com os dados dos alunos que ingressaram antes da reforma da matriz curricular de 2006
    """

    if discentes.empty: #se o parâmetro for vazio
        discentes = gerenciador_dados.retorna_discentes()
        return discentes[discentes['periodo_ingresso'] < 2006]

    else: #caso contrário, o dataframe foi passado como parâmetro
        return discentes[discentes['periodo_ingresso'] < 2006]

def retorna_discentes_depois(discentes):
    """Função que filtra os alunos que ingressaram depois da reforma da matriz curricular de 2006
    
    Arguments:
        discentes {DataFrame} -- DataFrame dos alunos em geral
    
    Returns:
        DataFrame -- DataFrame com os dados dos alunos que ingressaram depois da reforma da matriz curricular de 2006
    """

    if discentes.empty: #se o parâmetro for vazio
        discentes = gerenciador_dados.retorna_discentes()
        return discentes[discentes['periodo_ingresso'] > 2006]

    else: #caso contrário, o dataframe foi passado como parâmetro
        return discentes[discentes['periodo_ingresso'] > 2006]

def retorna_tempo_graduacao(ingresso, conclusao):
    """Função que calcula o tempo, em semestres, que um aluno levou para finalizar o curso
    
    Arguments:
        ingresso {float} -- Valor do semestre de ingresso do aluno
        conclusao {float} -- Valor do semestre de conclusão do aluno
    
    Returns:
        int -- Quantidade de semestres que o aluno levou para concluir o curso
    """

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

def retorna_lista_tempo_graduacao(discentes):
    """Função que, dada a lista de discentes, calcula o tempo que cada aluno levou para se graduar
    
    Arguments:
        discentes {DataFrame} -- DataFrame dos alunos em geral
    
    Returns:
        list -- Retorna a lista com tempo de graduação de cada discente
    """

    if discentes.empty: #se o parâmetro for vazio
        discentes = gerenciador_dados.retorna_discentes()
    
    auxDF = pd.DataFrame() #dataframe auxiliar para a iteração
    auxDF['ingresso'] = discentes['periodo_ingresso'] #vai possuir a coluna de semestre de ingresso
    auxDF['conclusao'] = discentes['periodo_conclusao'] #vai possuir a coluna de semestre de conclusao

    tempos = [] #lista que amazenará os tempos para conclusão e será retornada ao final da função

    for index, row in auxDF.iterrows():
        ingresso = row[0]
        conclusao = row[1]
        tempos.append(retorna_tempo_graduacao(ingresso=ingresso, conclusao=conclusao))

    return tempos

def funcao_filtro_intervalo(elemento):
    """Função auxiliar para a função filtra_tempo_valido
    
    Arguments:
        elemento {int} -- Tempo de graduação de um aluno
    
    Returns:
        bool -- Booleano que indica se o tempo de graduação é válido, como definido na instituição
    """
    return (elemento >= 6 and elemento <= 12)

def funcao_filtro_exato(elemento):
    """Função auxiliar para a função filtra_tempo_valido
    
    Arguments:
        elemento {int} -- Tempo de graduação de um aluno
    
    Returns:
        bool -- Boolenao que indica se o tempo de graduação é de exatamente 8 semestres
    """
    return (elemento == 8)

def filtra_tempo_valido(tempos, tipo):
    """Função que filtra a lista de tempos de conclusão do curso pelos alunos, seguindo o tipo do filtro
    
    Arguments:
        tempos {list} -- Lista de tempos de conclusão
        tipo {str} -- String que descreve o tipo de filtro ('exato' ou 'intervalo')
    
    Returns:
        list -- Lista com os alunos que obedeceram o filtro
    """

    if tipo == 'exato':
        return list(filter(funcao_filtro_exato, tempos))

    elif tipo == 'intervalo':
        return list(filter(funcao_filtro_intervalo, tempos))

def checa_disciplinas_duplicadas(componentes):
    """Função que checa se existem disciplinas com o mesmo código
    
    Arguments:
        componentes {DataFrame} -- DataFrame com as disciplinas
    """

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

def checa_disciplinas_nao_cursadas(codigos_disciplinas):
    """Função que checa se todas as disciplinas foram cursadas pelo menos uma vez
    
    Arguments:
        codigos_disciplinas {list} -- Lista com os códigos das disciplinas 
    """
      
    def funcao_filtro_disciplinas_nao_cursadas(codigo):
        if codigo in codigos_disciplinas: #se a lista foi cursada retorna false
            return False
        else: #se não foi, retorna true
            return True
    
    disciplinas_nao_cursadas = list(filter(funcao_filtro_disciplinas_nao_cursadas, codigos_disciplinas)) 

    if disciplinas_nao_cursadas:
        print("Disciplinas não cursadas: ")
        print(disciplinas_nao_cursadas)
    
    else:
        print("Todas as disciplinas foram cursadas pelo menos uma vez")

def mapeia_disciplina(lista_codigos, matriculas):
    """Função que abstrai para apenas um código componentes curriculares iguais,
    substituindo todas as ocorrências dos outros códigos por esse
    e retornando o código final escolhido
    
    Arguments:
        lista_codigos {list} -- Lista com os códigos das disciplinas que devem ser representadas apenas por um código
        matriculas {DataFrame} -- DataFrame com os dados das matrículas realizadas nas disciplinas
    
    Returns:
        str -- Código único para as disciplinas
        DataFrame -- DataFrame com os dados das matrículas realizadas nas disciplinas, modificado com o código único
    """
    
    #print(lista_codigos)

    componentes = gerenciador_dados.retorna_componentes()
    #matriculas = gerenciador_dados.retorna_matriculas()
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
    """Função que checa se o aluno obteve sucesso na primeira vez que cursou a disciplina
    
    Arguments:
        aluno_matricula {dict} -- Dicionário com a relação de matrícula de um aluno em uma disciplina
    
    Returns:
        tuple -- Tupla de dois elementos
        o primeiro elemento indica se o aluno obteve sucesso (True) ou insucesso (False)
        o segundo indica o tipo de sucesso, 1 para aprovado e 0 para dispensado; em caso de insucesso, retorna None 
    """
    
    #print(aluno_matricula['descricao'].iloc[0])
    
    descricao = aluno_matricula['descricao'].iloc[0]
    
    if (descricao == 'APROVADO'):
        return (True, 1)
    
    elif (descricao == 'DISPENSADO'):
        return (True, 0)
    
    else:
        return (False, None)

def agrupa_situacao_aluno(matriculas_alunos, matriculas, cod_disciplina):
    """Função que checa o sucesso do conjunto de alunos numa disciplina
    e os agrupa em dicinário nas categorias aprovado, dispensado, insucesso e sem cursar
    
    Arguments:
        matriculas_alunos {list} -- Lista com as matrículas dos alunos
        matriculas {DataFrame} -- DataFrame com os dados de matrículas dos alunos em disciplinas
        cod_disciplina {list} -- Lista com os códigos dos componentes curriculares
    
    Returns:
        dict -- Dicionário no qual as chaves são as situações e os valores são as listas de alunos
        que obtiveram tal situação em uma disciplina
    """

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

def mapeia_discente_matriculas(matriculas_discentes, matriculas_realizadas):
    """Função que mapeia a relação de alunos com as matrículas que ele realizou, gerando um dicionário
    
    Arguments:
        matriculas_discentes {list} -- Lista com as matrículas dos alunos
        matriculas_realizadas {DataFrame} -- DataFrame com os dados das matrículas que os alunos realizaram nas disciplinas
    
    Returns:
        dict -- Dicionário no qual as chaves são as matrículas dos alunos e os valores são DataFrames com suas matrículas em disciplinas
    """

    relacao_discente_matriculas = {}

    for matricula in matriculas_discentes:
        aux = str(matricula)
        relacao_discente_matriculas[matricula] = matriculas_realizadas.query('matricula == ' + aux)

    return relacao_discente_matriculas

def exibe_alunos_nao_rec(alunos_nao_rec, discentes_depois, codigo, matriculas_geral):
    """Função que percorre a lista de alunos que não cursaram uma disciplina no recomendado e
    exibe os seus dados
    
    Arguments:
        alunos_nao_rec {list} -- Lista de alunos que não cursaram uma disciplina no recomendado
        discentes_depois {DataFrame} -- DataFrame de alunos que ingressaram no curso após a atualização curricular de 2006
        codigo {str} -- Código da disciplina analisada
        matriculas_geral {DataFrame} -- DataFrame com os dados de matrículas dos alunos nas disciplinas
    """

    for aluno in alunos_nao_rec:
        print(discentes_depois[discentes_depois['matricula'] == aluno])
        aux = matriculas_geral[matriculas_geral['matricula'] == aluno]
        aux = aux[aux['codigo_componente'] == codigo]
        print(aux)
    
        print()

def remove_alunos(discentes, matriculas, matriculas_a_remover):
    """Função que remove as ocorrências da(s) matrícula(s) de aluno(s) na base de dados
    
    Arguments:
        discentes {DataFrame} -- DataFrame com os dados dos alunos
        matriculas {DataFrame} -- DataFrame com os dados de matrículas dos alunos em disciplinas
        matriculas_a_remover {list} -- Lista de matrículas dos alunos a serem removidos da base de dados
    
    Returns:
        DataFrame -- DataFrame com os dados dos alunos após a remoção
        DataFrame -- DataFrame com os dados de matrículas dos alunos em disciplinas após a remoção
    """

    for matricula in matriculas_a_remover:
        matriculas = matriculas.query('matricula != {}'.format(matricula))
        discentes = discentes.query('matricula != {}'.format(matricula))

    return discentes, matriculas

def trata_insucesso(lista_insucesso, lista_sucesso):
    """Função que trata casos em que o aluno obteve insucesso (reprovação/trancamento) na sua primeira
    matrícula na disciplina, adicionando a lista de sucesso, sua última matrícula na disciplina, na qual ele
    obteve sucesso
    
    Arguments:
        lista_insucesso {list} -- lista onde cada elemento é um dataframe de matrículas do aluno em uma disciplina, na qual na primeira matrícula ele obteve insucesso.
        lista_sucesso {list} -- lista onde cada elemento é um dataframe com matrícula com sucesso do aluno em uma disciplina.
    
    Returns:
        {list} -- retorna a lista_sucesso atualizada
    """

    aux = list(map(lambda df: df.iloc[-1], lista_insucesso)) #acessando a última matrícula na disciplina
    aux = list(map(lambda df: df.to_frame().T, aux)) #tranpondo para ficar no formato correto

    return (lista_sucesso + aux) #somando as duas listas

def mapeia_ordem_disciplinas(matriculas_alunos, matriculas_a_analisar, codigo_primeira_disciplina, codigo_segunda_disciplina):
    # função para cl-fac2
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

def filtra_alunos(aprovacoes_primeira_disciplina, aprovacoes_segunda_disciplina):
    # função para cl-fac2
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