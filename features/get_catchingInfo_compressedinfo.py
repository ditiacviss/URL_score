
import requests

def check_caching_and_compression(url):
    # Expanded list of caching and related headers to check
    caching_headers = [
        'Cache-Control',
        'Expires',
        'Last-Modified',
        'ETag',
        'Content-Encoding',
        'Pragma',
        'Vary',
        'Age',
        'Surrogate-Control',
        'Content-Disposition',
        'If-Modified-Since',
        'If-None-Match',
        'Accept-Encoding',
        'X-Cache',
        'X-Content-Type-Options',
        'X-Frame-Options',
        'X-XSS-Protection',
    ]

    try:
        response = requests.get(url)
        headers = response.headers

        # Check for the presence of caching headers
        caching_info_present = any(header in headers for header in caching_headers)

        # Determine if content is compressed
        is_compressed = 'Content-Encoding' in headers

        return caching_info_present, is_compressed

    except Exception as e:
        print(f"Error: {e}")
        return False, False