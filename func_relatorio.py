import streamlit as st
from util import string_to_list
from util import plotarRadar
from util import listaCompNon0
from util import string_to_list
from util import converte_data
from util import displayInd
import pandas as pd
import re
import datetime
from datetime import datetime
from datetime import date
from util import plot_all_employees1
from util import ListaCellNineTodos
from util import calculoDesempenho
from util import PlotDisperssao1
import plotly.graph_objs as go
from util import limpar_datas
from util import string_to_datetime
import mysql.connector

#CONEXÃO BD
conexao = mysql.connector.connect(
    passwd='nineboxeucatur',
    port=3306,
    user='ninebox',
    host='nineboxeucatur.c7rugjkck183.sa-east-1.rds.amazonaws.com',
    database='Colaboradores'
)
    

mycursor = conexao.cursor()
sql = 'SELECT * FROM Colaboradores;'
mycursor.execute(sql)
listDados2 = mycursor.fetchall()


def progress_bar(percentual,titulo):
    # Converter o valor percentual para uma porcentagem decimal
    progress_decimal = percentual / 100
    # Código HTML
    html_code = f'''
    <div class="container">
        <div class="circular-progress" style="background: conic-gradient(#D4AF37 {progress_decimal*360}deg, #ededed 0deg);">
            <span class="progress-value">{percentual}%</span>
        </div>
        <span class="text">{titulo}</span>
    </div>
    '''
    # Código CSS
    css_code = '''
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@200;300;400;500;600&display=swap');
        *{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            
        }
        body{
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #7d2ae8;
            
        }
        .container{
            display: flex;
            width: 100%;
            padding: 10px;
            border-radius: 15px;
            background: #fff;
            row-gap: 30px;
            flex-direction: column;
            align-items: center;
            box-sizing: border-box;
            font-family: 'Poppins', sans-serif; 
        }
        .circular-progress{
            position: relative;
            height: 150px;
            width: 150px;
            border-radius: 50%;
            background: conic-gradient(#7d2ae8 3.6deg, #ededed 0deg);
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .circular-progress::before{
            content: "";
            position: absolute;
            height: 115px;
            width: 115px;
            border-radius: 50%;
            background-color: #fff;
        }
        .progress-value{
            position: relative;
            font-size: 30px;
            font-weight: 600;
            color: black;
        }
        .text{
            font-size: 15px;
            font-weight: 500;
            color: black;
        }
    </style>
    '''
    # Exibir o código HTML e CSS usando st.markdown()
    st.markdown(html_code, unsafe_allow_html=True)
    st.markdown(css_code, unsafe_allow_html=True)

def ordena_data(lista_datas):
  maior = datetime.date(1999, 1, 1)  
  for a in lista_datas:
    if a > maior:
      maior = a

    

import datetime
def ordena_datas(datas):
    datas.sort()
    return datas


def contador_basico(lista):
    cont = 0
    for dado in lista:
        cont += 1

    return cont


def media_compet(lista):
    soma = 0
    cont = 0
    for a in lista:
      if a > 0:
        soma += a
        cont += 1
    
    if soma > 0 and cont > 0:
      media = soma / cont
    else:
      media = 0
    
    return media


def limpar_dados(lista):
      for a in range(len(lista)):
        if str(lista[a]) == 'None':
          lista[a] = 0                          
      
      return lista


def soma_horas(lista_horas):
    soma = 0
    for numbers in lista_horas:
        soma += int(numbers)
    return soma


def media_bas(lista_to_lista):
    soma = 0
    contad = 0

    for lista in lista_to_lista:
        for number in lista:
            contad += 1
            soma += int(number)

    media = soma / contad
    return media


def soma_lista_to_lista(lista_to_lista):
    soma = 0
    for lista_horas in lista_to_lista:
        for numbers in lista_horas:
            soma += int(numbers)

    return soma


