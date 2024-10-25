# # import pandas as pd
# # from features.get_domain_age import get_root_domain,get_domain_creation_date,days_passed_since
# # from features.get_page_rank import pagerank
# # from features.get_CAstatus import is_free_certificate
# # from features.get_domain_validity import get_validity_period
# # from src.get_domain import get_domain
# # from features.get_securitystatus import has_protective_statuses
# # from features.get_securitystatus2 import has_strong_security_headers
# # from features.get_catchingInfo_compressedinfo import check_caching_and_compression
# # from sklearn.preprocessing import LabelEncoder, StandardScaler
# # import matplotlib.pyplot as plt
# # import joblib
# # import streamlit as st
# #
# # model = joblib.load('ocsvm_model.h5')
# # scaler = StandardScaler()
# #
# # def main():
# #     st.title("URL Legitimacy Tracker")
# #     user_input = st.text_area("Enter the URL:", "")
# #
# #     if user_input:
# #         url = user_input
# #         domain_age = []
# #         page_rank = []
# #         is_free_list = []
# #         validation_period_list = []
# #         has_protective_status_list = []
# #         has_strong_security_list = []
# #         caching_list = []
# #         compressed_list = []
# #
# #         count = 0
# #
# #         domain = get_root_domain(url)
# #         date_input = get_domain_creation_date(domain=domain)
# #         age = days_passed_since(date_input=date_input)
# #         domain_age.append(age)
# #
# #         domain = get_domain(url)
# #         rank = pagerank(domain=domain)
# #         page_rank.append(rank)
# #
# #         is_free = is_free_certificate(url)
# #         is_free_list.append(is_free)
# #
# #         validation_period = get_validity_period(url)
# #         validation_period_list.append(validation_period)
# #
# #         has_protective_status = has_protective_statuses(url)
# #         has_protective_status_list.append(has_protective_status)
# #
# #         has_strong_security = has_strong_security_headers(url)
# #         has_strong_security_list.append(has_protective_status_list)
# #
# #         caching, compressed = check_caching_and_compression(url)
# #         caching_list.append(caching)
# #         compressed_list.append(compressed)
# #         # text = get_text_from_url(url=i)
# #         # text_list.append(text)
# #         print("count is ----------->", count)
# #         print("urls is -->", url)
# #         print("age, pagerank-->", age, rank)
# #         print("Is free CA-->", is_free, validation_period, has_protective_status, has_strong_security, caching,
# #               compressed)  # ,text)
# #
# #         data = {
# #             "Url": url,
# #             'Domain Age': domain_age,
# #             'Page Rank': page_rank,
# #             'Is Free': is_free_list,
# #             'Validation Period': validation_period_list,
# #             'Has Protective Status': has_protective_status_list,
# #             'Has Strong Security': has_strong_security_list,
# #             'Caching': caching_list,
# #             'Compressed': compressed_list,
# #         }
# #
# #         def predict_url(model, scaler):
# #             # Take user input for URL features
# #             new_url_features = {
# #                 'Domain Age': input("Domain Age: "),
# #                 'Page Rank': input("Page Rank: "),
# #                 'Is Free': input("Is the URL Free (True/False)? ").capitalize(),
# #                 'Validation Period': input("Validation Period: "),
# #                 'Has Protective Status': input("Has Protective Status (True/False)? ").capitalize(),
# #                 'Has Strong Security': input("Has Strong Security (True/False)? (Comma separated list if multiple): ")
# #             }
# #
# #             # Split the 'Has Strong Security' input into a list
# #             if ',' in new_url_features['Has Strong Security']:
# #                 has_strong_security_list = [x.strip().capitalize() for x in
# #                                             new_url_features['Has Strong Security'].split(',')]
# #                 # Process the list to use the first value (or you can handle it as needed)
# #                 new_url_features['Has Strong Security'] = has_strong_security_list[
# #                     0]  # Use the first value for prediction
# #
# #             new_url_features['Caching'] = input("Caching (True/False)? ").capitalize()
# #             new_url_features['Compressed'] = input("Compressed (True/False)? ").capitalize()
# #
# #             # Convert the input features into a DataFrame
# #             new_url_df = pd.DataFrame([new_url_features])
# #
# #             # Label encode the features
# #             label_encoder = LabelEncoder()
# #             col_list = ['Is Free', 'Has Protective Status', 'Has Strong Security', 'Caching', 'Compressed']
# #             for col in new_url_df.columns:
# #                 if col in col_list:
# #                     new_url_df[col] = label_encoder.fit_transform(new_url_df[col].astype(str))
# #
# #             # Scale the data
# #             new_url_scaled = scaler.transform(new_url_df)
# #
# #             prediction = model.predict(new_url_scaled)
# #
# #             plt.scatter(new_url_scaled[:, 0], new_url_scaled[:, 1], c='green', edgecolors='black', marker='x', s=100)
# #             plt.title("New URL Prediction (Green X represents new input)")
# #             plt.show()
# #
# #             if prediction[0] == -1:
# #                 print("The URL is predicted to be an outlier (potentially suspicious).")
# #             else:
# #                 print("The URL is predicted to be an inlier (normal).")
# #
# #         predict_url(model, scaler)
# #         st.write(f"Prediction: {predict_url}")
# #
# # if __name__ == "__main__":
# #     main()
#

