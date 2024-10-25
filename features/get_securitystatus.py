import whois
from src.get_domain import get_domain
def has_protective_statuses(url):
    try:
        domain = get_domain(url=url)  # Extract the domain from the URL
        whois_info = whois.whois(domain)

        # Check for protective statuses
        protective_statuses = [
            'clientDeleteProhibited',
            'clientRenewProhibited',
            'clientTransferProhibited',
            'clientUpdateProhibited',
            'clientHold',
            'clientPendingDelete',
            'clientTransferProhibited',
            'clientUpdateProhibited',
            'clientRevokeProhibited',
            'clientRenewProhibited',
            'clientDeleteProhibited',
            'clientTransferProhibited',
            'serverTransferProhibited',
            'serverUpdateProhibited',
            'serverDeleteProhibited',
            'serverRenewProhibited',
            'serverHold'
        ]
        status_keywords = [status.split()[0] for status in whois_info.status]
        return bool(set(protective_statuses) & set(status_keywords))
    except:
        return None
