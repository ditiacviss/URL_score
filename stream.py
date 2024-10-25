import pandas as pd
from features.get_domain_age import get_root_domain, get_domain_creation_date, days_passed_since
from features.get_page_rank import pagerank
from features.get_CAstatus import is_free_certificate
from features.get_domain_validity import get_validity_period
from src.get_domain import get_domain
from features.get_securitystatus import has_protective_statuses
from features.get_securitystatus2 import has_strong_security_headers
from features.get_catchingInfo_compressedinfo import check_caching_and_compression
import joblib
import pickle
import streamlit as st
import matplotlib.pyplot as plt

model = joblib.load('ocsvm_model.h5')
with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

def map_boolean(value):
    """Map True to 1, False to 0, and None to -1."""
    if value is True:
        return 1
    elif value is False:
        return 0
    else:
        return -1

def map_security_status(security_list):
    """Map list of security statuses to 1, 0, -1."""
    if isinstance(security_list, list):
        return [map_boolean(status) for status in security_list]
    return -1  # Handle unexpected cases

def main():
    st.title("URL Legitimacy Tracker")
    user_input = st.text_area("Enter the URL:")
    st.button("Enter", type="primary")

    if user_input:
        try:
            url = user_input
            domain_age = days_passed_since(get_domain_creation_date(get_root_domain(url)))
            page_rank = pagerank(get_domain(url))
            is_free = is_free_certificate(url)
            validation_period = get_validity_period(url)
            has_protective_status = has_protective_statuses(url)
            has_strong_security = has_strong_security_headers(url)  # should be list
            caching, compressed = check_caching_and_compression(url)

            # Create a DataFrame with the extracted features
            data = pd.DataFrame({
                'Domain Age': [domain_age],
                'Page Rank': [page_rank],
                'Is Free': [is_free],
                'Validation Period': [validation_period],
                'Has Protective Status': [has_protective_status],
                'Has Strong Security': [has_strong_security],  # list value
                'Caching': [caching],
                'Compressed': [compressed],
            })

            # Apply mapping to boolean features
            data['Is Free'] = data['Is Free'].apply(map_boolean)
            data['Has Protective Status'] = data['Has Protective Status'].apply(map_boolean)
            data['Caching'] = data['Caching'].apply(map_boolean)
            data['Compressed'] = data['Compressed'].apply(map_boolean)
            data['Has Strong Security'] = data['Has Strong Security'].apply(map_security_status)  # Apply mapping to each element in the list

            # Fill NaN values
            data.fillna(-1, inplace=True)  # Ensure any remaining NaNs are handled
            st.write(data)

            # Scale the data for prediction
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

# import pandas as pd
# from features.get_domain_age import get_root_domain,get_domain_creation_date,days_passed_since
# from features.get_page_rank import pagerank
# from features.get_CAstatus import is_free_certificate
# from features.get_domain_validity import get_validity_period
# from src.get_domain import get_domain
# from features.get_securitystatus import has_protective_statuses
# from features.get_securitystatus2 import has_strong_security_headers
# from features.get_catchingInfo_compressedinfo import check_caching_and_compression
#
# df = pd.read_csv("data/top-1m - Copy.csv")
#
# url = 'https://x.com/SimpleEnergyEV'
# domain_age = []
# page_rank = []
# is_free_list = []
# validation_period_list = []
# has_protective_status_list = []
# has_strong_security_list = []
# caching_list = []
# compressed_list = []
# text_list = []
# count = 0
#
#
# domain = get_root_domain(url)
# date_input = get_domain_creation_date(domain=domain)
# age = days_passed_since(date_input=date_input)
# domain_age.append(age)
#
# domain = get_domain(url)
# rank = pagerank(domain=domain)
# page_rank.append(rank)
#
# is_free = is_free_certificate(url)
# is_free_list.append(is_free)
#
# validation_period = get_validity_period(url)
# validation_period_list.append(validation_period)
#
# has_protective_status = has_protective_statuses(url)
# has_protective_status_list.append(has_protective_status)
#
# has_strong_security = has_strong_security_headers(url)
# has_strong_security_list.append(has_protective_status_list)
#
# caching,compressed = check_caching_and_compression(url)
# caching_list.append(caching)
# compressed_list.append(compressed)
#
# print("count is ----------->", count)
# print("urls is -->", url)
# print("age, pagerank-->", age, rank)
# print("Is free CA-->",is_free,validation_period,has_protective_status, has_strong_security, caching,compressed) #,text)
#
# data = {
#     "Url" : url,
#     'Domain Age': domain_age,
#     'Page Rank': page_rank,
#     'Is Free': is_free_list,
#     'Validation Period': validation_period_list,
#     'Has Protective Status': has_protective_status_list,
#     'Has Strong Security': has_strong_security_list,
#     'Caching': caching_list,
#     'Compressed': compressed_list,
# }
#
# # Creating a DataFrame
# df = pd.DataFrame(data)
# df.to_csv(f"temp3/data{count}.csv")
# count = count+1