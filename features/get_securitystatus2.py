import requests

def has_strong_security_headers(url):
    # Expanded list of strong security headers to check
    security_headers = [
        'Strict-Transport-Security',
        'X-Frame-Options',
        'X-Content-Type-Options',
        'X-XSS-Protection',
        'Content-Security-Policy',
        'Referrer-Policy',
        'Feature-Policy',
        'Permissions-Policy',
        'Access-Control-Allow-Origin',
        'Access-Control-Allow-Methods',
        'Access-Control-Allow-Headers',
        'Content-Disposition',
        'X-Content-Security-Policy',
        'X-WebKit-CSP',
        'Public-Key-Pins',
        'Expect-CT',
        'Cross-Origin-Embedder-Policy',
        'Cross-Origin-Opener-Policy',
        'Cross-Origin-Resource-Policy',
    ]

    try:
        response = requests.get(url)
        headers = response.headers

        # Check for the presence of at least one security header
        return any(header in headers for header in security_headers)

    except Exception as e:
        print(f"Error: {e}")
        return "ERROR"
