import pandas as pd
from features.get_domain_age import get_root_domain,get_domain_creation_date,days_passed_since
from features.get_page_rank import pagerank
from features.get_CAstatus import is_free_certificate
from features.get_domain_validity import get_validity_period
from src.get_domain import get_domain
from features.get_securitystatus import has_protective_statuses
from features.get_securitystatus2 import has_strong_security_headers
from features.get_catchingInfo_compressedinfo import check_caching_and_compression

df = pd.read_csv("data/top-1m - Copy.csv")

url = []
domain_age = []
page_rank = []
is_free_list = []
validation_period_list = []
has_protective_status_list = []
has_strong_security_list = []
caching_list = []
compressed_list = []
text_list = []
count = 0
for i in df["url"]:
    url.append(i)

    domain = get_root_domain(url=i)
    date_input = get_domain_creation_date(domain=domain)
    age = days_passed_since(date_input=date_input)
    domain_age.append(age)

    domain = get_domain(url=i)
    rank = pagerank(domain=domain)
    page_rank.append(rank)

    is_free = is_free_certificate(url=i)
    is_free_list.append(is_free)

    validation_period = get_validity_period(url = i)
    validation_period_list.append(validation_period)

    has_protective_status = has_protective_statuses(url=i)
    has_protective_status_list.append(has_protective_status)

    has_strong_security = has_strong_security_headers(url=i)
    has_strong_security_list.append(has_protective_status_list)

    caching,compressed = check_caching_and_compression(url=i)
    caching_list.append(caching)
    compressed_list.append(compressed)
    # text = get_text_from_url(url=i)
    # text_list.append(text)
    print("count is ----------->", count)
    print("urls is -->", i)
    print("age, pagerank-->", age, rank)
    print("Is free CA-->",is_free,validation_period,has_protective_status, has_strong_security, caching,compressed) #,text)

    data = {
        "Url" : url,
        'Domain Age': domain_age,
        'Page Rank': page_rank,
        'Is Free': is_free_list,
        'Validation Period': validation_period_list,
        'Has Protective Status': has_protective_status_list,
        'Has Strong Security': has_strong_security_list,
        'Caching': caching_list,
        'Compressed': compressed_list,
        # 'Text': text_list
    }

    # Creating a DataFrame
    df = pd.DataFrame(data)
    df.to_csv(f"temp2/data{count}.csv")
    count = count+1