import streamlit as st
import pandas as pd
import joblib
import pickle
from features.get_domain_age import get_root_domain, get_domain_creation_date, days_passed_since
from features.get_page_rank import pagerank
from features.get_CAstatus import is_free_certificate
from features.get_domain_validity import get_validity_period
from src.get_domain import get_domain
from features.get_securitystatus import has_protective_statuses
from features.get_securitystatus2 import has_strong_security_headers
from features.get_catchingInfo_compressedinfo import check_caching_and_compression
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder

# import pandas as pd
# from sklearn.svm import OneClassSVM
# from sklearn.preprocessing import LabelEncoder, StandardScaler
# from sklearn.model_selection import train_test_split
# import uuid
# import matplotlib.pyplot as plt
#
# # Read and process the CSV file
# file_path = 'data/data_details.csv'
# df = pd.read_csv(file_path)
# # df['UID'] = [str(uuid.uuid4())[:8] for _ in range(len(df))]
# df.fillna(-1, inplace=True)
#
# def train_model(train_data):
#     """Train the One-Class SVM model on the training data."""
#     label_encoder = LabelEncoder()
#
#     col_list = ['Is Free', 'Has Protective Status', 'Has Strong Security', 'Caching', 'Compressed']
#     for col in train_data.columns:
#         if col in col_list:
#             train_data[col] = label_encoder.fit_transform(train_data[col].astype(str))
#
#     # Drop unnecessary columns
#     train_data = train_data.drop(columns=['Unnamed: 0', 'Url'])
#
#     # Scale the features
#     scaler = StandardScaler()
#     train_data = scaler.fit_transform(train_data)
#
#     # Fit the One-Class SVM model
#     # oc_svm = OneClassSVM(kernel='linear', nu=0.1)
#     oc_svm = OneClassSVM(kernel='poly', nu=0.1)
#     oc_svm.fit(train_data)
#
#     # from joblib import dump
#     # dump(oc_svm, 'ocsvm_model.h5')
#
#     return oc_svm, scaler  # Return both the model and the scaler
#
# def svm_model(model, test_data):
#     """Evaluate the model and return the outlier proportion."""
#     label_encoder = LabelEncoder()
#     col_list = ['Is Free', 'Has Protective Status', 'Has Strong Security', 'Caching', 'Compressed']
#     for col in test_data.columns:
#         if col in col_list:
#             test_data[col] = label_encoder.fit_transform(test_data[col].astype(str))
#
#     test_data = test_data.drop(columns=['Unnamed: 0', 'Url'])
#     test_data = test_data.values
#     y_test_pred = model.predict(test_data)
#
#     n_outliers_predicted = (y_test_pred == -1).sum()
#     outlier_proportion = n_outliers_predicted / len(y_test_pred)
#
#     # Plot the results using the first two features for 2D visualization
#     plt.figure(figsize=(8, 6))
#
#     # Color the points based on the prediction (-1 for outliers, 1 for inliers)
#     plt.scatter(test_data[:, 0], test_data[:, 1], c=y_test_pred, cmap='coolwarm', edgecolors='k', marker='o')
#
#     plt.title("One-Class SVM Predictions on Test Data")
#     plt.xlabel("Feature 1")
#     plt.ylabel("Feature 2")
#     plt.colorbar(label='Prediction (-1: Outlier, 1: Inlier)')
#     plt.show()
#
#     return outlier_proportion
#
#
# # # Main loop for chunk processing
# # file_path = 'top-1m-with-UIDs.csv'
# # df = pd.read_csv(file_path)
#
# chunk_size = 500
# chunks = [df[i:i + chunk_size] for i in range(0, df.shape[0], chunk_size)]
#
# accuracy_threshold = 1.0
#
# for chunk_num, chunk in enumerate(chunks):
#     print(f"Processing chunk {chunk_num + 1}/{len(chunks)}")
#
#     # Split the chunk into training and test sets
#     train_data, test_data = train_test_split(chunk, test_size=0.2, random_state=42)
#
#     # Train the model and calculate the initial test accuracy
#     model, scaler = train_model(train_data)
#     test_accuracy = svm_model(model, test_data)
#     # print(f"Initial test accuracy: {test_accuracy:.2f}")
#
#     # Continue training until the accuracy threshold is met
#     while test_accuracy < accuracy_threshold:
#         # Instead of concatenating test_accuracy, add more data from the remaining chunk
#         remaining_data = chunk[len(train_data):]  # Get remaining data in the chunk
#         if remaining_data.empty:
#             print("No more data to add to training from this chunk.")
#             break
#
#         train_data = pd.concat([train_data, remaining_data])  # Add remaining data to train
#         model, scaler = train_model(train_data)
#
#         # from joblib import dump
#         # dump(model, '/content/ocsvm_model.h5')
#         # import pickle
#         #
#         # with open('/content/scaler.pkl', 'wb') as f:
#         #     pickle.dump(scaler, f)
#
#         test_accuracy = svm_model(model, test_data)
#         print(f"Updated validation accuracy: {test_accuracy:.2f}")
#
# print("Training and validation complete.")
#
#
# # Streamlit App
# def main():
#     st.title("URL Legitimacy Tracker")
#
#     # User input for URL
#     url = st.text_input("Enter the URL:")
#
#     if url:
#         # Collect features based on the URL
#         domain_age = days_passed_since(get_domain_creation_date(get_root_domain(url)))
#         page_rank = pagerank(get_domain(url))
#         is_free = is_free_certificate(url)
#         validation_period = get_validity_period(url)
#         has_protective_status = has_protective_statuses(url)
#         has_strong_security = has_strong_security_headers(url)
#         caching, compressed = check_caching_and_compression(url)
#
#         # Prepare data for prediction
#         data = pd.DataFrame({
#             'Domain Age': [domain_age],
#             'Page Rank': [page_rank],
#             'Is Free': [is_free],
#             'Validation Period': [validation_period],
#             'Has Protective Status': [has_protective_status],
#             'Has Strong Security': [has_strong_security],
#             'Caching': [caching],
#             'Compressed': [compressed],
#         })
#
#         # Display the collected features
#         st.write("Collected Features:")
#         st.write(data)
#
#         # Encode and scale the data
#         label_encoder = LabelEncoder()
#         col_list = ['Is Free', 'Has Protective Status', 'Has Strong Security', 'Caching', 'Compressed']
#         for col in data.columns:
#             if col in col_list:
#                 data[col] = label_encoder.fit_transform(data[col].astype(str))
#
#         data_scaled = scaler.transform(data)
#
#         # Make prediction
#         prediction = model.predict(data_scaled)
#
#         # Display prediction result
#         if prediction[0] == -1:
#             st.write("🔴 The URL is predicted to be suspicious.")
#         else:
#             st.write("🟢 The URL is predicted to be safe.")
#
#         # Visualize the scaled data points
#         fig, ax = plt.subplots()
#         ax.scatter(data_scaled[:, 0], data_scaled[:, 1], c='green', edgecolors='black', marker='x', s=100)
#         ax.set_title("URL Prediction Visualization")
#         ax.set_xlabel("Feature 1")
#         ax.set_ylabel("Feature 2")
#         st.pyplot(fig)
#
#
# if __name__ == "__main__":
#     main()
#


