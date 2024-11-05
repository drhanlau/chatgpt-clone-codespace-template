import streamlit as st
import openai
from datetime import datetime

# Set your OpenAI API key
# st.secrets["OPENAI_API_KEY"] should be set in Streamlit's secrets management
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


def get_personality_prediction(birthdate):
    """Get personality prediction from OpenAI based on birthdate"""

    # Calculate age and zodiac sign (optional additional context)
    today = datetime.now()
    age = (
        today.year
        - birthdate.year
        - ((today.month, today.day) < (birthdate.month, birthdate.day))
    )

    # Construct the prompt for OpenAI
    prompt = f"""Based on the birthdate {birthdate.strftime('%B %d, %Y')}, provide a brief personality analysis.
    Consider factors like:
    - General personality traits
    - Potential strengths and challenges
    - Career inclinations
    - Relationship tendencies
    Please keep the response concise and positive.

    """

    # Make API call to OpenAI
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an insightful personality analyst.",
                },
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating prediction: {str(e)}"


# Streamlit UI
st.title("🔮 Birthday Personality Analyzer")

st.write(
    """
Enter your birthdate below to receive a personalized personality analysis!
"""
)

# Date input
birthdate = st.date_input(
    "Select your birthdate",
    min_value=datetime(1900, 1, 1),
    max_value=datetime.now(),
    help="Choose your birthdate from the calendar",
)

# Generate button
if st.button("Analyze Personality"):
    with st.spinner("Generating your personality analysis..."):
        prediction = get_personality_prediction(birthdate)

        # Display results in an expander
        with st.expander("Your Personality Analysis", expanded=True):
            st.write(prediction)

        # Add a disclaimer
        st.caption(
            """
        Note: This analysis is for entertainment purposes only and is generated using AI.
        Each person is unique and not defined by their birthdate alone.
        """
        )

# Sidebar with additional information
with st.sidebar:
    st.header("About")
    st.write(
        """
    This app uses artificial intelligence to generate personality insights based on your birthdate.
    The analysis is created using OpenAI's language model.
    """
    )

    st.markdown("---")
    st.caption("Created with Streamlit and OpenAI")
