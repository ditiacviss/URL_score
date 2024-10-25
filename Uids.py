import pandas as pd
import uuid
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

# Load the CSV file into a pandas DataFrame
file_path = 'data/top-1m.csv'
df = pd.read_csv(file_path)

# Generate a random UID (first 8 characters of UUID) for each row
df['UID'] = [str(uuid.uuid4())[:8] for _ in range(len(df))]

output_file = 'data/top-1m-edit.csv'
df.to_csv(output_file, index=False)

print(f"Updated CSV file saved to {output_file}")


# import pandas as pd
# from sklearn.model_selection import train_test_split
#
# def train_model(train_data):
#     # Add your model training logic here
#     # This is a placeholder
#     return "trained_model"
#
# def svm_model(model, test_data):
# # Add your model evaluation logic here
# # This is a placeholder returning random accuracy
#     return
#
#
# file_path = 'top-1m-with-UIDs.csv'
# df = pd.read_csv(file_path)
#
# chunk_size = 500
# chunks = [df[i:i + chunk_size] for i in range(0, df.shape[0], chunk_size)]
#
# for chunk_num, chunk in enumerate(chunks):
#     print(f"Processing chunk {chunk_num + 1}/{len(chunks)}")
#     train_data, test_data = train_test_split(chunk, test_size=0.2, random_state=42)
#     model = train_model(train_data)
#     test_accuracy = svm_model(model, test_accuracy)
#     print(f"Initial test accuracy: {test_accuracy:.2f}")
#
#     accuracy_threshold = 0.8
#
#     while test_accuracy < accuracy_threshold:
#         train_data = pd.concat([train_data, test_accuracy])
#         remaining_data = chunk[len(train_data):]
#         if remaining_data.empty:
#             print("No more data to add to training from this chunk.")
#             break
#
#         test_data, remaining_data = train_test_split(remaining_data, test_size=0.8, random_state=42)
#         model = train_model(train_data)
#         test_accuracy = svm_model(model, test_data)
#         print(f"Updated validation accuracy: {test_accuracy:.2f}")
#
# print("Training and validation complete.")
