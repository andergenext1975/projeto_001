import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="COVID-19",
)

# Lendo o arquivo
df = pd.read_csv('covid19_variants.csv')
df = df.loc[df['variant_name'] != 'Total']

# Convertendo a coluna 'data' para o tipo datetime
df['date'] = pd.to_datetime(df['date'],format='%Y-%m-%d')

# Agrupando informações para criar os filtros
paises = list(df['area'].unique())
variantes = list(df['variant_name'].unique())
periodos = list(df['date'].dt.year.unique())

# Ordenando os resultados o Filtro
paises = sorted(paises)
variantes = sorted(variantes)

# Disponibilizando os Filtros para o Usuário
pais = st.sidebar.selectbox('Estado Americano: ',['Todos'] + paises)
variante = st.sidebar.selectbox('Variante da COVID-19: ',['Todas'] + variantes)
periodo = st.sidebar.selectbox('Período: ',['Todos'] + periodos)

# Aplicando os Filtros
if(periodo != 'Todos') :
    df = df[df['date'].dt.year==periodo]

if(pais != 'Todos') :
    st.header('Mostrando resultados de: ' + pais)
    df = df[df['area']==pais]
else:
    st.header('Mostrando todos os resultados')

if(variante != 'Todas') :
    st.subheader('Mostrando os resultado da variante: ' + variante)
    df = df[df['variant_name']==variante]
else:
    st.subheader('Mostrando todas as variantes da COVID-19')

# Agrupando as Informações por Data
dfShow = df.groupby(by = ['date']).sum()  

# Definindo os Eixos X e Y
fig = px.line(dfShow,x=dfShow.index, y='specimens')

# Definindo o Título
fig.update_layout(title='Casos diarios de Covid-19 by "Anderson Nascimento"')

# Publicando
st.plotly_chart(fig,use_container_width=True)

openai.api_key = st.secrets["OPENAI_API_KEY"]

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"
    
if "messages" not in st.session_state:
    st.session_state.messages = []
    
for message in st.session_state.messages:
     with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
if prompt := st.chat_input("E aí, posso te ajudar?"):
    st.session_state.messages.apend({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

with st.chat_message("assistant"):
    message_placeholder = st.empty()
    full_response = ""
    for response in openai.ChatCompletion.create(
        model=st.session_state["openai_model"],
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream='True',
     ):
        full_response += response.choices[0].delta.get("content","")
        message_placeholder.markdown(full_response + "")
    message_placeholder.markdown(full_response)
st.session_state.messages.apend({"role": "assistant", "content": full_response})
