import pandas as pd

def load_and_analyze_data(filepath):
    # Load the data
    data = pd.read_csv(filepath)
    
    # Display the first 5 rows
    print("First 5 rows of the dataset:")
    print(data.head())
    
    # Calculate and print the number of missing values in each column
    print("\nNumber of missing values in each column:")
    print(data.isnull().sum())

# Define the path to the CSV file
csv_file_path = 'data/health_data.csv'

# Run the function
load_and_analyze_data(csv_file_path)
