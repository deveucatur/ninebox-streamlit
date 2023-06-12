import streamlit as st
from util import string_to_list
from util import string_to_datetime
import datetime
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from util import soma_basica
import pymysql

conexao = pymysql.connect(
    passwd='npmyY8%UZ041',
    port=3306,
    user='ninebox',
    host='192.168.10.71',
    database='Colaboradores'
)


def limpar_nameindicador_bd(name_indicador):
    return str(name_indicador)[:-12]


def limpar_dataindicador_bd(name_indicador):
    qntd_digits = len(name_indicador) - 12
    return str(name_indicador)[qntd_digits:]


def FuncaoProcessos(dados_colab, rang, codAce):
    if dados_colab[rang][40] == "Líder de Processos":
        procCola = [dados_colab[rang][3]]
    else:
        procCola = dados_colab[rang][4].split(",")

    L_ind = []
    L_met = []
    L_Des = []
    L_Pol = []

    st.write(' ')
    col1, col2, col3 = st.columns((1.2, 1, 0.9))
    with col2:
        st.subheader('Desempenho Processos')
    st.text(' ')

    name_indicadores_limpo = [list(set([limpar_nameindicador_bd(y).strip() for y in x])) for x in string_to_list(dados_colab[rang][29])]
    name_indicadores_BD = list(string_to_list(dados_colab[rang][29]))
    meta_BD = list(string_to_list(dados_colab[rang][30]))
    realizado_BD = list(string_to_list(dados_colab[rang][31]))
    polarid_BD = list(string_to_list(dados_colab[rang][32]))
    
    periodicidade = dados_colab[rang][41]
    if periodicidade == 'Trimestral':
        vezes_periodo = 3
    elif periodicidade == 'Bimestral':
        vezes_periodo = 2
    else:                               
        vezes_periodo = 1

    cont = [[x] for x in range(len(procCola))]

    st.text(' ')
    cont = 0
    lista_indicadores_aux = []
    lista_indicadores_escolha_user = []

    qntd_indicadr = []
    for procin in range(len(procCola)):
        st.caption(procCola[procin])
        col1, col2 = st.columns((1,3))
        with col1:
            qntd_indicadr.append(st.number_input('Indicador', min_value=0, step=1, key= f'Number {procin} - {rang}'))

        for a in range(qntd_indicadr[procin]):
            cont += 1
            with col2:    
                lista_indicadores_aux.append(st.text_input('Nome Indicador', key = f'Nome Indicador {cont}'))    
        
        indicador_do_proc = [x for x in name_indicadores_limpo[procin]]
        
        #ESCOLHA DE INDICADORES DO USER
        escolha_user_indicad = st.multiselect('Escolha de Indicadores', indicador_do_proc, indicador_do_proc, key = f'{procCola[procin]} - {rang}')
        
        lista_indicadores_escolha_user.append(escolha_user_indicad)
        
        st.write('---')
    
    name_newIndicador = [] 
    for a in range(len(procCola)):
        lista = [lista_indicadores_aux[x] for x in range(int(qntd_indicadr[a]))]

        name_newIndicador.append(lista)
    
    with st.form(f"my_form1{rang}"):
        cont = 0
        for proc in range(len(procCola)):
            titulo_proc = f'<div style="text-align:center; color:White;font-size:20px">{procCola[proc]}</div>'
            st.markdown(titulo_proc, unsafe_allow_html=True)
            st.text(' ')
            
            #SEPARANDO UMA LISTA DE LISTAS POR INDICADOR DAQUELE PROCESSO - [NOME INDICADOR, META INDICADOR, DESEMPENHO INDICADOR, POLARIDADE INDICADOR, DATA INDICADOR]            
            lista_dados_indicador = [[limpar_nameindicador_bd(name_indicadores_BD[proc][x]), meta_BD[proc][x], realizado_BD[proc][x], polarid_BD[proc][x], limpar_dataindicador_bd(name_indicadores_BD[proc][x])] for x in range(len(name_indicadores_BD[proc]))]
            
            procedimentos = []
            

            if string_to_list(dados_colab[rang][49])[proc] != '[]' and string_to_list(dados_colab[rang][49])[proc] != '' and string_to_list(dados_colab[rang][49])[proc] != None:
                for a in (string_to_list(dados_colab[rang][49])[proc]):
                    procedimentos.append(a)
            
            indicadores_to_proc = list(lista_indicadores_escolha_user[proc])
            if len(name_newIndicador[proc])> 0:
                indicadores_to_proc.extend(name_newIndicador[proc])
            
            periodo_inicial = string_to_datetime(dados_colab[rang][12])    
            lista_final_indicad = []        
            list_aux_indic = [[lista_final_indicad.append(y) for y in lista_dados_indicador if str(y[0]) == x] if x in list(set([h[0] for h in lista_dados_indicador])) else [lista_final_indicad.append([f'{x}', 0, 0, 'Positivo', f'({periodo_inicial + relativedelta(months=rang)})']) for rang in range(vezes_periodo)] for x in indicadores_to_proc]


            col1, col2, col3, col4 = st.columns((1.20, 0.4, 0.5, 0.5))
            with col1:
                st.info(f"Indicadores")
            with col2:
                st.info("Meta")
            with col3:
                st.info("Realizado")
            with col4:
                st.info("Polaridade")
            L_aux1 = []
            L_aux2 = []
            L_aux3 = []
            L_aux4 = []
            
            polarid = ['Positivo', 'Negativo']
            
            for index_indc in range(len(lista_final_indicad)):
                with col1:
                    L_aux1.append(st.text_input(f'a', f'{lista_final_indicad[index_indc][0]} {lista_final_indicad[index_indc][4]}', label_visibility="hidden",key=f'name indicador {proc} - {index_indc} - {rang}'))
                with col2:
                    L_aux2.append(st.number_input(f'b', value=float(lista_final_indicad[index_indc][1]), label_visibility="hidden", min_value=(0.00), step=0.01, key=f'meta indicador {proc} - {index_indc} - {rang}'))
                with col3:
                    L_aux3.append(st.number_input(f'c', label_visibility="hidden", value=float(lista_final_indicad[index_indc][2]), min_value=(0.00), step=0.01, key=f'realizado indicador {proc} - {index_indc} - {rang}'))
                with col4:
                    L_aux4.append(st.selectbox(f'd', polarid, index=[x for x in range(len(polarid)) if str(polarid[x]) == str(lista_final_indicad[index_indc][3])][0], label_visibility="hidden", key=f'polaridade indicador {proc} - {index_indc} - {rang}'))
            L_ind.append(L_aux1)
            L_met.append(L_aux2)
            L_Des.append(L_aux3)
            L_Pol.append(L_aux4)

            st.text(" ")

        submitted1 = st.form_submit_button("Registrar Desempenho Processos")
        if submitted1:
            #DESCOBRINDO SE O CAMPO META E REALIZADO ESTÃO ZERADOS
            tem_zero = False
            for index in range(len(L_met)):
                if 0 in L_met[index] or 0 in L_Des[index]:
                    tem_zero = True
                    
            if tem_zero:
                st.warning('Os campos meta e realizado não podem conter o valor Zero.')
            
            else:
                linrow = [L_ind, L_met, L_Des, L_Pol, 1]
                colunas = ["N_IPROC", "M_IPROC", "D_IPROC", "P_IPROC", "DPROC_Check"]
                for i in range(len(colunas)):
                    sql = f'UPDATE Colaboradores SET {colunas[i]} = "{linrow[i]}"  WHERE CódAce = {int(codAce)}'
                    mycursor = conexao.cursor()
                    mycursor.execute(sql)
                    conexao.commit()
                mycursor.close()
                st.success('Registro realizado')


