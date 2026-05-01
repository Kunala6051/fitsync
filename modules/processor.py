import pandas as pd


def load_data():
    """
    Loads and cleans the health data from a CSV file.
    
    Returns:
        pd.DataFrame: A cleaned DataFrame with missing values handled and the 'Date' column converted to datetime.
    """
    # Read the CSV file into a DataFrame
    df = pd.read_csv('data/health_data.csv')

    # Fill missing values in the 'Steps' column with the median value of that column
    df['Steps'].fillna(df['Steps'].median(), inplace=True)
    
    # Fill missing values in the 'Sleep_Hours' column with 7.0
    df['Sleep_Hours'].fillna(7.0, inplace=True)
    
    # Fill missing values in the 'Heart_Rate_bpm' column with 68
    df['Heart_Rate_bpm'].fillna(68, inplace=True)

    # Fill missing values in other columns with their respective median values
    for column in df.columns:
        if df[column].isnull().any() and column not in ['Steps', 'Sleep_Hours', 'Heart_Rate_bpm']:
            df[column].fillna(df[column].median(), inplace=True)
    
    # Convert the 'Date' column to datetime data type
    df['Date'] = pd.to_datetime(df['Date'])

    return df

def calculate_recovery_score(df):
    """
    Adds a 'Recovery_Score' column to the DataFrame, which is calculated based on Sleep_Hours,
    Heart_Rate_bpm, and Steps. The score is between 0 and 100, indicating daily recovery status.

    Parameters:
    df (pd.DataFrame): DataFrame containing health data with 'Sleep_Hours', 'Heart_Rate_bpm', and 'Steps'.

    Returns:
    pd.DataFrame: The updated DataFrame with the new 'Recovery_Score' column.
    """
    recovery_scores = []

    for _, row in df.iterrows():
        score = 100

        # Adjust score based on Sleep_Hours
        if row['Sleep_Hours'] < 6:
            score -= 30  # Significant penalty for poor sleep
        elif row['Sleep_Hours'] >= 7:
            score += 10  # Bonus for good sleep

        # Adjust score based on Heart_Rate_bpm
        if row['Heart_Rate_bpm'] < 60:
            score += 10  # Bonus for lower heart rate
        elif row['Heart_Rate_bpm'] > 80:
            score -= 10  # Penalty for higher heart rate

        # Adjust score based on Steps
        if row['Steps'] > 12000:
            score -= 10  # Slight penalty for very high activity
        elif row['Steps'] < 5000:
            score -= 10  # Penalty for very low activity

        # Ensure the score stays within 0 to 100
        score = max(0, min(score, 100))
        recovery_scores.append(score)

    df['Recovery_Score'] = recovery_scores
    return df

def process_data():
    """
    Main function to process and return the cleaned and processed DataFrame.

    Returns:
        pd.DataFrame: The final DataFrame with the Recovery Score added.
    """
    # Load and clean the data
    df = load_data()

    # Calculate and add the Recovery Score
    df = calculate_recovery_score(df)

    # Return the processed DataFrame
    return df

