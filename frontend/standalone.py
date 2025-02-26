"""
Standalone Streamlit App for TailorTalk

This version of the app doesn't require a backend API.
It uses mock data and responses for demonstration purposes.
"""

import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time

# Configure the page
st.set_page_config(
    page_title="TailorTalk",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Gemini-like appearance
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
        font-family: 'Google Sans', Arial, sans-serif;
    }
    .stTextInput > div > div > input {
        background-color: white;
        border-radius: 24px;
        border: 1px solid #dadce0;
        padding: 12px 16px;
        font-size: 16px;
    }
    .stButton > button {
        background-color: #8ab4f8;
        color: #202124;
        border: none;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 24px;
        transition: background-color 0.3s;
    }
    .stButton > button:hover {
        background-color: #aecbfa;
    }
    .user-message {
        background-color: #e8f0fe;
        padding: 12px 16px;
        border-radius: 12px;
        margin-bottom: 16px;
        color: #202124;
    }
    .bot-message {
        background-color: white;
        padding: 12px 16px;
        border-radius: 12px;
        margin-bottom: 16px;
        border: 1px solid #dadce0;
        color: #202124;
    }
    h1, h2, h3 {
        color: #202124;
        font-family: 'Google Sans', Arial, sans-serif;
    }
    .stSpinner > div > div {
        border-color: #8ab4f8 !important;
    }
    .css-18e3th9 {
        padding-top: 2rem;
    }
    .css-1d391kg {
        padding-top: 3.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Load sample Titanic data
@st.cache_data
def load_titanic_data():
    """Load sample Titanic data."""
    # URL to the Titanic dataset on GitHub
    url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    try:
        df = pd.read_csv(url)
        return df
    except:
        # Fallback to a small sample if the URL is not accessible
        data = {
            'PassengerId': list(range(1, 11)),
            'Survived': [0, 1, 1, 1, 0, 0, 0, 0, 1, 1],
            'Pclass': [3, 1, 3, 1, 3, 3, 1, 3, 3, 2],
            'Name': ['Braund, Mr. Owen Harris', 'Cumings, Mrs. John Bradley (Florence Briggs Thayer)', 
                    'Heikkinen, Miss. Laina', 'Futrelle, Mrs. Jacques Heath (Lily May Peel)', 
                    'Allen, Mr. William Henry', 'Moran, Mr. James', 'McCarthy, Mr. Timothy J', 
                    'Palsson, Master. Gosta Leonard', 'Johnson, Mrs. Oscar W (Elisabeth Vilhelmina Berg)', 
                    'Nasser, Mrs. Nicholas (Adele Achem)'],
            'Sex': ['male', 'female', 'female', 'female', 'male', 'male', 'male', 'male', 'female', 'female'],
            'Age': [22, 38, 26, 35, 35, None, 54, 2, 27, 14],
            'SibSp': [1, 1, 0, 1, 0, 0, 0, 3, 0, 1],
            'Parch': [0, 0, 0, 0, 0, 0, 0, 1, 2, 0],
            'Ticket': ['A/5 21171', 'PC 17599', 'STON/O2. 3101282', '113803', '373450', '330877', 
                      '17463', '349909', '347742', '237736'],
            'Fare': [7.25, 71.2833, 7.925, 53.1, 8.05, 8.4583, 51.8625, 21.075, 11.1333, 30.0708],
            'Cabin': [None, 'C85', None, 'C123', None, None, 'E46', None, None, None],
            'Embarked': ['S', 'C', 'S', 'S', 'S', 'Q', 'S', 'S', 'S', 'C']
        }
        return pd.DataFrame(data)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'username' not in st.session_state:
    st.session_state.username = "default_user"

if 'query_input' not in st.session_state:
    st.session_state.query_input = ""

if 'titanic_data' not in st.session_state:
    st.session_state.titanic_data = load_titanic_data()

def display_message(message, is_user=False):
    """Display a message in the chat interface."""
    if is_user:
        st.markdown(f'<div class="user-message"><strong>You:</strong> {message}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-message"><strong>Bot:</strong> {message}</div>', unsafe_allow_html=True)

def generate_visualization(query_text):
    """Generate a visualization based on the query text."""
    df = st.session_state.titanic_data
    
    # Create a figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Determine the type of visualization based on the query
    if "survival rate" in query_text.lower() or "survived" in query_text.lower():
        # Survival rate visualization
        survival_counts = df['Survived'].value_counts()
        labels = ['Did not survive', 'Survived']
        colors = ['#ff6b6b', '#4ecdc4']
        
        ax.pie(survival_counts, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
        ax.set_title('Survival Rate on the Titanic')
        
    elif "class" in query_text.lower() or "pclass" in query_text.lower():
        # Class-based visualization
        sns.countplot(x='Pclass', hue='Survived', data=df, palette='viridis', ax=ax)
        ax.set_title('Survival by Passenger Class')
        ax.set_xlabel('Passenger Class')
        ax.set_ylabel('Count')
        ax.legend(['Did not survive', 'Survived'])
        
    elif "age" in query_text.lower():
        # Age distribution
        sns.histplot(data=df, x='Age', hue='Survived', multiple='stack', bins=20, ax=ax)
        ax.set_title('Age Distribution by Survival Status')
        ax.set_xlabel('Age')
        ax.set_ylabel('Count')
        
    elif "gender" in query_text.lower() or "sex" in query_text.lower():
        # Gender-based visualization
        sns.countplot(x='Sex', hue='Survived', data=df, palette='viridis', ax=ax)
        ax.set_title('Survival by Gender')
        ax.set_xlabel('Gender')
        ax.set_ylabel('Count')
        ax.legend(['Did not survive', 'Survived'])
        
    elif "fare" in query_text.lower() or "ticket price" in query_text.lower():
        # Fare distribution
        sns.boxplot(x='Survived', y='Fare', data=df, palette='viridis', ax=ax)
        ax.set_title('Fare Distribution by Survival Status')
        ax.set_xlabel('Survived')
        ax.set_ylabel('Fare')
        
    elif "embarked" in query_text.lower() or "port" in query_text.lower():
        # Embarkation port visualization
        sns.countplot(x='Embarked', hue='Survived', data=df, palette='viridis', ax=ax)
        ax.set_title('Survival by Port of Embarkation')
        ax.set_xlabel('Port of Embarkation')
        ax.set_ylabel('Count')
        ax.legend(['Did not survive', 'Survived'])
        
    else:
        # Default visualization - overall survival count
        sns.countplot(x='Survived', data=df, palette='viridis', ax=ax)
        ax.set_title('Overall Survival Count')
        ax.set_xlabel('Survived')
        ax.set_ylabel('Count')
    
    # Save the figure to a temporary file
    plt.tight_layout()
    
    # Return the figure for Streamlit to display
    return fig

def generate_response(query_text):
    """Generate a response based on the query text."""
    df = st.session_state.titanic_data
    
    # Calculate some basic statistics
    total_passengers = len(df)
    survived = df['Survived'].sum()
    survival_rate = survived / total_passengers * 100
    
    # Generate response based on query
    if "survival rate" in query_text.lower() or "survived" in query_text.lower():
        response = f"""# Survival Analysis

The overall survival rate was {survival_rate:.1f}%. Out of {total_passengers} passengers, {survived} survived the disaster.

First class passengers had a higher survival rate compared to other classes. Women and children had priority access to lifeboats, which significantly affected survival rates by gender and age.

## You might also be interested in:

- How did passenger class affect survival rates?
- What was the age distribution of Titanic passengers?
- How did gender affect survival rates?
- What was the relationship between ticket price and survival?
- Did the port of embarkation affect survival rates?
"""
        
    elif "class" in query_text.lower() or "pclass" in query_text.lower():
        # Calculate class-specific statistics
        class_stats = df.groupby('Pclass')['Survived'].mean() * 100
        
        response = f"""# Passenger Class Analysis

Passenger class had a significant impact on survival rates:

- First Class (1): {class_stats[1]:.1f}% survival rate
- Second Class (2): {class_stats[2]:.1f}% survival rate
- Third Class (3): {class_stats[3]:.1f}% survival rate

First-class passengers had better access to lifeboats and were located closer to the boat deck, which contributed to their higher survival rate.

## You might also be interested in:

- What was the overall survival rate?
- How did gender affect survival rates within each class?
- What was the relationship between ticket price and survival?
"""
        
    elif "age" in query_text.lower():
        # Calculate age-related statistics
        avg_age = df['Age'].mean()
        avg_age_survived = df[df['Survived'] == 1]['Age'].mean()
        avg_age_not_survived = df[df['Survived'] == 0]['Age'].mean()
        
        response = f"""# Age Distribution Analysis

The average age of passengers was {avg_age:.1f} years.

- Average age of survivors: {avg_age_survived:.1f} years
- Average age of non-survivors: {avg_age_not_survived:.1f} years

Children had a higher chance of survival due to the "women and children first" policy. However, many children in third class did not survive due to their location in the ship and limited access to lifeboats.

## You might also be interested in:

- What was the overall survival rate?
- How did passenger class affect survival rates?
- How did gender affect survival rates?
"""
        
    elif "gender" in query_text.lower() or "sex" in query_text.lower():
        # Calculate gender-specific statistics
        gender_stats = df.groupby('Sex')['Survived'].mean() * 100
        
        response = f"""# Gender Analysis

Gender had a dramatic impact on survival rates:

- Female: {gender_stats['female']:.1f}% survival rate
- Male: {gender_stats['male']:.1f}% survival rate

The "women and children first" policy for loading lifeboats clearly affected survival rates. This was one of the most significant factors determining survival on the Titanic.

## You might also be interested in:

- What was the overall survival rate?
- How did passenger class affect survival rates?
- What was the age distribution of survivors?
"""
        
    elif "fare" in query_text.lower() or "ticket price" in query_text.lower():
        # Calculate fare-related statistics
        avg_fare = df['Fare'].mean()
        avg_fare_survived = df[df['Survived'] == 1]['Fare'].mean()
        avg_fare_not_survived = df[df['Survived'] == 0]['Fare'].mean()
        
        response = f"""# Fare Analysis

The average fare paid by passengers was £{avg_fare:.2f}.

- Average fare paid by survivors: £{avg_fare_survived:.2f}
- Average fare paid by non-survivors: £{avg_fare_not_survived:.2f}

Passengers who paid higher fares generally had a better chance of survival. This is closely related to passenger class, as higher fares corresponded to better accommodations and closer proximity to lifeboats.

## You might also be interested in:

- What was the overall survival rate?
- How did passenger class affect survival rates?
- How did gender affect survival rates?
"""
        
    elif "embarked" in query_text.lower() or "port" in query_text.lower():
        # Calculate embarkation-specific statistics
        embarked_stats = df.groupby('Embarked')['Survived'].mean() * 100
        
        response = f"""# Embarkation Port Analysis

Survival rates varied by port of embarkation:

- Cherbourg (C): {embarked_stats.get('C', 0):.1f}% survival rate
- Queenstown (Q): {embarked_stats.get('Q', 0):.1f}% survival rate
- Southampton (S): {embarked_stats.get('S', 0):.1f}% survival rate

Passengers who embarked at Cherbourg had the highest survival rate. This may be related to the fact that more first and second-class passengers boarded at Cherbourg.

## You might also be interested in:

- What was the overall survival rate?
- How did passenger class affect survival rates?
- What was the relationship between ticket price and survival?
"""
        
    else:
        # General response for other queries
        response = f"""# Titanic Dataset Analysis

The Titanic disaster occurred on April 15, 1912, when the ship struck an iceberg during her maiden voyage.

Key statistics:
- Total passengers in dataset: {total_passengers}
- Number of survivors: {survived}
- Overall survival rate: {survival_rate:.1f}%

Survival was strongly influenced by factors such as:
- Passenger class (1st, 2nd, or 3rd)
- Gender (female passengers had higher survival rates)
- Age (children had priority)
- Fare (higher fares correlated with better survival chances)

## You might be interested in asking:

- What was the survival rate by passenger class?
- How did gender affect survival rates?
- What was the age distribution of survivors?
- Was fare price correlated with survival?
- Did the port of embarkation affect survival rates?
"""
    
    return response

def process_query(query_text):
    """Process a query and return a response with visualization."""
    # Ensure titanic_data is initialized
    if 'titanic_data' not in st.session_state:
        st.session_state.titanic_data = load_titanic_data()
        
    # Generate a text response
    text_content = generate_response(query_text)
    
    # Generate a visualization
    fig = generate_visualization(query_text)
    
    # Return the response
    return {
        "text_content": text_content,
        "visualization": fig
    }

def main():
    """Main function for the Streamlit app."""
    # Sidebar
    with st.sidebar:
        st.title("Titanic Dataset AI")
        st.markdown("---")
        st.markdown("### About")
        st.markdown(
            "This AI assistant can answer questions about the Titanic dataset. "
            "Ask questions about survival rates, passenger demographics, and more!"
        )
        st.markdown("---")
        st.markdown("### Sample Questions")
        st.markdown("- What was the overall survival rate?")
        st.markdown("- How did passenger class affect survival?")
        st.markdown("- What was the age distribution of passengers?")
        st.markdown("- How did gender affect survival rates?")
        st.markdown("- What was the relationship between ticket price and survival?")
        st.markdown("- Did the port of embarkation affect survival rates?")
        
        # Mode indicator
        st.markdown("---")
        st.info("Running in standalone mode (no backend API required)")
    
    # Main content
    st.title("Titanic Dataset Explorer")
    st.markdown("Ask questions about the Titanic dataset and get AI-powered insights with visualizations.")
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        # Ensure messages are initialized in session state
        if 'messages' not in st.session_state:
            st.session_state.messages = []
            
        for message in st.session_state.messages:
            display_message(message['text'], message['is_user'])
            if 'visualization' in message and message['visualization'] is not None:
                st.pyplot(message['visualization'])
    
    # Create a form for the input field and submit button
    with st.form(key="query_form", clear_on_submit=True):
        # Query input
        query_text = st.text_input(
            "Ask a question about the Titanic dataset:", 
            key="query_input", 
            placeholder="Type your question here..."
        )
        
        # Send button
        send_button = st.form_submit_button("Send")
    
    if send_button and query_text:
        # Ensure messages are initialized
        if 'messages' not in st.session_state:
            st.session_state.messages = []
            
        # Add user message to chat
        st.session_state.messages.append({
            'text': query_text,
            'is_user': True
        })
        
        # Display user message
        with chat_container:
            display_message(query_text, is_user=True)
        
        # Show spinner while waiting for response
        with st.spinner("Thinking..."):
            # Process the query
            time.sleep(1)  # Simulate processing time
            response = process_query(query_text)
            
            # Add bot message to chat
            message_data = {
                'text': response['text_content'],
                'is_user': False,
                'visualization': response['visualization']
            }
            
            st.session_state.messages.append(message_data)
            
            # Display bot message
            with chat_container:
                display_message(response['text_content'])
                st.pyplot(response['visualization'])

if __name__ == "__main__":
    main() 