# advanced_analysis.py

import pandas as pd
import numpy as np
from collections import Counter
import warnings

warnings.filterwarnings('ignore')

# Import VADER
try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
except ImportError:
    print("Error importing VADER. Please run: pip install vaderSentiment")

# Import TextBlob
try:
    from textblob import TextBlob
except ImportError:
    print("Error importing TextBlob. Please run: pip install textblob")

# Import NLTK
try:
    import nltk
    from nltk.tokenize import word_tokenize

    nltk.download('punkt', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
    nltk.download('wordnet', quiet=True)
except ImportError:
    print("Error importing NLTK. Please run: pip install nltk")

# Import scikit-learn
try:
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.decomposition import LatentDirichletAllocation
except ImportError:
    print("Error importing scikit-learn. Please run: pip install scikit-learn")


class AdvancedChatAnalyzer:
    def __init__(self, df):
        self.df = df.copy()
        try:
            self.analyzer = SentimentIntensityAnalyzer()
        except:
            print("Warning: VADER Sentiment Analyzer not initialized")
            self.analyzer = None

    def analyze_sentiment(self):
        """Perform VADER sentiment analysis on messages"""
        if self.analyzer is None:
            self.df['sentiment'] = 'neutral'
            return

        def get_sentiment(text):
            if isinstance(text, str):
                return self.analyzer.polarity_scores(text)
            return {'compound': 0, 'pos': 0, 'neg': 0, 'neu': 0}

        self.df['sentiment_scores'] = self.df['message'].apply(get_sentiment)
        self.df['sentiment'] = self.df['sentiment_scores'].apply(
            lambda x: 'positive' if x['compound'] > 0.05
            else 'negative' if x['compound'] < -0.05
            else 'neutral'
        )

    def analyze_response_patterns(self):
        """Analyze user response times and patterns"""
        try:
            self.df['next_message_time'] = self.df['date'].shift(-1)
            self.df['response_time'] = (self.df['next_message_time'] - self.df['date']).dt.total_seconds()

            response_patterns = self.df.groupby('user')['response_time'].agg([
                'mean', 'median', 'std'
            ]).reset_index()

            return response_patterns
        except Exception as e:
            print(f"Error in response patterns analysis: {e}")
            return pd.DataFrame()

    def topic_modeling(self, n_topics=3):
        """Perform LDA topic modeling"""
        try:
            # Filter out non-text messages
            text_messages = self.df[self.df['message'].notna()]['message'].astype(str)

            vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
            doc_term_matrix = vectorizer.fit_transform(text_messages)

            lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
            lda.fit(doc_term_matrix)

            feature_names = vectorizer.get_feature_names_out()
            topics = {}
            for topic_idx, topic in enumerate(lda.components_):
                top_words = [feature_names[i] for i in topic.argsort()[:-10:-1]]
                topics[f'Topic {topic_idx + 1}'] = top_words

            return topics
        except Exception as e:
            print(f"Error in topic modeling: {e}")
            return {'Topic 1': ['Error in topic modeling']}

    def analyze_engagement(self):
        """Analyze user engagement patterns"""
        try:
            # Message frequency by time of day
            hourly_activity = self.df.groupby('hour')['message'].count()

            # Average message length
            self.df['message_length'] = self.df['message'].astype(str).str.len()
            avg_message_length = self.df.groupby('user')['message_length'].mean()

            # Create engagement metrics DataFrame
            engagement_metrics = pd.DataFrame({
                'hourly_activity': hourly_activity,
                'avg_message_length': avg_message_length
            })

            return engagement_metrics
        except Exception as e:
            print(f"Error in engagement analysis: {e}")
            return pd.DataFrame()

    def linguistic_analysis(self):
        """Analyze linguistic patterns in messages"""
        try:
            def get_pos_tags(text):
                if isinstance(text, str):
                    tokens = word_tokenize(text)
                    return nltk.pos_tag(tokens)
                return []

            self.df['pos_tags'] = self.df['message'].apply(get_pos_tags)
            self.df['word_count'] = self.df['message'].astype(str).apply(lambda x: len(x.split()))

            return self.df[['user', 'message', 'word_count', 'pos_tags']]
        except Exception as e:
            print(f"Error in linguistic analysis: {e}")
            return pd.DataFrame()