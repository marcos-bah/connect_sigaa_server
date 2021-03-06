import mechanize as mechanize
from bs4 import BeautifulSoup as bs
import http.cookiejar as cookielib

import pandas as pd
from pandas.core.frame import DataFrame

import pandas as pd
from pandas.core.frame import DataFrame
   
class getGroup:
    def __name__(self):
        return 'getGroup'


    def __init__(self):
        # get col name value Código Disciplina,Turma,Professor,Link of csv file
        self.filename = "sigaa_server/CataGrupoUnifei.csv"
        self.col_name = ['codigo', 'turma', 'professor', 'wpp_url']
        self.index = 0
        pass

    def get_group_csv(self):
        # get csv file(
        pd_csv = pd.read_csv(self.filename, names=self.col_name, header=1, index_col=False).fillna('')
        json = pd_csv.to_dict('records')
        
        return json

class ScrapingSigaa():

    def __init__(self, userlogin, userpass, url='https://sigaa.unifei.edu.br/sigaa/verTelaLogin.do'):
        self.userlogin = userlogin
        self.userpass = userpass
        self.error = "Usuário e/ou senha inválidos";
        self.cookies = cookielib.CookieJar()  # cria um repositório de cookies
        self.browser = mechanize.Browser()    # inicia um browser
        self.browser.set_handle_robots(False)
        self.browser.set_cookiejar(self.cookies)   # aponta para o seu repositório de cookies
        self.url = url

        # inicializando grupos
        self.groups = getGroup().get_group_csv()

        #inicializando browser
      
        self.browser.open(self.url)
        self.browser.select_form(nr=0)
        self.browser.form['user.login'] = self.userlogin
        self.browser.form['user.senha'] = self.userpass
        self.browser.submit()
        self.pagina = self.browser.response().read()
        self.soup = bs(self.pagina, 'html.parser')
        self.isLoginFailed()
        self.isPageValid()

    def isLoginFailed(self):
        res = self.soup.find('center', style=lambda value: value and 'color: #922' in value)
        if(res != None):
            raise ValueError("Credencial inválida")
    
    def isPageValid(self):
        self.perfil = self.soup.find(id="perfil-docente")
        if(self.perfil == None):
            while(self.perfil == None):
                self.browser.select_form(nr=0)
                self.browser.submit()
                self.pagina = self.browser.response().read()
                self.soup = bs(self.pagina, 'html.parser')
                self.perfil = self.soup.find(id="perfil-docente")
            self.nome = self.perfil.find(name="b").text
        else:
            self.perfil = self.soup.find(id="perfil-docente")
            self.nome = self.perfil.find(name="b").text


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
            pos = 0

            horario = bases.strip().replace(")","").split(" (")

            dia = []
            inicio = []
            fim = []
        
            for tempos in horario[0].split(" "):
                lista = list(tempos)

                for turno in TURNOS:
                    if(turno in lista):
                        pos = lista.index(turno)
              
                dia.extend(DIAS[int(dias)] for dias in lista[:pos])   
                inicio.append(HORARIOS[lista[pos]+lista[pos+1]]["inicio"])
                fim.append(HORARIOS[lista[pos]+lista[-1]]["fim"])
            
            saida = {
                "dias_semana": dia,
                "hr_inicio": inicio*len(dia) if len(dia) != len(inicio) else inicio,
                "hr_fim": fim*len(dia) if len(dia) != len(fim) else fim,
                }
        return saida

    def getDataUser(self):
        print("iniciando busca por user: ", self.userlogin)

        try:
            dados_universidade = self.perfil.find(name="table")
            
            i = 0
            saida = dict()
            saida["nome"] = self.nome
           
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
        except Exception as e:
            return str(e)

    def getBodyClass(self):
        print("iniciando busca pelas atualizacoes das disciplinas")

        return ""

    def getNotices(self):
        print("iniciando busca por noticias")
        try:
            saida = []
            notices = self.soup.find(id="formAtualizacoesTurmas")
            for tables in notices.find_all('table'):
                s = {}
                i = 0
                for notice in tables.find_all('td'):
                    if(i%2==0):
                        s["title"] = notice.text.strip().replace("\t", "").replace("\n", "")
                    else:
                        s["notice"] = notice.text.strip().replace("\t", "").replace("\n", "")
                    i += 1
                saida.append(s)
        
            return saida
        except Exception as e:
            return str(e)


    def getTasks(self):
        print("iniciando busca por tarefas do user: ", self.userlogin)

        try:
            portal = self.soup.find(id="avaliacao-portal")
            vazio = portal.find(class_='vazio')
            
            if(vazio!=None):
                return vazio.text.strip() 


            df = DataFrame()
            feitos = []
            tipos = []
            atividades = []
            disciplina = []

            for ativ in portal.find_all('td', style=lambda value: value and 'text-align:center' in value):
                if (ativ.find(name="img") != None) : feitos.append(ativ.find(name="img").get('title'))
                else: feitos.append("Atividade passada")
            
            for ativ in portal.find_all(name="small"):
                novo = []
                for x in ativ.text.split("\n"):
                    item = x
                    for y in ['\n', '\t', '/', '.', '-', '(', ')']:
                        item = item.replace(y, "")
                    item = item.split(":")
                    if (item != ['']): novo.extend(item)
                novo = [elemento for elemento in novo if elemento.strip()]
                atividades.append(novo[2].strip())
                tipos.append(novo[1])
                disciplina.append(novo[0])

            df_data = pd.read_html(str(portal), header=0)[0].iloc[:,1]
            df_data = df_data.tolist()[1:]

            for x in range(len(df_data)):
                if("(" in df_data[x]):
                    if(feitos[x] == "Atividade passada"):
                        feitos[x] = "Atividade para a próxima semana"

            df["data"] = df_data
            df["data"] = df["data"].apply(lambda x : pd.to_datetime(x.split(" ")[0], dayfirst=True))
            df["feito"] = feitos
            df["tipo"] = tipos
            df["atividade"] = atividades
            df["disciplina"] = disciplina

            df = df.sort_values(by="data")

            return df.to_dict('records')
        except Exception as e:
            return str(e)
            

    def getClasses(self):
        print("iniciando busca por aulas do user: ", self.userlogin)

        try:
            aulas = self.soup.find(id="turmas-portal")
            vazio = aulas.find(class_='vazio')
            
            if(vazio!=None):
                return vazio.text.strip() 

            df = pd.read_html(str(aulas), header=0)[-1].iloc[1:,0:3].dropna()
            df.columns = ["disciplina", "local", "horario"]
            df["horario"] = df["horario"].apply(lambda x : self.changeHour(sigaaBase=x))
            return df.to_dict('records')
        except Exception as e:
            return str(e)

    def getGroups(self):
        return self.groups

    def getAll(self):
        saida = {
            "user_data": self.getDataUser(),
            "tasks": self.getTasks(),
            "classes": self.getClasses(),
            "classes_with_group" : self.getClassesWithGroup(),
            #"last_classes": self.getLastClasses(),
            "notices": self.getNotices(),
            #"groups" : self.getGroups(),
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

    def getClassesWithGroup(self):
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

        atual = saida[list(saida.keys())[0]]

        ctt = 0
        for disciplina in atual:
            atual[ctt]["Grupo"] = []
            for row in self.groups:
                if(row["codigo"] == disciplina["Disciplina"].split("-")[0].strip()):
                    atual[ctt]["Grupo"].append(row)
            ctt += 1   
        
        return saida[list(saida.keys())[0]]
    
