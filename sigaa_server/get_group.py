import pandas as pd
from pandas.core.frame import DataFrame

class getGroup:
    def __init__(self):
        # get col name value Código Disciplina,Turma,Professor,Link of csv file
        self.filename = "/home/marcos-barbosa/Documents/dev/pessoal/django-rest/connect_sigaa_server/sigaa_server/CataGrupoUnifei.csv"
        self.col_name = ['code', 't', 'professor', 'wpp_url']
        self.index = 0
        pass

    def get_group_csv(self):
        # get csv file
        return pd.read_csv(self.filename, names=self.col_name, header=1, index_col=False)

        
