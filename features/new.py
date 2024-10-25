from bs4 import BeautifulSoup
import requests

def get_meta_tags(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        meta_tags = soup.find_all('meta')
        return {tag.get('name'): tag.get('content') for tag in meta_tags if tag.get('name')}
    except:
        return None

domain = "https://amazon.com"
meta_tags = get_meta_tags(domain)
print(f"The meta tags for {domain} is {meta_tags}")


from bs4 import BeautifulSoup
import requests
def get_content_ratio(url):
    try:
        response = requests.get(url)
        content_length = len(response.text)
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text()
        visible_content_length = len(text)
        return visible_content_length / content_length if content_length > 0 else 0
    except:
        return None

domain = "https://www.bikedekho.com/showrooms/simple-energy/bangalore"
meta_tags = get_content_ratio(domain)
print(f"The content ratio for {domain} is {meta_tags}")

import requests
# X-Frame-Options - SAMEORIGIN/DENY, None means allows  header is only useful when the HTTP response where it is included has something to interact with (e.g. links, buttons).
# If the HTTP response is a redirect or an API returning JSON data, X-Frame-Options does not provide any security.
def get_security_headers(url):
    try:
        response = requests.get(url)
        headers = response.headers
        return {
            'X-Frame-Options': headers.get('X-Frame-Options', 'None'),
            'Strict-Transport-Security': headers.get('Strict-Transport-Security', 'None'),
            'X-DNS-Prefetch-Control': headers.get('X-DNS-Prefetch-Control', 'None'),
            'Cross-Origin-Embedder-Policy': headers.get('Cross-Origin-Embedder-Policy', 'None'),
            'Cross-Origin-Opener-Policy': headers.get('Cross-Origin-Opener-PolicyNone', 'None'),
            'Referrer-Policy': headers.get('Referrer-Policy', 'None'),
            'X-Content-Type-Options': headers.get('X-Content-Type-Options', 'None'),
            'Content-Security-Policy': headers.get('Content-Security-Policy', 'None'),
            'X-XSS-Protection': headers.get('X-XSS-Protection', 'None'),
            'X-Powered-By': headers.get('X-Powered-By', 'None'),
            'Set-Cookie': headers.get('Set-Cookie', 'None'),
            'Content-Type': headers.get('Content-Type', 'None')
        }
    except requests.exceptions.RequestException:
        return None

# domain = 'https://Mozilla.org'
domain = 'https://google.com'
meta_tags = get_security_headers(domain)
print(f"The security headers for {domain} is {meta_tags}")

# from googleapiclient.discovery import build
#
# def get_google_safety_status(api_key, url):
#     service = build('safebrowsing', 'v4', developerKey=api_key)
#     threat_match = service.threatMatches().find(body={
#         'client': {
#             'clientId': "yourcompany",
#             'clientVersion': "1.5.2"
#         },
#         'threatInfo': {
#             'threatTypes': ["MALWARE", "SOCIAL_ENGINEERING"],
#             'platformTypes': ["ANY_PLATFORM"],
#             'threatEntryTypes': ["URL"],
#             'threatEntries': [
#                 {'url': url}
#             ]
#         }
#     }).execute()
#     return threat_match
#
# api_key=''
# domain = "https://www.bikedekho.com/showrooms/simple-energy/bangalore"
# meta_tags = get_google_safety_status(api_key,domain)
# print(f"The content ratio for {domain} is {meta_tags}")