import pandas as pd
from features.get_domain_age import get_root_domain, get_domain_creation_date, days_passed_since
from features.get_page_rank import pagerank
from features.get_CAstatus import is_free_certificate
from features.get_domain_validity import get_validity_period
from src.get_domain import get_domain
from features.get_securitystatus import has_protective_statuses
from features.get_securitystatus2 import has_strong_security_headers
from features.get_catchingInfo_compressedinfo import check_caching_and_compression
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.svm import OneClassSVM
from sklearn.model_selection import train_test_split
import joblib
import pickle
import streamlit as st
import matplotlib.pyplot as plt

# Load the pre-trained model and scaler
model = joblib.load('ocsvm_model.h5')
with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

# def train_model(train_data):
#     label_encoder = LabelEncoder()
#
#     col_list = ['Is Free', 'Has Protective Status', 'Has Strong Security', 'Caching', 'Compressed']
#     for col in train_data.columns:
#         if col in col_list:
#             train_data[col] = label_encoder.fit_transform(train_data[col].astype(str))
#
#     train_data = train_data.drop(columns=['Unnamed: 0', 'Url'])
#
#     scaler = StandardScaler()
#     train_data = scaler.fit_transform(train_data)
#
#     oc_svm = OneClassSVM(kernel='poly', nu=0.1)
#     oc_svm.fit(train_data)
#
#     # Save model and scaler
#     joblib.dump(oc_svm, 'ocsvm_model.h5')
#     with open('scaler.pkl', 'wb') as f:
#         pickle.dump(scaler, f)
#
#     return oc_svm, scaler
#
# def svm_model(model, test_data):
#     label_encoder = LabelEncoder()
#     col_list = ['Is Free', 'Has Protective Status', 'Has Strong Security', 'Caching', 'Compressed']
#     for col in test_data.columns:
#         if col in col_list:
#             test_data[col] = label_encoder.fit_transform(test_data[col].astype(str))
#
#     test_data = test_data.drop(columns=['Unnamed: 0', 'Url'])
#
#     test_data = test_data.values
#     y_test_pred = model.predict(test_data)
#
#     n_outliers_predicted = (y_test_pred == -1).sum()
#     outlier_proportion = n_outliers_predicted / len(y_test_pred)
#
#     # Plotting
#     plt.figure(figsize=(8, 6))
#     plt.scatter(test_data[:, 0], test_data[:, 1], c=y_test_pred, cmap='coolwarm', edgecolors='k', marker='o')
#     plt.title("One-Class SVM Predictions on Test Data")
#     plt.xlabel("Feature 1")
#     plt.ylabel("Feature 2")
#     plt.colorbar(label='Prediction (-1: Outlier, 1: Inlier)')
#     plt.show()
#
#     return outlier_proportion

