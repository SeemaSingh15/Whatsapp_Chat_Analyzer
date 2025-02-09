# 📊 WhatsApp Chat Analyzer

## 🚀 Overview
The **WhatsApp Chat Analyzer** is a Python-based tool that provides deep insights into WhatsApp conversations. It helps users visualize chat activity, message trends, and other useful statistics. 

## 🛠️ Technologies Used
- **Python 3.7+**
- **Streamlit** for interactive UI
- **Matplotlib & Seaborn** for data visualization
- **WordCloud** for text analysis
- **Pandas** for data processing

## 🔥 Features
- **Chat Statistics**: Analyze total messages, words, media, and links shared.
- **Activity Trends**: View daily, monthly, and weekly chat patterns.
- **Heatmap Analysis**: Understand chat activity using a weekly heatmap.
- **WordCloud & Common Words**: Identify the most used words in your chats.
- **Emoji Analysis**: Discover the most used emojis in a conversation.

## ⚠️ Current Limitations
- **Only Supports 24-hour Format Chats**: The tool currently works with WhatsApp chat exports in the **24-hour format**. Support for **12-hour format** is still under development.
- **No Sentiment Analysis Yet**: Currently, the tool does not analyze the sentiment behind messages.

## 🚀 Future Scope
- **Sentiment Analysis**: Implement AI-based sentiment detection to analyze message tone.
- **Active User Tracking**: Identify the most active participants in a chat or group.
- **WhatsApp Integration**: Potentially integrate with WhatsApp to provide real-time insights.
- **Community Chat Monitoring**: Understand activity levels in WhatsApp communities, detect engagement trends, and monitor chat dynamics.
- **Chat Status Insights**: Track user availability and responsiveness within a conversation.

## 📂 How to Use
1. **Export your WhatsApp chat** (Settings → Chats → Export Chat → Without Media).
2. Upload the **.txt file** to the WhatsApp Chat Analyzer.
3. Select a user from the dropdown.
4. Click **Show Analysis** to explore the insights!

## 📥 Installation
Clone the repository and install dependencies:
```bash
git clone <https://github.com/SeemaSingh15/Whatsapp_Chat_Analyzer.git
>
cd whatsapp-chat-analyzer
pip install -r requirements.txt
streamlit run app.py
