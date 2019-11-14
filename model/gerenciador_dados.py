'''
Biblioteca para centralizar acesso à base de dados
'''

import pandas as pd

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