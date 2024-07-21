import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Load preprocessed data
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

# Function for collaborative filtering recommendations
def recommend(book_name):
    index = np.where(pt.index == book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]
    
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        
        data.append(item)
    
    return data

# Streamlit UI
st.title('Book Recommendation System')
st.write('Choose between Popular Books and Collaborative Filtering based recommendations.')

option = st.sidebar.selectbox('Recommendation Type', ('Popularity Based', 'Collaborative Filtering Based'))

if option == 'Popularity Based':
    st.subheader('Top Popular Books')
    for index, row in popular_df.iterrows():
        st.image(row['Image-URL-M'], width=100)
        st.write(f"**{row['Book-Title']}** by {row['Book-Author']}")
        st.write(f"Average Rating: {row['avg_rating']} (based on {row['num_ratings']} ratings)")
        st.write('---')
elif option == 'Collaborative Filtering Based':
    st.subheader('Find Books Similar to Your Favorite')
    book_list = pt.index.to_list()
    selected_book = st.selectbox('Select a book you like', book_list)
    
    if st.button('Recommend'):
        recommendations = recommend(selected_book)
        for item in recommendations:
            st.image(item[2], width=100)
            st.write(f"**{item[0]}** by {item[1]}")
            st.write('---')
