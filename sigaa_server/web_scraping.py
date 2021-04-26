import mechanize as mechanize
from bs4 import BeautifulSoup as bs
import http.cookiejar as cookielib
from numpy import NaN

import pandas as pd

class ScrapingSigaa():

    def __init__(self, userlogin, userpass, url='https://sigaa.unifei.edu.br/sigaa/verTelaLogin.do'):
        self.userlogin = userlogin
        self.userpass = userpass
        self.cookies = cookielib.CookieJar()  # cria um repositório de cookies
        self.browser = mechanize.Browser()    # inicia um browser
        self.browser.set_cookiejar(self.cookies)   # aponta para o seu repositório de cookies
        self.url = url

        #inicializando browser
      
        self.browser.open(self.url)
        self.browser.select_form(nr=0)
        self.browser.form['user.login'] = self.userlogin
        self.browser.form['user.senha'] = self.userpass
        self.browser.submit()
        self.pagina = self.browser.response().read()
        self.soup = bs(self.pagina, 'html.parser')

    def dispose(self):
        self.browser.close()

    def changeHour(self, sigaaBase):
        print(sigaaBase)
        DIAS = {
            2: 'SEG',
            3: 'TER',
            4: 'QUA',
            5: 'QUI',
            6: 'SEX',
            7: 'SAB'
        }

        HORARIOS = {
            'M1': {"inicio": '08:00', "fim": '08:55'},
            'M2': {"inicio": '08:55', "fim": '09:50'},
            'M3': {"inicio": '10:00', "fim": '10:55'},
            'M4': {"inicio": '10:55', "fim": '11:50'},
            'M5': {"inicio": '12:00', "fim": '12:55'},
            'T1': {"inicio": '12:55', "fim": '13:50'},
            'T2': {"inicio": '14:00', "fim": '14:55'},
            'T3': {"inicio": '14:55', "fim": '15:50'},
            'T4': {"inicio": '16:00', "fim": '16:55'},
            'T5': {"inicio": '16:55', "fim": '17:50'},
            'T6': {"inicio": '18:00', "fim": '18:55'},
            'T7': {"inicio": '18:55', "fim": '19:50'},
            'N1': {"inicio": '19:00', "fim": '19:50'},
            'N2': {"inicio": '19:50', "fim": '20:40'},
            'N3': {"inicio": '20:50', "fim": '21:40'},
            'N4': {"inicio": '21:40', "fim": '22:30'}
        }

        TURNOS = ['M', 'T', 'N']
    
        saida = dict()
    
        for bases in sigaaBase.split(","):

            horario = bases.strip().replace(")","").split(" (")
        
            for tempos in horario[0].split(" "):
                lista = list(tempos)

                for turno in TURNOS:
                    if(turno in lista):
                        pos = lista.index(turno)
                
                dia = [DIAS[int(dias)] for dias in lista[:pos]]
                inicio = HORARIOS[lista[pos]+lista[pos+1]]["inicio"]
                fim = HORARIOS[lista[pos]+lista[-1]]["fim"]

                saida[bases.strip() if len(horario) > 1 else tempos] = {
                    "dias_semana": dia,
                    "hr_inicio": inicio,
                    "hr_fim": fim,
                    "dias_datas":  horario[1].strip().split(" - ") if len(horario) > 1 else ""
                }
        return saida

    def getDataUser(self):
        print("iniciando busca por user: ", self.userlogin)

        try:
            perfil = self.soup.find(id="perfil-docente")
            nome = perfil.find(name="b").text
            dados_universidade = perfil.find(name="table")
            
            i = 0
            saida = dict()
            saida["nome"] = nome
           
            for row in dados_universidade.findAll("td"):
             
                if(i == 1):
                    saida["matricula"] = int(row.text.strip())
                if(i == 3):
                    saida["curso"] = row.text.strip().replace("\n","").replace("\t","")
                if(i == 5):
                    saida["nivel"] = row.text.strip()
                if(i == 7):
                    saida["status"] = row.text.strip()
                if(i == 11):
                    saida["entrada"] = row.text.strip()
                if(i == 16):
                    saida["mc"] = float(row.text.strip())
                if(i == 18):
                    saida["ira"] = float(row.text.strip())
                if(i == 20):
                    saida["iech"] = float(row.text.strip())
                if(i == 22):
                    saida["iepl"] = float(row.text.strip())
                if(i == 24):
                    saida["iea"] = float(row.text.strip())
                if(i == 26):
                    saida["iechs"] = float(row.text.strip())
                if(i == 30):
                    saida["ch_obrigatoria_pendente"] = int(row.text.strip())
                if(i == 32):
                    saida["ch_optativa_pendente"] = int(row.text.strip())
                if(i == 34):
                    saida["ch_total_curriculo"] = int(row.text.strip())
                if(i == 36):
                    saida["ch_complementar_pendente"] = int(row.text.strip())
                i += 1
            
            return saida
        except:
            return {"code": 102, "description": "Erro da coleta dos dados"}


    def getTasks(self):
        print("iniciando busca por tarefas do user: ", self.userlogin)

        atividades = self.soup.find(id="avaliacao-portal")
        vazio = atividades.find(class_='vazio')
        
        if(vazio!=None):
            return vazio.text.strip() 

        df = pd.read_html(str(atividades), header=0)[0]
        df.columns = ["feito", "data", "atividade"]
        df["feito"] = df["feito"].apply(lambda x : x==NaN if None else None )
        
        return df.to_dict('records')

    def getClasses(self):
        print("iniciando busca por aulas do user: ", self.userlogin)

        aulas = self.soup.find(id="turmas-portal")
        vazio = aulas.find(class_='vazio')
        
        if(vazio!=None):
            return vazio.text.strip() 

        df = pd.read_html(str(aulas), header=0)[-1].iloc[:,0:3].dropna()
        df.columns = ["disciplina", "local", "horario"]
        df["horario"] = df["horario"].apply(lambda x : self.changeHour(sigaaBase=x))
      
        return df.to_dict()

    def getAll(self):
        saida = {
            "user_data": self.getDataUser(),
            "tasks": self.getTasks(),
            "classes": self.getClasses(),
        }

        return saida

    def getLastClasses(self):
        self.browser.open("https://sigaa.unifei.edu.br"+"/sigaa/portais/discente/turmas.jsf")
        disciplinas = self.browser.response().read()
        soup = bs(disciplinas, 'html.parser')

        tabela = soup.find(name="table", class_="listagem")
        periodos = [p.text for p in soup.find_all( class_="periodo")]

        df = pd.read_html(str(tabela),header=1)[0].iloc[:,0:4]

        aux = 0
        saida = dict()
        for periodo in periodos:
            if(aux == 0):
                saida[periodo] = df.iloc[1:(df.loc[df['Turma'] == float(periodos[1])].index.tolist()[0]),:].to_dict('records')
            else:
                if(aux+1==len(periodos)):
                    saida[periodo] = df.iloc[(df.loc[df['Turma'] == float(periodo)].index.tolist()[0]+1):-1,:].to_dict('records')
                else:
                    saida[periodo] = df.iloc[(df.loc[df['Turma'] == float(periodos[aux-1])].index.tolist()[0]+1):(df.loc[df['Turma'] == float(periodo)].index.tolist()[0]),:].to_dict('records')
            aux += 1
        
        return saida
    
