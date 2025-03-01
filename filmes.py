import streamlit as st
import requests
import random

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
        "page": random.randint(1, 5)  # Busca até 5 páginas
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
        "page": random.randint(1, 5)  # Busca até 5 páginas
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

# Título do aplicativo
st.title("Escolhe o que vc quer assistir gatinha 😻")

# Opção de escolha aleatória no centro da tela
st.write("---")
st.header("🎲 Escolha Aleatória")

# Escolher entre filme ou série
tipo_aleatorio = st.radio("Escolha o tipo:", ["Filme", "Série"])

if st.button("Escolher aleatoriamente"):
    if tipo_aleatorio == "Filme":
        # Busca filmes populares para escolha aleatória
        url = f"{BASE_URL}/movie/popular"
        params = {
            "api_key": API_KEY,
            "language": "pt-BR",
            "page": random.randint(1, 5)  # Busca até 5 páginas
        }
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            filmes = response.json()["results"]
            escolha = random.choice(filmes)
            titulo = escolha.get("title")
            st.success(f"🎉 Vocês devem assistir: **{titulo}**")
            if escolha.get("poster_path"):
                st.image(f"https://image.tmdb.org/t/p/w500{escolha['poster_path']}", width=300)
        else:
            st.error("Erro ao buscar filmes para escolha aleatória.")
    else:
        # Busca séries populares para escolha aleatória
        url = f"{BASE_URL}/tv/popular"
        params = {
            "api_key": API_KEY,
            "language": "pt-BR",
            "page": random.randint(1, 5)  # Busca até 5 páginas
        }
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            series = response.json()["results"]
            escolha = random.choice(series)
            titulo = escolha.get("name")
            st.success(f"🎉 Vocês devem assistir: **{titulo}**")
            if escolha.get("poster_path"):
                st.image(f"https://image.tmdb.org/t/p/w500{escolha['poster_path']}", width=300)
        else:
            st.error("Erro ao buscar séries para escolha aleatória.")

st.write("---")

# Opção de escolha aleatória por gênero
st.header("🎲 Escolha Aleatória por Gênero")
genero_aleatorio = st.selectbox("Escolha um gênero:", list(GENEROS.keys()))

if st.button(f"Escolher {genero_aleatorio} aleatoriamente"):
    if tipo_aleatorio == "Filme":
        filmes = buscar_filmes_por_genero(GENEROS[genero_aleatorio])
        if filmes:
            escolha = random.choice(filmes)
            titulo = escolha.get("title")
            st.success(f"🎉 Vocês devem assistir: **{titulo}**")
            if escolha.get("poster_path"):
                st.image(f"https://image.tmdb.org/t/p/w500{escolha['poster_path']}", width=300)
        else:
            st.warning("Nenhum filme encontrado para este gênero.")
    else:
        series = buscar_series_por_genero(GENEROS[genero_aleatorio])
        if series:
            escolha = random.choice(series)
            titulo = escolha.get("name")
            st.success(f"🎉 Vocês devem assistir: **{titulo}**")
            if escolha.get("poster_path"):
                st.image(f"https://image.tmdb.org/t/p/w500{escolha['poster_path']}", width=300)
        else:
            st.warning("Nenhuma série encontrada para este gênero.")

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