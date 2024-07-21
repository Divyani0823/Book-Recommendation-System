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
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Year-Of-Publication'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Publisher'].values))
        
        data.append(item)
    
    return data

# Streamlit UI
st.set_page_config(page_title="Book Recommendation System", layout="wide")
st.title('📚 Book Recommendation System')
st.write('Choose between Popular Books and Collaborative Filtering based recommendations.')

# Sidebar for user profile and recommendation type
with st.sidebar:
    st.header('User Profile')
    user_name = st.text_input('Name', 'John Doe')
    user_favorites = st.multiselect('Favorite Genres', ['Fiction', 'Non-Fiction', 'Science Fiction', 'Fantasy', 'Mystery', 'Romance', 'Thriller'])
    
    st.header('Recommendation Type')
    option = st.selectbox('Select Recommendation Type', ('Popularity Based', 'Collaborative Filtering Based', 'Book Search'))

if option == 'Popularity Based':
    st.subheader('Top Popular Books')
    for index, row in popular_df.iterrows():
        with st.container():
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(row['Image-URL-M'], width=100)
            with col2:
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
            with st.container():
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.image(item[2], width=100)
                with col2:
                    st.write(f"**{item[0]}** by {item[1]}")
                    st.write(f"Year: {item[3]}, Publisher: {item[4]}")
                    st.write('---')
                    
elif option == 'Book Search':
    st.subheader('Search for Books')
    search_query = st.text_input('Enter book title or author')
    
    if st.button('Search'):
        search_results = books[books['Book-Title'].str.contains(search_query, case=False, na=False) |
                               books['Book-Author'].str.contains(search_query, case=False, na=False)]
        for index, row in search_results.iterrows():
            with st.container():
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.image(row['Image-URL-M'], width=100)
                with col2:
                    st.write(f"**{row['Book-Title']}** by {row['Book-Author']}")
                    st.write(f"Year: {row['Year-Of-Publication']}, Publisher: {row['Publisher']}")
                    st.write('---')

# Footer
st.markdown("""
    <style>
        footer {
            visibility: hidden;
        }
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            width: 100%;
            background-color: #f1f1f1;
            text-align: center;
            padding: 10px;
        }
    </style>
    <div class="footer">
        <p>&copy; 2024 Book Recommendation System. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)
