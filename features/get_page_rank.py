import requests
import yaml


def pagerank(domain):
    try:
        endpoint = "https://openpagerank.com/api/v1.0/getPageRank"
        with open("keys.yaml", 'r') as file:
            data = yaml.safe_load(file)
            api_key = (data["api_key_page_rank"])
        headers = {
            "API-OPR": api_key
        }
        params = {
            "domains[]": domain
        }

        response = requests.get(endpoint, headers=headers, params=params)
        print(api_key)
        if response.status_code == 200:
            data = response.json()
            print(data)
            print(data["response"][0])
            return data['response'][0]['page_rank_integer']
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return f"Error: {response.status_code}, {response.text}"

    except:
        return -1


