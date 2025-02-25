# Import necessary libraries 
import pandas as pd
import pyodbc
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download the VADER lexicon for sentiment analysis
nltk.download('vader_lexicon')

def fetch_data_from_sql():

    conn_str = (
        "Driver={SQL Server};"
        "Server=LAPTOP-UKAL22UP;"
        "Database=PortfolioProject_MarketingAnalytics;"
        "Trusted_Connection=yes;"
    )

    conn = pyodbc.connect(conn_str)
    query = "SELECT ReviewID, CustomerID, ProductID, ReviewDate, Rating, ReviewText FROM dbo.customer_reviews"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

customer_reviews_df = fetch_data_from_sql()
sia = SentimentIntensityAnalyzer()

# Define a function to calculate sentiment scores using VADER
def calculate_sentiment(review):
    # Get the sentiment scores for the review text
    sentiment = sia.polarity_scores(review)

    # Return the compound score, which is a normalized score between -1(most negative) and 1(most positive)
    return sentiment['compound'] 

# Define a function to categorize sentiment using both the sentiment score and the review rating 
def categorize_sentiment(score, rating):
    if score > 0.05:
        if rating >= 4:
            return 'Positive'
        elif rating == 3:
            return 'Mixed Positive'
        else:
            return 'Mixed Negative'
        
    elif score < -0.05:
        if rating  <= 2:
            return 'Negative'
        elif rating == 3:
            return 'Mixed Negative'
        else:
            return 'Mixed Positive'
    
    else:
        if rating >= 4:
            return 'Positive'
        elif rating <= 2:
            return 'Negative'
        else:
            return 'Neutral'
    
# Define a function to bucket sentiment scores into text ranges
def sentiment_bucket(score):
    if score >= 0.5:
        return '0.5 to 1.0' # Strongly positive sentiment
    elif 0.0 <= score < 0.5:
        return '0.0 to 0.49' # Mildly positive sentiment
    elif -0.5 <= score < 0.0:
        return '-0.49 to 0.0' # Mildly negative sentiment
    else:
        return '-1.0 to -0.5' # Strongly negative sentiment

# Apply sentiment analysis to calculate sentiment scores for each review
customer_reviews_df['SentimentScore'] = customer_reviews_df['ReviewText'].apply(calculate_sentiment)

# Apply sentiment categorization using both text and rating
customer_reviews_df['SentimentCategory'] = customer_reviews_df.apply(
    lambda row: categorize_sentiment(row['SentimentScore'], row['Rating']), axis = 1
)

# Apply sentiment bucketing to categorize scores into defined ranges
customer_reviews_df['SentimentBucket'] = customer_reviews_df['SentimentScore'].apply(sentiment_bucket)

# Display the first few rows of the DataFrame with sentiment scores, categories, and buckets
print(customer_reviews_df.head())

# Save the DataFrame with sentiment scores, categories, and buckets to a new CSV file
customer_reviews_df.to_csv('C:/Users/igsuw/OneDrive/Documents/GitHub/Projects/marketing_analytics/python_scripts/fact_customer_reviews_with_sentiment.csv', index=False)

print("output saved")