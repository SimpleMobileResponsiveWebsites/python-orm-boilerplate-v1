import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

# Database connection (replace with your actual database URL)
def get_database_connection():
    # Replace with your actual database URL
    database_url = "sqlite:///library.db"  # Example using SQLite
    return create_engine(database_url)

def get_books_by_author(author_name):
    engine = get_database_connection()
    
    # Using SQLAlchemy for safe SQL queries
    query = text("SELECT * FROM library WHERE author = :author")
    
    # Execute query and return as pandas DataFrame
    with engine.connect() as conn:
        result = pd.read_sql(query, conn, params={"author": author_name})
    return result

def main():
    st.title("Library Book Search")
    
    # Create input field for author name
    author_name = st.text_input("Enter author name:", "Linus")
    
    if st.button("Search Books"):
        try:
            # Get books and display them
            books_df = get_books_by_author(author_name)
            
            if not books_df.empty:
                st.write(f"Found {len(books_df)} books by {author_name}:")
                st.dataframe(books_df)
                
                # Optional: Display books in a more detailed format
                for _, book in books_df.iterrows():
                    with st.expander(f"📚 {book['book']}"):
                        st.write(f"Author: {book['author']}")
                        # Add more book details as needed
            else:
                st.info(f"No books found for author: {author_name}")
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