# REGISTRO DE PROCEDIMENTOS DE PROCESSOS
def FuncaoProcediment(dados_colab, rang, codAce):
    if dados_colab[rang][40] == "Líder de Processos":
        procCola = [dados_colab[rang][3]]
    else:
        procCola = dados_colab[rang][4].split(",")
    
    procediment_BD_colab = list(string_to_list(dados_colab[rang][49]))
    
    st.write(' ')
    st.write(' ')
    col1, col2, col3 = st.columns((1.1, 1, 0.9))
    with col2:
        st.subheader('Carga Horária Processos')
    
    new_number_procedim = []
    st.write(' ')
    colun1, colun2, colun3 = st.columns((3, 1, 1))
    for proc in range(len(procCola)):
        with colun1:
            new_number_procedim.append(st.number_input(f'Procedimentos - {procCola[proc]} - {rang}', min_value=(0), step=(1)))

            for a in range(int(new_number_procedim[proc])):
                var_aux = list(procediment_BD_colab[proc])

                var_aux.append(' ')
                procediment_BD_colab[proc] = var_aux

    lista_final_proced = []
    lista_final_horas = []
    with st.form(f'form_proced{rang}'):
        for proc in range(len(procCola)):
            colP1, colP2 = st.columns((3, 1))
            with colP1:
                st.markdown(f'Procedimentos - {procCola[proc]}')
            with colP2:
                st.markdown(f'Horas')
            lista_procedimentos = []
            lista_horas_proced = []
            
            number_total_proced = len(procediment_BD_colab[proc])

            for a in range(number_total_proced):
                coluna1, coluna2 = st.columns((3, 1))
                with coluna1:
                    proced = st.text_input(f'Procedimentos {a + 1}', f'{procediment_BD_colab[proc][a]}', key=f'Procedimentos {a + 1} - {procCola[proc]}  - {rang}', label_visibility='hidden')
                    lista_procedimentos.append(proced)
                with coluna2:
                    horas_proced = st.number_input(f'Horas {a + 1}', min_value=(1), step=(1), key=f'Horas {a + 1} - {procCola[proc]} - {rang}', label_visibility='hidden')
                    lista_horas_proced.append(horas_proced)
            lista_final_proced.append(lista_procedimentos)
            lista_final_horas.append(lista_horas_proced)

        proced_button = st.form_submit_button("Registrar Procedimentos de Processos")
        if proced_button:
            linrow = [lista_final_proced, lista_final_horas, 1]
            colunas = ["Procedimento", "hrs_procedim", "Check_proced"]
            for i in range(len(colunas)):
                sql = f'UPDATE Colaboradores SET {colunas[i]} =  "{linrow[i]}"  WHERE CódAce = {int(codAce)}'
                mycursor = conexao.cursor()
                mycursor.execute(sql)
                conexao.commit()
            mycursor.close()
            st.success('Registro realizado')
        

