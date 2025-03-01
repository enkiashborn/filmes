import streamlit as st
import requests
import random
import time

st.set_page_config(
    page_title="ffilmes e séries"
)


# Configuração do fundo preto e cores dos textos/botões
st.markdown(
    """
    <style>
    .stApp {
        background-color: black;
        color: white;
    }
    .stButton>button {
        color: white;
        background-color: #FF4B4B;
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #FF0000;
    }
    .stRadio>div {
        background-color: black;
        padding: 10px;
        border-radius: 10px;
    }
    .stRadio>div>label>div {
        color: white;
    }
    .stSelectbox>div>div>select {
        color: white;
        background-color: #333333;
    }
    .stSelectbox>div>div>div {
        color: white;
        background-color: #333333;
    }
    .stSelectbox>div>div>div:hover {
        background-color: #444444;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sua chave de API do TMDb
API_KEY = "d78f9edcc46b81eeaaf33881876d449e"  # Substitua pela sua chave de API
BASE_URL = "https://api.themoviedb.org/3"

# Função para buscar filmes por gênero
def buscar_filmes_por_genero(genero_id):
    url = f"{BASE_URL}/discover/movie"
    params = {
        "api_key": API_KEY,
        "language": "pt-BR",  # Para resultados em português
        "with_genres": genero_id,
        "sort_by": "popularity.desc",
        "page": random.randint(1, 100)  # Busca até 1005 páginas
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()["results"]
    else:
        st.error(f"Erro ao buscar filmes. Código de status: {response.status_code}")
        return []

# Função para buscar séries por gênero
def buscar_series_por_genero(genero_id):
    url = f"{BASE_URL}/discover/tv"
    params = {
        "api_key": API_KEY,
        "language": "pt-BR",  # Para resultados em português
        "with_genres": genero_id,
        "sort_by": "popularity.desc",
        "page": random.randint(1, 100)  # Busca até 100 páginas
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()["results"]
    else:
        st.error(f"Erro ao buscar séries. Código de status: {response.status_code}")
        return []

# Dicionário de gêneros (IDs do TMDb)
GENEROS = {
    "Ação": 28,
    "Comédia": 35,
    "Terror": 27,
    "Drama": 18,
    "Ficção Científica": 878,
    "Animação": 16,
    "Romance": 10749
}

# Função para simular a roleta
def roleta(lista, tipo_aleatorio, placeholder):
    # Escolhe um item aleatório da lista
    escolha_final = random.choice(lista)
    
    # Tempo total da roleta (6 segundos)
    tempo_total = 6.0
    inicio = time.time()
    
    while True:
        # Calcula o tempo restante
        tempo_decorrido = time.time() - inicio
        if tempo_decorrido >= tempo_total:
            break
        
        # Escolhe um item aleatório da lista
        item_aleatorio = random.choice(lista)
        if tipo_aleatorio == "Filme":
            titulo = item_aleatorio.get("title")
        else:
            titulo = item_aleatorio.get("name")
        
        # Exibe o título atual com efeito de roleta
        placeholder.markdown(
            f"""
            <div style="text-align: center; font-size: 24px; padding: 20px; border: 2px solid #FF4B4B; border-radius: 10px;">
                🎡 {titulo}
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Aumenta o tempo entre cada "giro" para simular a desaceleração
        time.sleep(0.1 * (tempo_decorrido + 1))
    
    # Exibe o resultado final
    if tipo_aleatorio == "Filme":
        titulo_final = escolha_final.get("title")
    else:
        titulo_final = escolha_final.get("name")
    
    placeholder.markdown(
        f"""
        <div style="text-align: center; font-size: 32px; padding: 20px; border: 2px solid #FF4B4B; border-radius: 10px; background-color: #FF4B4B;">
            🎉 {titulo_final}
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Exibe a imagem do filme/série escolhido
    if escolha_final.get("poster_path"):
        st.image(f"https://image.tmdb.org/t/p/w500{escolha_final['poster_path']}", width=300)

# Título do aplicativo
st.title("👾 Escolhe ai gatinha 👾")

# Opção de escolha aleatória no centro da tela
st.write("---")
st.header("🎲 Escolha Aleatória")

# Escolher entre filme ou série
tipo_aleatorio = st.radio("Escolha o tipo:", ["Filme", "Série"])

# Botão para escolha aleatória geral
if st.button("Escolher aleatoriamente"):
    if tipo_aleatorio == "Filme":
        # Busca filmes populares para escolha aleatória
        url = f"{BASE_URL}/movie/popular"
        params = {
            "api_key": API_KEY,
            "language": "pt-BR",
            "page": random.randint(1, 100)  # Busca até 100 páginas
        }
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            lista = response.json()["results"]
            placeholder = st.empty()
            roleta(lista, tipo_aleatorio, placeholder)
        else:
            st.error("Erro ao buscar filmes para escolha aleatória.")
    else:
        # Busca séries populares para escolha aleatória
        url = f"{BASE_URL}/tv/popular"
        params = {
            "api_key": API_KEY,
            "language": "pt-BR",
            "page": random.randint(1, 100)  # Busca até 100 páginas
        }
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            lista = response.json()["results"]
            placeholder = st.empty()
            roleta(lista, tipo_aleatorio, placeholder)
        else:
            st.error("Erro ao buscar séries para escolha aleatória.")

st.write("---")

# Opção de escolha aleatória por gênero
st.header("🎲 Escolha Aleatória por Gênero")
genero_aleatorio = st.selectbox("Escolha um gênero:", list(GENEROS.keys()))

# Botão para escolha aleatória por gênero
if st.button(f"Escolher {genero_aleatorio} aleatoriamente"):
    if tipo_aleatorio == "Filme":
        lista = buscar_filmes_por_genero(GENEROS[genero_aleatorio])
    else:
        lista = buscar_series_por_genero(GENEROS[genero_aleatorio])
    
    if lista:
        placeholder = st.empty()
        roleta(lista, tipo_aleatorio, placeholder)
    else:
        st.warning("Nenhum item encontrado para este gênero.")

st.write("---")

# Abas para gêneros
st.header("🎬 Catálogo por Gênero")
aba_generos = st.tabs(list(GENEROS.keys()))

for i, genero_nome in enumerate(GENEROS.keys()):
    with aba_generos[i]:
        st.write(f"### Filmes de {genero_nome}")
        filmes = buscar_filmes_por_genero(GENEROS[genero_nome])
        
        if filmes:
            for item in filmes:
                st.write(f"**{item.get('title')}**")
                if item.get("poster_path"):
                    st.image(f"https://image.tmdb.org/t/p/w500{item['poster_path']}", width=200)
                st.write(item.get("overview"))
                st.write("---")
        else:
            st.warning("Nenhum filme encontrado para este gênero.")
