import mechanize as mechanize
from bs4 import BeautifulSoup as bs
import http.cookiejar as cookielib
from numpy import NaN

import pandas as pd
from pandas.core.frame import DataFrame

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
        DIAS = {
            2: 1,
            3: 2,
            4: 3,
            5: 4,
            6: 5,
            7: 6
        }

        HORARIOS = {
            'M1': {"inicio": '07:00', "fim": '07:55'},
            'M2': {"inicio": '07:55', "fim": '08:50'},
            'M3': {"inicio": '18:50', "fim": '09:45'},
            'M4': {"inicio": '10:10', "fim": '11:05'},
            'M5': {"inicio": '11:05', "fim": '12:00'},
            'T1': {"inicio": '13:30', "fim": '14:25'},
            'T2': {"inicio": '14:25', "fim": '15:20'},
            'T3': {"inicio": '15:45', "fim": '16:40'},
            'T4': {"inicio": '16:40', "fim": '17:35'},
            'T5': {"inicio": '17:35', "fim": '18:30'},
            'N1': {"inicio": '19:00', "fim": '19:50'},
            'N2': {"inicio": '19:50', "fim": '20:40'},
            'N3': {"inicio": '21:00', "fim": '21:50'},
            'N4': {"inicio": '21:50', "fim": '22:40'},
            'N5': {"inicio": '22:40', "fim": '23:30'}

        }

        TURNOS = ['M', 'T', 'N']
    
        saida = dict()
    
        for bases in sigaaBase.split(","):

            horario = bases.strip().replace(")","").split(" (")

            dia = []
        
            for tempos in horario[0].split(" "):
                lista = list(tempos)

                for turno in TURNOS:
                    if(turno in lista):
                        pos = lista.index(turno)
              
                dia.extend(DIAS[int(dias)] for dias in lista[:pos])
                inicio = HORARIOS[lista[pos]+lista[pos+1]]["inicio"]
                fim = HORARIOS[lista[pos]+lista[-1]]["fim"]
            saida = {
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

        myatividades = self.soup.find(id="avaliacao-portal")
        vazio = myatividades.find(class_='vazio')
        
        if(vazio!=None):
            return vazio.text.strip() 

        feitos = []
        for ativ in myatividades.find_all('td', style=lambda value: value and 'text-align:center' in value):
            if (ativ.find(name="img") != None) : feitos.append(ativ.find(name="img").get('title'))
            else: feitos.append("Atividade passada")

        tipos = []
        for ativ in myatividades.find_all(name="strong"):
            tipos.append(ativ.text)

        atividades = []
        for ativ in myatividades.find_all(name="a"):
            atividades.append(ativ.text)

        disciplina = []
        for ativ in myatividades.find_all(name="small"):
            disciplina.append(ativ.text.split("\n")[2].strip())

        df_data = pd.read_html(str(myatividades), header=0)[0].iloc[:,1]
        df = DataFrame()

        df["datas"] = df_data.tolist()
        df["feitos"] = feitos
        df["tipos"] = tipos
        df["atividades"] = atividades[:-1]
        df["disciplinas"] = disciplina


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
      
        return df.to_dict('records')

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
    
