import streamlit as st
import pandas as pd
import plotly.express as px

from textblob import TextBlob


# -------------------------------
# Page Configuration
# -------------------------------

st.set_page_config(
    page_title="AI Sentiment Analyzer",
    page_icon="💬",
    layout="wide"
)


# -------------------------------
# Header
# -------------------------------

st.title(
    "💬 AI Sentiment Analysis System"
)

st.write(
    "NLP based application to analyze emotions from text data"
)

st.divider()


# -------------------------------
# Sentiment Function
# -------------------------------

def analyze_sentiment(text):

    result = TextBlob(text)

    polarity = result.sentiment.polarity


    if polarity > 0:

        sentiment = "Positive 😊"


    elif polarity < 0:

        sentiment = "Negative 😞"


    else:

        sentiment = "Neutral 😐"


    return sentiment, polarity

# -------------------------------
# Single Text Analysis
# -------------------------------

st.subheader(
    "📝 Analyze Text Sentiment"
)


user_text = st.text_area(
    "Enter your text here",
    placeholder="Example: This product is amazing..."
)


if st.button("Analyze Sentiment"):


    if user_text:


        sentiment, score = analyze_sentiment(
            user_text
        )


        col1, col2 = st.columns(2)


        with col1:

            st.metric(
                label="Detected Sentiment",
                value=sentiment
            )


        with col2:

            st.metric(
                label="Sentiment Score",
                value=round(score, 2)
            )


        # Sentiment message

        if "Positive" in sentiment:

            st.success(
                "The text shows a positive emotion."
            )


        elif "Negative" in sentiment:

            st.error(
                "The text shows a negative emotion."
            )


        else:

            st.info(
                "The text shows a neutral emotion."
            )


    else:

        st.warning(
            "Please enter some text first."
        )
    
# -------------------------------
# CSV Sentiment Analysis
# -------------------------------

st.divider()

st.subheader(
    "📂 Analyze Review Dataset"
)


uploaded_file = st.file_uploader(
    "Upload CSV file",
    type=["csv"]
)


if uploaded_file:


    df = pd.read_csv(uploaded_file)


    st.write(
        "Dataset Preview"
    )


    st.dataframe(
        df.head()
    )


    text_column = st.selectbox(
        "Select text column",
        df.columns
    )


    if st.button(
        "Analyze Dataset"
    ):


        df["Sentiment"] = df[
            text_column
        ].apply(
            lambda x: analyze_sentiment(str(x))[0]
        )


        df["Score"] = df[
            text_column
        ].apply(
            lambda x: analyze_sentiment(str(x))[1]
        )


        st.success(
            "Analysis Completed Successfully"
        )


        st.dataframe(
            df
        )


        # Sentiment count

        sentiment_count = (
            df["Sentiment"]
            .value_counts()
            .reset_index()
        )


        sentiment_count.columns = [
            "Sentiment",
            "Count"
        ]


        fig = px.pie(
            sentiment_count,
            names="Sentiment",
            values="Count",
            title="Sentiment Distribution"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )