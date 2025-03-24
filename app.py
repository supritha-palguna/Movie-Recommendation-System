import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fastapi import FastAPI

# Initialize FastAPI app
app = FastAPI()

# Load dataset from local file
df = pd.read_csv("tmdb_5000_movies.csv", low_memory=False)[["title", "overview"]].dropna()

# Compute TF-IDF vectors
vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(df["overview"])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Function to get recommendations
def recommend_movies(movie_title, top_n=5):
    if movie_title not in df["title"].values:
        return {"error": "Movie not found!"}

    idx = df[df["title"] == movie_title].index[0]
    similarity_scores = list(enumerate(cosine_sim[idx]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]

    recommended_movies = [df.iloc[i[0]]["title"] for i in similarity_scores]
    return {"recommended_movies": recommended_movies}

# API endpoint
@app.get("/recommend/{movie_title}")
def get_recommendations(movie_title: str):
    return recommend_movies(movie_title)
