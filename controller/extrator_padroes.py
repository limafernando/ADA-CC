# Biblioteca para centralizar funções com objetivo de extrair os padrões/dados dos fluxos reais dos alunos

import sys

sys.path.insert(1, '/home/luiz/ufpb/tcc/ADA.CC/src/')

from controller import controlador_dados

def porcentagem_por_periodo(alunos_nao_rec, discentes_depois, matriculas_realizadas, codigo_disciplina, periodo_rec):
    """
    Função que, dado os alunos que não cursaram uma certa disiciplina no recomendado, 
    computa a porcentagem de alunos que cursaram essa disciplinas nos outros semestres.
    
    Arguments:
        alunos_nao_rec {list} -- lista com as matrículas dos alunos que não cursaram a disciplina no recomendado
        discentes_depois {dataframe} -- dataframe dos alunos que ingressaram após 2006.1
        matriculas_realizadas {dataframe} -- dataframe das matrículas, com sucesso, dos alunos na disciplina
        codigo_disciplina {str} -- código (chave primária) da disciplina
        periodo_rec {int} -- valor do semestre recomendado na grade curricular para se cursar a disciplina
    
    Returns:
        list -- lista com as porcentagens de alunos que cursaram a disciplina em cada semestre;
        cada índice da lista representa um semestre, onde i = semestre-1
    """
    porcentagem_por_periodo = [0]
    
    matriculas = len(alunos_nao_rec)
    
    for aluno in alunos_nao_rec:
        
        aux = matriculas_realizadas[matriculas_realizadas['matricula'] == aluno]
        aux = aux[aux['codigo_componente'] == codigo_disciplina]
        
        periodo_matricula = aux['periodo_matricula'].iloc[0]
        periodo_ingresso = discentes_depois[discentes_depois['matricula'] == aluno]['periodo_ingresso'].iloc[0]

        periodo_cursou = controlador_dados.retorna_tempo_graduacao(periodo_ingresso, periodo_matricula)

        indice = periodo_cursou-1

        '''if indice == 0:
            print(aluno)'''

        try:
            porcentagem_por_periodo[indice] += 1
        
        except IndexError:
            cont = indice - len(porcentagem_por_periodo) + 1
            
            while(cont > 0):
                porcentagem_por_periodo.append(0)
                cont -= 1
            
            porcentagem_por_periodo[indice] += 1

    return list(map(lambda x: x/matriculas, porcentagem_por_periodo))

def porcentagem_por_situacao(alunos, discentes_depois, matriculas_realizadas, codigo_disciplina, periodo_rec):
    """
    Função que, dado os alunos que não cursaram uma certa disiciplina no recomendado, 
    computa a porcentagem das situações dos alunos na sua primeira tentativa de cursar a disciplina.
    
    Arguments:
        alunos {list} -- lista com as matrículas dos alunos que não cursaram a disciplina no recomendado
        discentes_depois {dataframe} -- dataframe dos alunos que ingressaram após 2006.1
        matriculas_realizadas {dataframe} -- dataframe das matrículas, com e sem sucesso, dos alunos na disciplina
        codigo_disciplina {str} -- código (chave primária) da disciplina
        periodo_rec {int} -- valor do semestre recomendado na grade curricular para se cursar a disciplina
    
    Returns:
        dict -- dicionário com as porcentagens das situações dos alunos na sua primeira tentativa de cursar a disciplina;
        cada chave do dicionário é uma situação
    """

    porcentagem_por_situacao = {}
    
    matriculas = len(alunos)
    
    for aluno in alunos:
        #print(aluno)

        aux = matriculas_realizadas[matriculas_realizadas['matricula'] == aluno]
        #print(aux)
        aux = aux[aux['codigo_componente'] == codigo_disciplina]

        #print(aux)
        
        situacao_matricula = aux['descricao'].iloc[0]

        try:
            porcentagem_por_situacao[situacao_matricula] += 1
        
        except KeyError:
            porcentagem_por_situacao[situacao_matricula] = 0
            porcentagem_por_situacao[situacao_matricula] += 1

    return dict(map(lambda item: (item[0], (item[1]/matriculas)), porcentagem_por_situacao.items()))