def main():
    # Read and process the CSV file
    # file_path = 'data/data_details.csv'
    # df = pd.read_csv(file_path)
    # df.fillna(-1, inplace=True)
    #
    # chunk_size = 300
    # chunks = [df[i:i + chunk_size] for i in range(0, df.shape[0], chunk_size)]
    #
    # accuracy_threshold = 1.0
    #
    # for chunk_num, chunk in enumerate(chunks):
    #     print(f"Processing chunk {chunk_num + 1}/{len(chunks)}")
    #
    #     # Split the chunk into training and test sets
    #     train_data, test_data = train_test_split(chunk, test_size=0.2, random_state=42)
    #
    #     # Train the model and calculate the initial test accuracy
    #     model, scaler = train_model(train_data)
    #     test_accuracy = svm_model(model, test_data)
    #
    #     # Continue training until the accuracy threshold is met
    #     while test_accuracy < accuracy_threshold:
    #         remaining_data = chunk[len(train_data):]  # Get remaining data in the chunk
    #         if remaining_data.empty:
    #             print("No more data to add to training from this chunk.")
    #             break
    #
    #         train_data = pd.concat([train_data, remaining_data])  # Add remaining data to train
    #         model, scaler = train_model(train_data)
    #         test_accuracy = svm_model(model, test_data)
    #         print(f"Updated validation accuracy: {test_accuracy:.2f}")
    #
    # print("Training and validation complete.")

    st.title("URL Legitimacy Tracker")
    user_input = st.text_area("Enter the URL:")

    if user_input:
        try:
            url = user_input
            domain_age = days_passed_since(get_domain_creation_date(get_root_domain(url)))
            page_rank = pagerank(get_domain(url))
            is_free = is_free_certificate(url)
            validation_period = get_validity_period(url)
            has_protective_status = has_protective_statuses(url)
            has_strong_security = has_strong_security_headers(url)
            caching, compressed = check_caching_and_compression(url)

            # Create a DataFrame with the extracted features
            data = pd.DataFrame({
                'Domain Age': [domain_age],
                'Page Rank': [page_rank],
                'Is Free': [is_free],
                'Validation Period': [validation_period],
                'Has Protective Status': [has_protective_status],
                'Has Strong Security': [has_strong_security],
                'Caching': [caching],
                'Compressed': [compressed],
            })
            st.write(data)

            label_encoder = LabelEncoder()
            # Encode and scale the data for prediction
            col_list = ['Is Free', 'Has Protective Status', 'Has Strong Security', 'Caching', 'Compressed']
            for col in data.columns:
                if col in col_list:
                    data[col] = label_encoder.fit_transform(data[col].astype(str))

            data_scaled = scaler.transform(data)

            # Use the loaded model to predict
            prediction = model.predict(data_scaled)

            if prediction[0] == -1:
                st.write("🔴 The URL is predicted to be suspicious.")
            else:
                st.write("🟢 The URL is predicted to be safe.")

            # Visualize the scaled data points
            fig, ax = plt.subplots()
            ax.scatter(data_scaled[:, 0], data_scaled[:, 1], c='green', edgecolors='black', marker='x', s=100)
            ax.set_title("URL Prediction Visualization")
            st.pyplot(fig)

        except Exception as e:
            st.write(f"Error processing the URL: {e}")

if __name__ == "__main__":
    main()