def divisaoSecao(title):
  style23 = """
  .card23 {
    width: 100%;
    background-color: #fff;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    border-radius: 100px;
    overflow: hidden;
    border: none; /* Adiciona esta propriedade para remover a borda */
  }
  .header23 {
    background-color: #D4AF37;
    color: black;
    padding: 4px;
    text-align: center;
    font-size: 22px;
    font-weight: bold;
  }
  """
  html23 = f"""<div class="card23"><div class="header23">{title}</div>"""
  st.write(f'<style>{style23}</style>', unsafe_allow_html=True)
  st.write(f'<div>{html23}</div>', unsafe_allow_html=True)
  st.write("")


#FUNÇÕES RELATÓRIO FUNCIONAL
def comparar_periodos(listDados2, linhaBD):
  
  st.text(' ')
  datas = [str(x[12]) for x in listDados2 if x[12] != '' and x[12] != None]
  datas_datetima = [string_to_datetime(x) for x in datas]
  

  Nomes_geral = [f'{x[12]} - {x[13]}' for x in listDados2 if str(x[0]) == str(listDados2[linhaBD][0]) and f'{x[12]} - {x[13]}' != f'{listDados2[linhaBD][12]} - {listDados2[linhaBD][13]}'] 
  periodos = st.multiselect('Comparar - Períodos', Nomes_geral)

  return periodos

def novos_compromissos(listDados2, linhaBD, number_random, tipo_proc):
  with st.form(f'Myforma{number_random}'):
    col1, col2, col3 = st.columns((3, 1.5, 1.5))
    
    areas_melhorar = ['Processos', 'Projetos', 'Competências']
    
    if tipo_proc == 'PC':
      index = 0
    elif tipo_proc == 'PJ':
      index = 1
    else:
      index = 2

    with col1:
      area = st.selectbox('Área a melhorar', areas_melhorar, index=index)
    with col2:
        data_inicio = str(st.date_input(f'Data Inicio', date.today(), key=f'Inicio {number_random - 1}'))
    with col3:
        data_fim = str(st.date_input(f'Data Término', date.today(), key=f'Fim {number_random - 3}'))

    Comportamento = st.text_area(f'Comportamento a Melhorar', key=f'comport {number_random - 7}')
    plano = st.text_area(f'Plano de Ação', key=f'plano {number_random - 5}')
    recursos = st.text_area(f'Recursos Necessários | Acompanhamento', key=f'recurs {number_random - 10}')
    resultado = st.text_area(f'Resultado Previsto', key=f'result {number_random - 2}')
    check_compr = '0'
      
    st.write("---")
    st.text(' ')

    submitted3 = st.form_submit_button("Registrar Compromisso")
    if submitted3:
      sql = f'INSERT INTO compromissos_9box (matricula, nome, comport_melhorar, plano_acao, recuro_necessar, resultado_previst, data_inicio, data_fim, check_conclui, area_melhorar) VALUES ({listDados2[linhaBD][0]}, "{listDados2[linhaBD][1]}", "{Comportamento}", "{plano}", "{recursos}", "{resultado}", "{data_inicio}", "{data_fim}", "{check_compr}", "{area}");'
      mycursor.execute(sql)
      conexao.commit()
      st.success('Registro do colaborador encaminhado.')   
    