def FuncaoProjetos(dados_colab, rang, codAce):
    st.subheader("Desempenho Projetos")
    if str(dados_colab[rang][38]) == '1':        
        lista_projetos = string_to_list(dados_colab[rang][39])
        lista_indicadores = string_to_list(dados_colab[rang][34])
        lista_metas = string_to_list(dados_colab[rang][35])
        lista_desemp = string_to_list(dados_colab[rang][36])
        lista_polaridade = string_to_list(dados_colab[rang][37])
        lista_horas = string_to_list(dados_colab[rang][52])
    else:
        lista_projetos = []
        lista_indicadores = []
        lista_metas = []
        lista_desemp = []
        lista_polaridade = []
        lista_horas = []
   
    col1, col2, col3 = st.columns((1.5, 0.75, 0.75))
    with col3:
        qnt_projetos = st.number_input("N° Projetos", min_value=(0), step=(1), key=f'N° Projetos {rang}')
    with col1:
        for a in range(qnt_projetos):
            lista_projetos.append(st.text_input(f"", f'Nome Novo Projeto {a + 1}',key=f'Nome Projeto {a + 1} - {rang}'))
    with col2:
        for a in range(qnt_projetos):
            aux_indicadores = []
            aux_meta = []
            aux_desem = []
            aux_polaridade = []
            number_indicador = int(st.number_input(f'Indicadores', key=f'Indicadores {a + 1} - {rang}', min_value=(1), step=(1)))
            
            if number_indicador > 0:
                for number_rang in range(number_indicador):
                    aux_indicadores.append(' ')
                    aux_meta.append(0)
                    aux_desem.append(0)
                    aux_polaridade.append('Positivo')

            lista_indicadores.append(aux_indicadores)
            lista_metas.append(aux_meta)
            lista_desemp.append(aux_desem)
            lista_polaridade.append(aux_polaridade)
            lista_horas.append(1)
    
    st.text(' ')
    st.text(' ')
    st.text(' ')
    with st.form(f"my_form3{rang}"):
        if dados_colab[rang][40] == "Líder de Processos":
            procCola = [dados_colab[rang][3]]
        else:
            procCola = dados_colab[rang][4].split(",")
        L_ind = []
        L_met = []
        L_Des = []
        L_Pol = []
        

        for proj in range(len(lista_projetos)):
            colu1, colu2 = st.columns((3, 1))
            with colu1:
                st.text(' ')
                st.text(' ')
                st.subheader(f"**{lista_projetos[proj]}**")
            with colu2:
                lista_horas.append(st.number_input(f'Horas',value = int(lista_horas[proj]), key=f'Horas {proj + 1} - {rang}',min_value=(1), step=(1)))
            L_aux1 = []
            L_aux2 = []
            L_aux3 = []
            L_aux4 = []
            polarid = ['Positivo', 'Negativo']

            for a in range(len(lista_indicadores[proj])):
                if str(lista_polaridade[proj][a]) == 'Positivo':
                    index_polarid = 0
                else:
                    index_polarid = 1

                col1, col2, col3, col4 = st.columns((1.50, 0.5, 0.5, 0.75))
                with col1:
                    L_aux1.append(st.text_input(f'Indicador', lista_indicadores[proj][a], key=f'Indicador {lista_projetos[proj]} {a} -{rang}'))
                with col2:
                    L_aux2.append(st.number_input(f'Meta', value=float(lista_metas[proj][a]),  key=f'Meta {lista_projetos[proj]} {a} - {rang}', min_value=(0.00), step=0.01))
                with col3:
                    L_aux3.append(st.number_input(f'Realizado', value=float(lista_desemp[proj][a]), key=f'Realizado {lista_projetos[proj]} {a} - {rang}',min_value=(0.00), step=0.01))
                with col4:
                    L_aux4.append(st.selectbox(f'Polaridade', polarid, index=index_polarid, key=f'Polaridade {lista_projetos[proj]} {a} - {rang}'))
            
                st.write("---")
            
            L_ind.append(L_aux1)
            L_met.append(L_aux2)
            L_Des.append(L_aux3)
            L_Pol.append(L_aux4)
            print(L_Pol)
            print(L_met, L_Des, L_ind)
        submitted2 = st.form_submit_button("Registrar Desempenho Projetos")
        if submitted2:
            #DESCOBRINDO SE O CAMPO META E REALIZADO ESTÃO ZERADOS
            tem_zero = False
            for index in range(len(L_met)):
                if 0 in L_met[index] or 0 in L_Des[index]:
                    tem_zero = True
                    
            if tem_zero:
                st.warning('Os campos meta e realizado não podem conter o valor Zero.')

            else:
                linrow = [L_ind, L_met, L_Des, L_Pol, 1, lista_projetos, lista_horas]
                colunas = ["N_IPROJ", "M_IPROJ", "D_IPROJ", "P_IPROJ", "DPROJ_Check", "NAME_PROJ", "HORAS_PROJ"]
                for i in range(len(colunas)):
                    mycursor = conexao.cursor()
                    sql = f'UPDATE Colaboradores SET {colunas[i]} = "{linrow[i]}"  WHERE CódAce = {int(codAce)}'
                    mycursor.execute(sql)
                    conexao.commit()
                mycursor.close()
                st.success('Registro do colaborador encaminhado.')


