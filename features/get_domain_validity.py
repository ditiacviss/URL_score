from datetime import datetime
from src.ssl_certificate import get_ssl_certificate

def get_validity_period(url):
    try:
        certificate = get_ssl_certificate(url=url)
        not_before = certificate.get('notBefore')
        not_after = certificate.get('notAfter')

        # Convert string dates to datetime objects
        not_before_date = datetime.strptime(not_before, '%b %d %H:%M:%S %Y %Z')
        not_after_date = datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')

        # Calculate the difference in days
        validity_days = (not_after_date - not_before_date).days
        return validity_days
    except:
        return None

