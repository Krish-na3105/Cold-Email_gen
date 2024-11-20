import streamlit as st  
from langchain_community.document_loaders import WebBaseLoader 
from chain import Chain
from portfolio import Portfolio
#from utils import clean_text

# Move st.set_page_config to the top, before any other Streamlit calls
#st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
st.set_page_config(layout="wide")

def add_background_color(color: str):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {color};
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def create_streamlit_app(llm, portfolio):
    #set background color to light grey
    add_background_color("#8fd9fb")
    
    # Set the title of the Streamlit app
    st.title("📧 Cold Mail Generator")
        
    # Input for URL
    url_input = st.text_input("Enter a URL:", value=" ")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            # Make sure the URL is valid (Basic validation)
            if not url_input.startswith("http"):
                st.error("Please enter a valid URL starting with http:// or https://")
                return

            # Load content from the URL using WebBaseLoader
            loader = WebBaseLoader([url_input])
            data = loader.load().pop().page_content

            # Load portfolio (assuming portfolio is already loaded)
            portfolio.load_portfolio()

            # Extract jobs data from the cleaned content
            jobs = llm.extract_jobs(data)

            if not jobs:
                st.warning("No jobs found in the provided content.")
                return

            # For each job, query portfolio links based on required skills
            for job in jobs:
                skills = job.get('skills', [])
                if skills:
                    links = portfolio.query_links(skills)
                else:
                    links = []

                # Generate email based on job data and portfolio links
                email = llm.write_mail(job, links)

                # Display the generated email
                st.code(email, language='markdown')

        except Exception as e:
            # If any error occurs, display it on the Streamlit UI
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    # Initialize Chain and Portfolio objects
    chain = Chain()
    portfolio = Portfolio()

    # Create the Streamlit app interface
    create_streamlit_app(chain, portfolio)