'''   
def changeHour(self, sigaaBase):
    print(sigaaBase)
    DIAS = {
        2: 'SEG',
        3: 'TER',
        4: 'QUA',
        5: 'QUI',
        6: 'SEX',
        7: 'SAB'
    }

    HORARIOS = {
        'M1': {"inicio": '08:00', "fim": '08:55'},
        'M2': {"inicio": '08:55', "fim": '09:50'},
        'M3': {"inicio": '10:00', "fim": '10:55'},
        'M4': {"inicio": '10:55', "fim": '11:50'},
        'M5': {"inicio": '12:00', "fim": '12:55'},
        'T1': {"inicio": '12:55', "fim": '13:50'},
        'T2': {"inicio": '14:00', "fim": '14:55'},
        'T3': {"inicio": '14:55', "fim": '15:50'},
        'T4': {"inicio": '16:00', "fim": '16:55'},
        'T5': {"inicio": '16:55', "fim": '17:50'},
        'T6': {"inicio": '18:00', "fim": '18:55'},
        'T7': {"inicio": '18:55', "fim": '19:50'},
        'N1': {"inicio": '19:00', "fim": '19:50'},
        'N2': {"inicio": '19:50', "fim": '20:40'},
        'N3': {"inicio": '20:50', "fim": '21:40'},
        'N4': {"inicio": '21:40', "fim": '22:30'}
    }

    TURNOS = ['M', 'T', 'N']

    saida = dict()

    for bases in sigaaBase.split(","):

        horario = bases.strip().replace(")","").split(" (")
    
        for tempos in horario[0].split(" "):
            lista = list(tempos)

            for turno in TURNOS:
                if(turno in lista):
                    pos = lista.index(turno)
            
            dia = [DIAS[int(dias)] for dias in lista[:pos]]
            inicio = HORARIOS[lista[pos]+lista[pos+1]]["inicio"]
            fim = HORARIOS[lista[pos]+lista[-1]]["fim"]

            saida[bases.strip() if len(horario) > 1 else tempos] = {
                "dias_semana": dia,
                "hr_inicio": inicio,
                "hr_fim": fim,
                "dias_datas":  horario[1].strip().split(" - ") if len(horario) > 1 else ""
            }
    return saida

  
user = ScrapingSigaa(userlogin="14755223636", userpass="Arara.azul123")
#print(changeHour(self=0, sigaaBase="3M45 5M23"))
print(user.getTasks())
user.dispose()
'''
           


            
    

