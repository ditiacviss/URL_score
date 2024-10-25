from src.ssl_certificate import get_ssl_certificate


def get_organization_name(certificate):
    # Navigate to the issuer's information
    issuer_info = certificate['issuer']

    for item in issuer_info:
        for sub_item in item:
            if sub_item[0] == 'organizationName':
                return sub_item[1]
    return None

def is_free_certificate(url):
    try:
        # Expanded list of free Certificate Authorities
        free_cas = [
            "Let's Encrypt",
            "ZeroSSL",
            "Buypass",
            "SSL.com",
            "Actalis",
            "Cloudflare",
            "BuyPass",
            "StartCom",
            "WoSign",
            "Google Trust Services",
            "Amazon",
            "CAcert",
            "FreeSSL",
            "DigiCert (Free Trials)",
            "Certum",
            "SubCA",
            "Trustico",
            "ACME Certificate Authorities",
            "FreeSSL/TLS Certificates by Cloudflare",
            "Mozilla CA Certificate Program",
            "Comodo (Free Trials)",
            "SSL Mate",
            "R3",
            "Let’s Encrypt Staging",
            "Sectigo (Free Trials)",
            "Node.js Foundation",
            "GoDaddy (Free Trials)",
            "PositiveSSL (Free Trials)",
            "ComodoCA (Free Trials)"
        ]
        certificate = get_ssl_certificate(url=url)
        issuer = get_organization_name(certificate=certificate)
        # Check if the issuer's organization name is in the free CA list
        for ca in free_cas:
            if ca in issuer:
                return True
        return False
    except:
        return None





