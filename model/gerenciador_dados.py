# Biblioteca para centralizar acesso à base de dados

import pandas as pd

def retorna_caminho():
    """Retorna o caminho para acessar as bases de dados
    
    Returns:
        [str] -- String do caminho para acessar a base de dados
    """
    return 'bd/2019_02_COMPUTACAO_CONCLUINTES/'

def retorna_discentes():
    """Retorna o DataFrame de discentes
    
    Returns:
        DataFrame -- DataFrame de discentes
    """
    return pd.read_csv(retorna_caminho() + 'discentes.csv')

def retorna_componentes():
    """Retorna o dataframe de componentes
    
    Returns:
        DataFrame -- DataFrame de disciplinas
    """
    return pd.read_csv(retorna_caminho() + 'componentes_curriculares.csv')

def retorna_componentes_com_semestre():
    """Retorna o dataframe de componentes
    
    Returns:
        DataFrame -- DataFrame de disciplinas com a adição de coluna de semestre recomendado
    """
    return pd.read_csv(retorna_caminho() + 'componentes_curriculares_com_semestre.csv')

def retorna_matriculas():
    """Retorna o dataframe de matriculas
    
    Returns:
        DataFrame -- DataFrame de matrículas dos alunos nas disciplinas
    """
    return pd.read_csv(retorna_caminho() + 'matriculas.csv')