def visualizaçao_processos(listDados2, linhaBD):
    if listDados2[linhaBD][33] != None and listDados2[linhaBD][33] != "" and listDados2[linhaBD][33] != 0:
        divisaoSecao("Desempenho | Processos")
        #st.caption("<h4 style='text-align: center; color: white;'>Desempenho | Processos</h2>", unsafe_allow_html=True)
        nomeIndProc = string_to_list(listDados2[linhaBD][29])
        N_metasProc = string_to_list(listDados2[linhaBD][30])
        N_DesProc = string_to_list(listDados2[linhaBD][31])
        P_IndProc = string_to_list(listDados2[linhaBD][32])
        # st.write(listDados2[linhaBD][3],listDados2[linhaBD][4],len(listDados2[linhaBD][4]))
        if len(listDados2[linhaBD][4]) < 3:
            procCola = [listDados2[linhaBD][3]]
        else:
            procCola = listDados2[linhaBD][4].split(",")
        # st.write(procCola,nomeIndProc,N_metasProc,N_DesProc)
        lauxmedProc = []
        lista_columsProc = ["Indicador", "Meta", "Realizado", "Desempenho"]
        indicadorProc = string_to_list(listDados2[linhaBD][29])
        MetaProc = string_to_list(listDados2[linhaBD][30])
        realizadProc = string_to_list(listDados2[linhaBD][31])
        number_random = 123

        INDICADORES_PROCESSOS_TO_HTML = []
        for i in range(len(procCola)):
            lista_df_proc = []
            lista_des = []
            for j in range(len(nomeIndProc[i])):
                if P_IndProc[i][j] == 'Positivo':
                    auxI = int((float(N_DesProc[i][j]) * 100) / float(N_metasProc[i][j]))
                else:
                    auxI = int((float(N_metasProc[i][j]) * 100) / float(N_DesProc[i][j]))
                lauxmedProc.append(auxI)
                meta = round(float(MetaProc[i][j]), 2)
                realizado = round(float(realizadProc[i][j]), 2)
                desempenh = '{}%'.format(int(auxI))
                lista_des.append(desempenh)
                lista_df_proc.append([indicadorProc[i][j], '{:.2f}'.format(meta), '{:.2f}'.format(realizado), desempenh])            

            proc = re.sub("'", "", procCola[i])
            
            tab1, tab2, tab3 = st.tabs(["Indicadores", "Tabela detalhada", 'Novos Compromissos'])
            
            INDICADORES_PROCESSOS_TO_HTML.append([nomeIndProc[i], lista_des, procCola[i]])
            with tab1:
              cardPlot(f"Indicadores do Processo {proc}",nomeIndProc[i],lista_des)
              st.text(' ')
              st.text(' ')

            with tab2:
              if listDados2[linhaBD][51] != None and listDados2[linhaBD][51] != "":
                procedimentProc = string_to_list(listDados2[linhaBD][49])
                horas_procedim = string_to_list(listDados2[linhaBD][50])
                
                st.caption("<h4 style='text-align: center; color: white;'>Procedimentos do Processo</h2>", unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns((3,1,1))
                with col1:
                  st.markdown('Processo') 
                  st.subheader(re.sub("'", "", procCola[i]))
                
                col2.metric('Procedimentos', contador_basico(procedimentProc[i]))
                col3.metric('Horas', soma_horas(horas_procedim[i]))
                
                proced_for_df = []
                
                for procd_rang in range(len(procedimentProc[i])):
                  proced_for_df.append([procedimentProc[i][procd_rang], horas_procedim[i][procd_rang]])
            
                df_procd = pd.DataFrame(proced_for_df, columns=['Procedimento', 'Horas'])
                st.table(df_procd)

              st.text(' ')
              st.text(' ') 
              st.caption("<h4 style='text-align: center; color: white;'>Indicadores do Processo</h2>", unsafe_allow_html=True)
              df = pd.DataFrame(lista_df_proc, columns=lista_columsProc)
              st.table(df)
              st.text(' ')           
              st.write('---')
              
            number_random = number_random - 1 
            with tab3:
               novos_compromissos(listDados2, linhaBD, number_random, 'PC')
        
        
        medProc = sum(lauxmedProc) / len(lauxmedProc)

    else:
      medProc = 0
    
    return medProc

          
def visualizacao_Projetos(listDados2, linhaBD):
    INDICADORES_PROJETOS_TO_HTML = []
    if listDados2[linhaBD][38] != "" and listDados2[linhaBD][38] != None and listDados2[linhaBD][38] != 0:
        divisaoSecao("Desempenho | Projetos")
        #st.caption("<h4 style='text-align: center; color: white;'>Desempenho | Projetos</h2>", unsafe_allow_html=True)

        lista_columsProj = ["Indicador", "Meta", "Realizado", "Desempenho"]
        projetos = string_to_list(listDados2[linhaBD][39])
        horaProjet = string_to_list(listDados2[linhaBD][52])
        metaProj = string_to_list(listDados2[linhaBD][35])
        RealizadProj = string_to_list(listDados2[linhaBD][36])
        polaridProj = string_to_list(listDados2[linhaBD][37])
        indicadoresProj = string_to_list(listDados2[linhaBD][34])
        List_to_media = []
        number_random = 4444

        for a in range(len(projetos)):
            st.write(' ')
            lista_to_df_Proj = []
            
            for index_indicador in range(len(indicadoresProj[a])):
                if polaridProj[a][index_indicador] == 'Positivo':
                    desempenho = int(
                        (float(RealizadProj[a][index_indicador]) * 100) / float(metaProj[a][index_indicador]))
                else:
                    desempenho = int(
                        (float(metaProj[a][index_indicador]) * 100) / float(RealizadProj[a][index_indicador]))
                    
                lista_to_df_Proj.append([indicadoresProj[a][index_indicador], '{:.2f}'.format(metaProj[a][index_indicador]),
                                        '{:.2f}'.format(RealizadProj[a][index_indicador]), desempenho])
            
            tab1, tab2, tab3 = st.tabs(["Indicadores", "Tabela detalhada", "Novos Compromissos"])
            
            with tab1:
              cardPlot(f"Projeto: {projetos[a]}" ,[x[0] for x in lista_to_df_Proj], [f'{x[3]}%' for x in lista_to_df_Proj])

            with tab2:
                st.caption("<h4 style='color: white;'>Projeto</h2>", unsafe_allow_html=True)
                st.markdown(projetos[a])
                col1, col2 = st.columns((1.5,2))
                #col1.metric('Projeto', projetos[a])
                col1.metric('Indicadores', contador_basico(indicadoresProj[a]))
                col2.metric('Horas', horaProjet[a])
                st.text(' ')

                dfProj = pd.DataFrame(lista_to_df_Proj, columns=lista_columsProj)
                st.table(dfProj)
            List_to_media.append([x[3] for x in lista_to_df_Proj])
            
            number_random = number_random - 1
            with tab3:
              novos_compromissos(listDados2, linhaBD, number_random, 'PJ')
            
            st.write("")
            for b in lista_to_df_Proj:
              INDICADORES_PROJETOS_TO_HTML.append([b[0], b[3], projetos[a]])

        medProj = media_bas(List_to_media)
    
    else:
      medProj = 0
    
    return medProj
      
    
def visualizacao_competencias(listDados2, linhaBD, periodos):
    competenEucatur = ["OPPR", "Pensamento Crítico e Criativo", "Comunicação", "Foco no Cliente"]
    competenEspEucatur = ["Inteligência Emocional", "Autonomia e Proatividade", "Relacionamento e Network",
                        "Futuro e Tendências", "Raciocínio Analítico", "Empreendedorismo", "Tomada de Decisão",
                        "Visão Estratégica", "Visão Inovadora", "Liderança"]
    data_geral = [limpar_dados(list(y[14:28])) for y in listDados2 if str(y[0]) == str(listDados2[linhaBD][0])]
  
    if sum(data_geral[0]) > 0:
        divisaoSecao("Competências Comportamentais")
  
        Nomes = [f'{listDados2[linhaBD][12]} - {listDados2[linhaBD][13]}']
    
        if len(periodos) > 0:
          Nomes.extend(periodos) 
          
        periodos_date = [list(limpar_datas(x))[0] for x in Nomes]
  
        data = [limpar_dados(list(y[14:28])) for y in listDados2 if str(y[0]) == str(listDados2[linhaBD][0]) and str(y[12]) in periodos_date]
        st.text(' ')

        Nomes.append('Ideal')
        ideal_data = []
        for a in range(len(data[0])):
          if str(data[0][a]) == '0':
            ideal_data.append(0)   
          else:
            ideal_data.append(70)

        data.append(ideal_data)
        data, categories = listaCompNon0(data, competenEucatur + competenEspEucatur)
        medComp = sum(data[0]) / len(data[0])
        tab2, tab1, tab3 = st.tabs(["Gráfico Radar","Métricas", "Novos Compromissos"])
        with tab1:
            title = "Métricas"
            cardPlot(title,categories,[f"{x}%" for x in data[0]])
        with tab2:
            radar = plotarRadar(data, categories, Nomes)
            st.pyplot(radar)
        with tab3:
          novos_compromissos(listDados2, linhaBD, 10000, 'CPT')  
        st.write("")
         
    else:
        medComp = 0        
    return medComp

def visualizacao_geral(listDados2, linhaBD, medProc, medProj, medComp, periodos):
    st.text(' ')
    divisaoSecao("Avaliação Geral")
      
    tab1, tab2 = st.tabs(['Avaliação Geral', 'Histórico'])
    with tab1:
      if listDados2[linhaBD][56] != '' and listDados2[linhaBD][56] != None:
          proc_BSC = string_to_list(listDados2[linhaBD][54])
          proj_BSC = string_to_list(listDados2[linhaBD][55])
          compt_BSC = string_to_list(listDados2[linhaBD][53])
      else:
          proc_BSC = 0
          proj_BSC = 0
          compt_BSC = 0
          
      if listDados2[linhaBD][50] != "" and listDados2[linhaBD][50] != None:
          horas_procedim = string_to_list(listDados2[linhaBD][50])
          ch_proces = soma_lista_to_lista(horas_procedim)
      else:
          ch_proces = 0

      if listDados2[linhaBD][52] != "" and listDados2[linhaBD][52] != None:
          horaProjet = string_to_list(listDados2[linhaBD][52])
          ch_projet = soma_horas(horaProjet)
      else:
          horaProjet = 0
          ch_projet = 0
      if medProc == "" or medProc == 0:
          medDes = medProj
      elif medProj == "" or medProj == 0:
          medDes = medProc
      else:
          medDes = int((medProc + medProj + medComp) / 3)

      indicadores = ['Des.', 'CH', 'Peso']
      col1, col2, col3 = st.columns(3)
      with col1:
          title = "Processos"
          ind1 = '{:.0f}'.format(medProc)
          ind2 = ch_proces
          ind3 = proc_BSC
          valores = [f'{ind1}%',ind2,f'{ind3}%']
          cardPlot(title, indicadores, valores)
      with col2:
          title = "Projetos"
          ind1 = '{:.0f}'.format(medProj)
          ind2 = ch_projet
          ind3 = proj_BSC
          valores = [f'{ind1}%',ind2,f'{ind3}%']
          cardPlot(title, indicadores, valores)
      with col3:
          title = "Competências"
          ind1 = '{:.0f}'.format(medComp)
          ind2 = 0
          ind3 = compt_BSC
          valores = [f'{ind1}%',ind2,f'{ind3}%']
          cardPlot(title, indicadores, valores)
      col1, col2 = st.columns(2)
      with col1:
          st.text(' ')
          title = 'PP'
          contMed = contador_basico([x for x in [medProc, medProj] if x> 0])
          Des = soma_horas([x for x in [medProc, medProj] if x> 0]) 
          if contMed > 0 and Des > 0:
              medDes = Des / contMed
          else:
              medDes = 0
          ind = ['{:.0f}%'.format(medDes)]
          cardPlot(title, ['Des'],ind)
      with col2:
          st.text(' ')
          title = 'PPC'
          lista_indicadores = [x for x in [[medProc, proc_BSC], [medProj, proj_BSC], [medComp, compt_BSC]] if x[0]>0 ]
          
          #CONTADORES DE DESEMPENHOS E PESOS
          contDes = contador_basico(lista_indicadores)
          contPeso = contador_basico([x[1] for x in lista_indicadores])
          if contDes == 3 and contPeso == 3:   
              bsc = soma_lista_to_lista([[x[0] * x[1]] for x in lista_indicadores]) / soma_horas([x[1] for x in lista_indicadores])
          else:
              bsc = 0
              
          ind = ['{:.0f}%'.format(bsc)]
          cardPlot(title,['Des.'], ind)
    with tab2:
      ##########TRATAMENTO DOS DADOS PARA PLOTAR GRÁFICO DE LINHA###########

      #DADOS DE TODAS AS AVALIAÇÕES DAQUELA MATRICULA
      dados_outras_avaliac = [x for x in listDados2 if str(x[0]) == str(listDados2[linhaBD][0])] #and str(x[11]) != codAceUser1
  
      media_competencia = {}
      media_proj = {}
      media_proc = {}
      media_pp = {}
      media_ppc = {}
      
      for dados_user in dados_outras_avaliac:
        periodo_user_range = f'{dados_user[12]} - {dados_user[13]}'
        if periodo_user_range in periodos or periodo_user_range == f'{listDados2[linhaBD][12]} - {listDados2[linhaBD][13]}':
          #MEDIA COMPETÊNCIAS
          media = media_compet(limpar_dados(list(dados_user[14:28])))
          media_competencia[f'{dados_user[12]} - {dados_user[13]}'] = media
          
          #MEDIA PROJETOS
          if str(dados_user[38]) == '1': 
            desempenho_proj = []
            meta = string_to_list(dados_user[35])
            realizado = string_to_list(dados_user[36])
            polaridade = string_to_list(dados_user[37])

            for a in range(len(meta)):
              for b in range(len(meta[a])):
                  
                if polaridade[a][b] == 'Positivo':
                  desempenho = int(
                            (float(realizado[a][b]) * 100) / float(meta[a][b]))
                else:
                  desempenho = int(
                            (float(meta[a][b]) * 100) / float(realizado[a][b]))
                desempenho_proj.append(desempenho)

            media_proj[f'{dados_user[12]} - {dados_user[13]}'] = sum(desempenho_proj) / len(desempenho_proj)
          else:
            media_proj[f'{dados_user[12]} - {dados_user[13]}'] = 0
            desempenho_proj = [0]

          #MEDIA PROCESSOS
          if str(dados_user[33]) == '1': 
            desempenho_proc = []
            meta_proc = string_to_list(dados_user[30])
            realizado_proc = string_to_list(dados_user[31])
            polaridade_proc = string_to_list(dados_user[32])
            
            for a in range(len(meta_proc)):
              for b in range(len(meta_proc[a])):
                  
                if polaridade_proc[a][b] == 'Positivo':
                  desempenho = int(
                            (float(realizado_proc[a][b]) * 100) / float(meta_proc[a][b]))
                else:
                  desempenho = int(
                            (float(meta_proc[a][b]) * 100) / float(realizado_proc[a][b]))
                desempenho_proc.append(desempenho)

            media_proc[f'{dados_user[12]} - {dados_user[13]}'] = sum(desempenho_proc) / len(desempenho_proc)
          else:
            media_proc[f'{dados_user[12]} - {dados_user[13]}'] = 0
            desempenho_proc = [0]
      
          #PP
          pp = ((sum(desempenho_proc) / len(desempenho_proc)) + (sum(desempenho_proj) / len(desempenho_proj))) / 2
          media_pp[f'{dados_user[12]} - {dados_user[13]}'] = pp
        
          #PPC
          if dados_user[53] != None and dados_user[53] != '':
            ppc = ((media * int(dados_user[53])) + 
            ((sum(desempenho_proj) / len(desempenho_proj)) * int(dados_user[55])) + 
            ((sum(desempenho_proc) / len(desempenho_proc)) *int(dados_user[54]))) / 100

            media_ppc[f'{dados_user[12]} - {dados_user[13]}'] = ppc
          else:
            media_ppc[f'{dados_user[12]} - {dados_user[13]}'] = 0
    
      dados_finais_usuarios = {'Processos':media_proc,
                         'Projetos':media_proj,
                         'Competências':media_competencia,
                         'PP':media_pp,
                         'PPC':media_ppc}

      st.caption("<h4 style='text-align: center; color: white;'>Análise Geral</h2>", unsafe_allow_html=True)
      df = pd.DataFrame(dados_finais_usuarios)

      fig = go.Figure()
      for col in df.columns:
          fig.add_trace(go.Scatter(x=df.index, y=df[col], mode='lines+markers', name=col))

      fig.update_layout(xaxis_title='Data', yaxis_title='Valores')
      st.dataframe(df, use_container_width=True)
      st.plotly_chart(fig, use_container_width=True)

    return medDes

def visualizacao_ninebox(listDados2, linhaBD, medDes, medComp,periodos):
    if medDes > 0 and medComp > 0:
        dadosNineBoxAux = []
        cont = 0

        #PEGANDO OS DADOS DE TODAS AS AVALIAÇÕES DAQUELE USUÁRIO   
        for a in range(len(listDados2)):
           if str(listDados2[a][0]) == str(listDados2[linhaBD][0]):
              cont += 1
              compet = limpar_dados(list(listDados2[a][14:28]))
              if sum(compet) > 0:
                media_compt = media_compet(limpar_dados(list(listDados2[a][14:28])))
              else:
                 media_compt = 0

              dadosNineBoxAux.append([f'{listDados2[a][12]} - {listDados2[a][13]}', calculoDesempenho(a, listDados2), media_compt])
        
        #FILTRANDO OS DADOS PARA VISUALIZAR SOMENTE OS DADOS DOS PERÍODOS SELECIONADOS
        dadosNineBoxAux = [dadosNineBoxAux[x] for x in range(len(dadosNineBoxAux)) if dadosNineBoxAux[x][0] in periodos or dadosNineBoxAux[x][0] == f'{listDados2[linhaBD][12]} - {listDados2[linhaBD][13]}']
        
        divisaoSecao("9 Box")
        col1, col2 = st.columns(2)
        with col1:
            cellaux = ListaCellNineTodos(dadosNineBoxAux)
            st.info(cellaux)
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.pyplot(plot_all_employees1(cellaux[0], cellaux[1]))
            with col2:
                PlotDisperssao1(dadosNineBoxAux)
        st.text(" ")
        st.text(" ")
        st.text(" ")      


def visualizacao_Compromissos(listDados2, linhaBD, matricula):
  st.text(' ')
  divisaoSecao("Compromissos Assumidos")

  #CONEXÃO BD
  comando = f'SELECT * FROM compromissos_9box WHERE(matricula = {matricula});'
  mycursor.execute(comando)
  compromissos_user = mycursor.fetchall()

  if len(compromissos_user) > 0:

    #declarar os valores title, valor, porc, min_val, max_val para usar a função "displayInd"
    col1, col2, col3 = st.columns(3)
    #TOTAL DE COMPROMISSOS
    with col1:
      title = 'Todos'
      valor = str(contador_basico(compromissos_user))
      porc = ''
      min_val = 0
      max_val = int(valor)

      displayInd(title, valor, min_val, max_val)

    #COMPROMISSOS EXECUTADOS
    with col3:
      title = 'Concluidos'
      valor = str(contador_basico([x for x in compromissos_user if x[10] == '1']))
      displayInd(title, valor, min_val, max_val)

    #COMPROMISSOS PENDENTES
    with col2:
      title = 'Em andamento'
      valor = str(len([x for x in compromissos_user if x[10] != '1']))
      displayInd(title, valor, min_val, max_val)
   
    comp_compt = [x[4] for x in compromissos_user]
    comp_Plan = [x[5] for x in compromissos_user]
    comp_Recurs = [x[6] for x in compromissos_user]
    comp_Result = [x[7] for x in compromissos_user]
    comp_dat_Inin = [x[8] for x in compromissos_user]
    comp_dat_Fim = [x[9] for x in compromissos_user]
    check_db = [x[10] for x in compromissos_user]
    compr_area = [x[11] for x in compromissos_user]
  
    st.text(' ')
    for a in range(len(comp_compt)):
      if compr_area[a] != None and compr_area[a] != '': 
        name_expend = f'{comp_compt[a]} | {compr_area[a]} | {converte_data(comp_dat_Inin[a])} - {converte_data(comp_dat_Fim[a])}'
      else:
        name_expend = f'{comp_compt[a]} | {converte_data(comp_dat_Inin[a])} - {converte_data(comp_dat_Fim[a])}'

      with st.expander(f'{name_expend}'):
        st.text(' ')
        col1, col2, col3, col4 = st.columns((3.7, 2.0, 2.0, 2.0))
        with col1:
          if compr_area[a] != None and compr_area[a] != '':
            st.text_input(f'Área a melhorar', compr_area[a], key = f'area{a + 1}')
          else:
            st.text_input(f'Área a melhorar', key = f'area{a + 1}')
        with col2:
          st.text_input(f'Inicio', converte_data(comp_dat_Inin[a]), key=f'Inicio {a + 1}')
        with col3:
          st.text_input(f'Fim', converte_data(comp_dat_Fim[a]), key=f'Fim {a + 1}')
        with col4:
          st.text(" ")
          st.text(" ")
          if int(check_db[a]) == 0:
            var1 = 0
            meta = st.checkbox(f'Concluido', value=False, key=f'Concluido {a + 1}')
            if meta:
              var1 = 1
              check_db[a] = var1
          elif int(check_db[a]) == 1:
            var1 = 1
            meta = st.checkbox(f'Concluido', value=True, key=f'Concluido {a + 1}')
            if meta == False:
              var1 = 0
              check_db[a] = var1    
        st.text_input(f'Comportamento a Melhorar', str(comp_compt[a]), key=f'Comportamento a Melhorar {a + 1}')
        st.text_area(f'Plano de Ação', str(comp_Plan[a]), key=f'Plano de Ação {a + 1}')
        st.text_area(f'Recursos Necessários | Acompanhamento', str(comp_Recurs[a]), key=f'Recursos Necessários | Acompanhamento {a + 1}')
        st.text_area(f'Resultado Previsto', str(comp_Result[a]), key=f'Resultado Previsto {a + 1}')
        st.write("---")  
      
      for a in range(len(check_db)):    
        comandBDCheck = f'UPDATE compromissos_9box SET check_conclui = "{check_db[a]}" WHERE (matricula = {matricula}) AND (comport_melhorar = "{comp_compt[a]}");'
        mycursor.execute(comandBDCheck)
        conexao.commit()


def visualizacao_CPA(listDados2, linhaBD, medDes, medComp):
  if (listDados2[linhaBD][60]) == '1' and str(listDados2[linhaBD][28]) == '1':
    divisaoSecao("CPA")
    col1, col2, col3 = st.columns(3)
    capacitacBD = listDados2[linhaBD][58]
    perfilBD = listDados2[linhaBD][57]

    competencias_bd = listDados2[linhaBD][14:27]
    
    competencias = [x for x in competencias_bd if x != None]
    mediaC = int(sum(competencias) / len(competencias))
    
    with col1:
      cardPlot('Conhecimento', ['Valor'], [f'{capacitacBD}%'])

    with col2:
      cardPlot('Perfil', ['Valor'], [f'{perfilBD}%'])
    
    with col3:
      cardPlot('Atitude', ['Valor'], [f'{mediaC}%'])

    st.text(' ')
    progress_bar(int((int(capacitacBD) + int(perfilBD) + int(mediaC)) / 3), 'CPA')


      
def gerar_HTML_Caixa(title,subtitulo,valores):    
    texto = ""    
    for i in range(len(subtitulo)):
        aux = f"""<div class="skill"><div class="skill-name">{subtitulo[i]}</div><div class="skill-level"><div class="skill-percent" style="width: {valores[i]}"></div></div><div class="skill-percent-number">{valores[i]}</div></div>"""
        texto += aux
    html = f"""<div class="card"><div class="header">{title}</div><div class="body">{texto}</div></div>"""
    return html

def cardPlot(title,subtitulo,valores):

  style = """
        .card {
          width: 100%;
          background-color: #fff;
          box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
          border-radius: 10px;
          overflow: hidden;
        }
        .header {
          background-color: #06405C;
          color: #fff;
          padding: 20px;
          text-align: center;
          font-size: 18px;
          font-weight: bold
        }
        .body {
         padding: 20px;
         color: black; 
        }
        .skill {
          display: flex;
          align-items: center;
          margin-bottom: 20px;
        }
        .skill-name {
          #width: 120px;
          font-size: 16px;
          margin-right: 20px;
          
        }
        .skill-level {
          width: 100%;
          height: 10px;
          background-color: #eee;
          border-radius: 10px;
          overflow: hidden;
        }
        .skill-percent {
          background-color: #D4AF37;
          height: 100%;
        }
        .skill-percent-number {
          margin-left: 20px;
          font-size: 16px;
        }
        """

  html = gerar_HTML_Caixa(title,subtitulo,valores)

  st.write(f'<style>{style}</style>', unsafe_allow_html=True)
  st.write(f'<div>{html}</div>', unsafe_allow_html=True)
