import streamlit as st
import streamlit_authenticator as stauth
from PIL import Image
import mysql.connector

conexao = mysql.connector.connect(
    passwd='nineboxeucatur',
    port=3306,
    user='ninebox',
    host='nineboxeucatur.c7rugjkck183.sa-east-1.rds.amazonaws.com',
    database='Colaboradores'
)
mycursor = conexao.cursor()


comando2 = 'SELECT * FROM Usuarios WHERE(Email IS NOT NULL);'
mycursor.execute(comando2)
dadosUser = mycursor.fetchall()


def mostrarIcon(image_url):
  st.markdown(
      f"""
      <style>
      .display-flex {{
          display: flex;
          justify-content: center;
          align-items: center;
      }}
      </style>
      <div class="display-flex">
          <img src="{image_url}" width="50%" height="50%">
      </div>
      """,
      unsafe_allow_html=True
  )


st.set_page_config(
    page_title="Home",
    page_icon=Image.open('icon.png'),
    layout="wide",
    initial_sidebar_state='collapsed'
)

names = [x[5] for x in dadosUser if x[5] != None]
usernames = [x[7] for x in dadosUser if x[7] != None]
hashed_passwords = [x[11] for x in dadosUser if x[8] != None]
funcao = [x[6] for x in dadosUser if x[6] != None]


def convert_to_dict(names, usernames, passwords):
    credentials = {"usernames": {}}
    for name, username, password in zip(names, usernames, passwords):
        user_credentials = {
            "email":username,
            "name": name,
            "password": password
        }
        credentials["usernames"][username] = user_credentials
    return credentials

credentials = convert_to_dict(names, usernames, hashed_passwords)
authenticator = stauth.Authenticate(credentials, "Teste", "abcde", 30)

col1, col2,col3 = st.columns([1,3,1])
with col2:
    name, authentication_status, username = authenticator.login('Acesse o sistema 9box', 'main')

if authentication_status == False:
    with col2:
        st.error('Email ou Senha Incorreto')
elif authentication_status == None:
    with col2:
        st.warning('Insira seu Email e Senha')
elif authentication_status:
    with st.sidebar:
        authenticator.logout('Logout', 'main')
    
    dados_to_user = [list(x) for x in dadosUser if x[7] == str(username)]

    st.image(Image.open("logo.png"), width = 180)
    st.write("")
    st.write(f"# Olá {name}!")

    def botão1(nomeBotão, link, image_url):
      st.markdown(
          f"""
          <style>
          .botao-estiloso {{
              display: flex;
              flex-direction: column;
              justify-content: center;
              align-items: center;
              background-color: #06405C;
              color: white;
              font-family: ;
              padding: 12px 35px;
              text-align: center;
              text-decoration: none;
              font-size: 15px;
              border-radius: 10px;
              transition: background-color 0.3s ease;
          }}
          .botao-estiloso:hover {{
              background-color: #D4AF37;
              border-radius: 20px;
          }}
          .botao-imagem {{
              height: 50px;
              width: 50px;
              margin-bottom: 10px;
          }}

         .botao-texto {{
            font-weight: bold;
            color: white;
          }}

         .botao-texto:hover {{
            font-weight: bold;
            color: black;
          }}
               
          </style>

          <a href="{link}" target="_self" class="botao-estiloso ">
              <img src="{image_url}" class="botao-imagem">
              <span class="botao-texto">{nomeBotão}</span>
          </a>
          """,
          unsafe_allow_html=True
      )


    st.write("---")
    col1, col2, col3 = st.columns(3)

    with col1:
      st.write("")
      nomeBotão = "Dashboard"
      link = "https://9box.eucatur.com.br/Dashboard_Administrativo"
      image_url=  "https://cdn-icons-png.flaticon.com/512/5601/5601970.png"
      botão1(nomeBotão,link,image_url)

      st.write("")
      nomeBotão = "Adicionar usuários"
      link = "https://9box.eucatur.com.br/Novo_Usu%C3%A1rio"
      image_url=  "https://cdn-icons-png.flaticon.com/512/8695/8695106.png"
      botão1(nomeBotão,link,image_url)

    with col2:
      st.write("")
      nomeBotão = "Nova Avaliação"
      link = "https://9box.eucatur.com.br/Nova_Avalia%C3%A7%C3%A3o"
      image_url=  "https://cdn-icons-png.flaticon.com/512/8528/8528054.png"
      botão1(nomeBotão,link,image_url)

      st.write("")
      nomeBotão = "Avaliar colaborador"
      link = "https://9box.eucatur.com.br/Avaliar_Colaborador"
      image_url= "https://cdn-icons-png.flaticon.com/512/8527/8527991.png"
      botão1(nomeBotão,link,image_url)


    with col3:
      st.write("")
      nomeBotão = "Relatório Funcional"
      link = "https://9box.eucatur.com.br/Relat%C3%B3rio_Funcional"
      image_url="https://cdn-icons-png.flaticon.com/512/8528/8528025.png"
      botão1(nomeBotão,link,image_url)
      
      st.write("")
      nomeBotão = 'PDI'
      link = 'https://9box.eucatur.com.br/PDI'
      image_url="https://cdn-icons-png.flaticon.com/512/4625/4625458.png"
      botão1(nomeBotão,link,image_url)
