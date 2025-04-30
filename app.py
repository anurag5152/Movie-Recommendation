import pandas as pd
import streamlit as st
import pickle
import requests

# --- Function to fetch poster from TMDB ---
def fetch_poster(movie_id):
    try:
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=2dee086293a7109c9f3b5d03359fd274'
        )
        data = response.json()
        return f'https://image.tmdb.org/t/p/w500/{data["poster_path"]}'
    except:
        return 'https://via.placeholder.com/500x750?text=No+Poster+Available'

# --- Recommend movies ---
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        index = i[0]
        movie_id = movies.iloc[index]['movie_id']
        recommended_movies.append(movies.iloc[index].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters

# --- Load data ---
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# --- Custom CSS to match your design ---
st.markdown("""
    <style>
    .block-container {
        max-width: 95% !important;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    h1 {
        text-align: center;
        font-size: 48px !important;
        font-weight: 800;
        color: white;
        margin-bottom: 0.5rem;
    }

    .subheader {
        text-align: center;
        font-size: 24px;
        font-weight: 600;
        color: #cccccc;
        margin-top: 0;
        margin-bottom: 0.25rem;
    }

    .description {
        text-align: center;
        font-size: 16px;
        color: #aaaaaa;
        margin-bottom: 2rem;
    }

    .stSelectbox > div {
        width: 100% !important;
    }

    .stButton > button {
        width: 100% !important;
        border: 2px solid red;
        background-color: transparent;
        color: red;
        font-weight: 600;
    }

    .movie-title {
        text-align: center;
        font-weight: bold;
        font-size: 16px;
        margin-top: 8px;
        color: white;
    }

    h2 {
        font-size: 24px;
        font-weight: 700;
        color: white;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }

    @media (max-width: 768px) {
        h1 {
            font-size: 32px !important;
        }
        .subheader {
            font-size: 18px;
        }
        .description {
            font-size: 14px;
        }
        .movie-title {
            font-size: 14px;
        }
    }
    </style>
""", unsafe_allow_html=True)

# --- App UI Header ---
st.markdown("<h1>Movie Recommender System</h1>", unsafe_allow_html=True)
st.markdown("<p class='subheader'>Find Your Next Favorite Movie!</p>", unsafe_allow_html=True)
st.markdown("<p class='description'>Choose a movie and get recommendations based on your selection.</p>", unsafe_allow_html=True)

# --- Select Box ---
selected_movie_name = st.selectbox("Select a Movie:", movies['title'].values)

# --- Recommend Button ---
if st.button('Get Recommendations'):
    names, posters = recommend(selected_movie_name)
    st.markdown("## Recommended Movies")
    cols = st.columns(5) if len(names) >= 5 else st.columns(len(names))
    for idx, col in enumerate(cols):
        with col:
            st.image(posters[idx], use_container_width=True)
            st.markdown(f"<p class='movie-title'>{names[idx]}</p>", unsafe_allow_html=True)




# import pandas as pd
# import streamlit as st
# import pickle
#
# import requests
#
# def fetch_poster(movie_id):
#     try:
#         response = requests.get(
#             f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=2dee086293a7109c9f3b5d03359fd274')
#         data = response.json()
#         print(data)
#         return f'https://image.tmdb.org/t/p/w500/{data["poster_path"]}'
#     except:
#         return 'https://via.placeholder.com/500x750?text=No+Poster+Available'
#
#
# def recommend(movie):
#     movie_index = movies[movies['title'] == movie].index[0]
#     distances = similarity[movie_index]
#     movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
#
#     recommended_movies = []
#     recommended_movies_posters = []
#     for i in movies_list:
#         index = i[0]
#         movie_id = movies.iloc[index]['movie_id']  # Get actual TMDB movie_id
#         recommended_movies.append(movies.iloc[index].title)
#         recommended_movies_posters.append(fetch_poster(movie_id))
#
#     return recommended_movies, recommended_movies_posters
#
#
# movies_dict =pickle.load(open('movie_dict.pkl', 'rb'))
# movies=pd.DataFrame(movies_dict)
#
#
# similarity = pickle.load(open('similarity.pkl', 'rb'))
#
# st.title('Movie Recommender System')
#
# selected_movie_name = st.selectbox(
#     "Select Movies", movies['title'].values
# )
#
# if st.button('Recommend'):
#     names, posters = recommend(selected_movie_name)
#     cols = st.columns(5)
#     for idx, col in enumerate(cols):
#         with col:
#             st.image(posters[idx], use_container_width=True)
#             st.markdown(f"<p style='text-align: center; font-weight: bold;'>{names[idx]}</p>", unsafe_allow_html=True)
