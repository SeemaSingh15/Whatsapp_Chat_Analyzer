import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Page Config
st.set_page_config(page_title="WhatsApp Chat Analyzer", layout="wide")

# Custom Styling
st.markdown("""
    <style>
        .main {background-color: #1e1e2e; color: white;}
        h1, h2, h3, h4 {color: #f1c40f; text-align: center;}
        .stButton>button {width: 100%; border-radius: 10px; background-color: #e74c3c; color: white; font-size: 18px;}
        .stButton>button:hover {background-color: #c0392b;}
        .stMetric {text-align: center;}
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("📊 WhatsApp Chat Analyzer")
st.sidebar.markdown("Upload your chat file and explore insights!")
uploaded_file = st.sidebar.file_uploader("📂 Upload your chat file (TXT)", type=["txt"])
selected_user = None

# Main Title and About Section
st.title("📊 WhatsApp Chat Analyzer")
st.subheader("📌 About the Project")
st.markdown(
    """
    **WhatsApp Chat Analyzer** provides detailed insights into WhatsApp conversations, helping you visualize 
    and understand your chat patterns. Currently, it only supports the **24-hour format** and is being improved
    to support the **12-hour format.**

    Features:
    - 📊 Chat statistics (Messages, Words, Media, Links)
    - 📅 Monthly & Daily Activity Trends
    - 🔥 Weekly Heatmap Analysis
    - ☁️ WordCloud & Common Words
    - 😊 Emoji Breakdown
    """
)

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # Fetch unique users
    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("👤 Select User for Analysis", user_list)
    if st.sidebar.button("🚀 Show Analysis"):
        st.subheader("📈 Chat Insights")

        # Top Statistics
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label="💬 Total Messages", value=num_messages)
        with col2:
            st.metric(label="📝 Total Words", value=words)
        with col3:
            st.metric(label="📷 Media Shared", value=num_media_messages)
        with col4:
            st.metric(label="🔗 Links Shared", value=num_links)

        # Monthly Timeline
        st.subheader("📅 Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='cyan', marker='o')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily Timeline
        st.subheader("📆 Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='lime', marker='o')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Activity Maps
        st.subheader("📌 Activity Map")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📅 Most Active Days")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='magenta')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.subheader("📆 Most Active Months")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='yellow')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # Weekly Heatmap
        st.subheader("🔥 Weekly Activity Heatmap")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        sns.heatmap(user_heatmap, cmap="coolwarm", ax=ax)
        st.pyplot(fig)

        # WordCloud
        st.subheader("☁️ Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)

        # Most Common Words
        st.subheader("📌 Most Common Words")
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1], color='blue')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Emoji Analysis
        st.subheader("😊 Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user, df)
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)
