import pandas as pd

def calculate_opportunity_scores(df):
    # Assumes df has columns: 'Outcome', 'Importance', 'Satisfaction'
    df['Opportunity Score'] = df['Importance'] + (df['Importance'] - df['Satisfaction'])
    df = df.sort_values(by='Opportunity Score', ascending=False).reset_index(drop=True)
    return df

def load_sample_outcomes():
    # Returns a small sample DataFrame for demonstration
    data = {
        'Outcome': [
            'Minimize time to gather team status updates',
            'Reduce the number of missed deadlines',
            'Improve visibility across projects',
            'Automate recurring reporting tasks',
            'Reduce the time spent switching tools'
        ],
        'Importance': [9, 8, 7, 6, 7],
        'Satisfaction': [3, 4, 5, 4, 6]
    }
    return pd.DataFrame(data)