def FuncaoPesosBSC(codA, rang):
    lista_pesos = ['Peso de Competências','Peso de Processos', 'Peso de Projetos']    
    pesos = []
    st.header('Pesos BSC')
    st.text(' ')
    with st.form(f'BSC {rang}'):
        for a in lista_pesos:
            coluna1, coluna2 = st.columns((3,1))
            with coluna1:
                st.text(' ')
                st.text(' ')
                st.markdown(f'{a}')
            with coluna2:
                peso_user = st.number_input('Porcetagem',max_value=100, step=1, key=f'{a} PORCEN {rang}')
        
            st.write('---')
            pesos.append(peso_user)
        submitted = st.form_submit_button("Registrar pesos")  
        
        if submitted:
            soma = soma_basica(pesos)
            if soma != 100:
                st.warning('Impossível prosseguir! A soma dos campos deve ser 100%.')
            else:
                pesos.append(1)
                coluna = ['BSC_Peso_Compr', 'BSC_Peso_Proces', 'BSC_Peso_Proj', 'BSC_check']
                for a in range(len(pesos)):    
                    comando = f'UPDATE Colaboradores SET {coluna[a]} = "{pesos[a]}"  WHERE CódAce = {int(codA)}'
                    mycursor = conexao.cursor()
                    mycursor.execute(comando)
                    conexao.commit()
                mycursor.close()
                st.success('Informações armazenadas com sucesso')


def FuncaoCPA(codA, rang, dados_colab):
    if str(dados_colab[rang][28]) == '1' and str(dados_colab[rang][60]) == '1':
        competencias_bd = dados_colab[rang][14:27]
        competencias = [x for x in competencias_bd if x != None]
        mediaC = sum(competencias) / len(competencias)
        
        st.header('CPA')
        st.text(' ')
        lista_valores = []
        topicos = ['Conhecimento', 'Perfil']
        
        with st.form(f'CPA {rang}'):
            for top in topicos:
                col_CPA, col_CPA1 = st.columns((3,1))
                with col_CPA:
                    st.text(' ')
                    st.text(' ')
                    st.markdown(f'{top}')
                
                with col_CPA1: 
                    valores = st.number_input('Porcetagem',max_value=100, step=1, key=f'{top} - {rang}')
                
                st.write('---')
                lista_valores.append(valores)
            
            col_CPA, col_CPA1 = st.columns((3,1))
            with col_CPA:
                st.text(' ')
                st.text(' ')
                st.markdown(f'Atitude')
            with col_CPA1: 
                st.number_input('Porcetagem',value=int(mediaC),max_value=100, step=1)
            
            lista_valores.append(int(mediaC))
            lista_valores.append(1)
            submittedCPA = st.form_submit_button("Registrar CPA")
            if submittedCPA: 
                mycursor = conexao.cursor()
                for a in range(len(lista_valores)):
                    coluna = ['CPA_Perfil', 'CPA_Capacit', 'CPA_Atitude', 'CPA_Check']
                    comando = f'UPDATE Colaboradores SET {coluna[a]} = "{lista_valores[a]}"  WHERE CódAce = {int(codA)}'
                    mycursor.execute(comando)
                    conexao.commit()
                mycursor.close()
                st.success('Informações armazenadas com sucesso')  