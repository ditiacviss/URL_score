import re
import socket
from datetime import datetime, date
import tldextract
import pandas as pd

### https://www.whatsmydns.net/api/domain?q=santorini-view.com
# Please contact api@whatsmydns.net for commercial or high volume use. API is in beta and may change at any time.
# This is giving domain_age most of the urls (even to some urls which this script got as -1)
"""
value is -1 is not able to find details
"""

WHOIS_PORT = 43
WHOIS_RESPONSE_LEN_LIMIT = 10000
WHOIS_PORTION_SIZE = 100

#WHO_IS SERVERS
SERVERS = {
    "ac": "whois.nic.ac",
    "ad": "whois.ripe.net",
    "ae": "whois.aeda.net.ae",
    "aero": "whois.aero",
    "af": "whois.nic.af",
    "ag": "whois.nic.ag",
    "ai": "whois.ai",
    "al": "whois.ripe.net",
    "am": "whois.amnic.net",
    "as": "whois.nic.as",
    "asia": "whois.nic.asia",
    "at": "whois.nic.at",
    "au": "whois.aunic.net",
    "aw": "whois.nic.aw",
    "ax": "whois.ax",
    "az": "whois.ripe.net",
    "ba": "whois.ripe.net",
    "bar": "whois.nic.bar",
    "be": "whois.dns.be",
    "berlin": "whois.nic.berlin",
    "best": "whois.nic.best",
    "bg": "whois.register.bg",
    "bi": "whois.nic.bi",
    "biz": "whois.neulevel.biz",
    "bj": "www.nic.bj",
    "bo": "whois.nic.bo",
    "br": "whois.nic.br",
    "br.com": "whois.centralnic.com",
    "bt": "whois.netnames.net",
    "bw": "whois.nic.net.bw",
    "by": "whois.cctld.by",
    "bz": "whois.belizenic.bz",
    "bzh": "whois-bzh.nic.fr",
    "ca": "whois.cira.ca",
    "cat": "whois.cat",
    "cc": "whois.nic.cc",
    "cd": "whois.nic.cd",
    "ceo": "whois.nic.ceo",
    "cf": "whois.dot.cf",
    "ch": "whois.nic.ch",
    "ci": "whois.nic.ci",
    "ck": "whois.nic.ck",
    "cl": "whois.nic.cl",
    "cloud": "whois.nic.cloud",
    "club": "whois.nic.club",
    "cn": "whois.cnnic.net.cn",
    "cn.com": "whois.centralnic.com",
    "co": "whois.nic.co",
    "co.nl": "whois.co.nl",
    "com": "whois.verisign-grs.com",
    "coop": "whois.nic.coop",
    "cx": "whois.nic.cx",
    "cy": "whois.ripe.net",
    "cz": "whois.nic.cz",
    "de": "whois.denic.de",
    "dk": "whois.dk-hostmaster.dk",
    "dm": "whois.nic.cx",
    "dz": "whois.nic.dz",
    "ec": "whois.nic.ec",
    "edu": "whois.educause.edu",
    "ee": "whois.tld.ee",
    "eg": "whois.ripe.net",
    "es": "whois.nic.es",
    "eu": "whois.eu",
    "eu.com": "whois.centralnic.com",
    "eus": "whois.nic.eus",
    "fi": "whois.fi",
    "fo": "whois.nic.fo",
    "fr": "whois.nic.fr",
    "gb": "whois.ripe.net",
    "gb.com": "whois.centralnic.com",
    "gb.net": "whois.centralnic.com",
    "qc.com": "whois.centralnic.com",
    "ge": "whois.ripe.net",
    "gg": "whois.gg",
    "gi": "whois2.afilias-grs.net",
    "gl": "whois.nic.gl",
    "gm": "whois.ripe.net",
    "gov": "whois.nic.gov",
    "gr": "whois.ripe.net",
    "gs": "whois.nic.gs",
    "gy": "whois.registry.gy",
    "hamburg": "whois.nic.hamburg",
    "hiphop": "whois.uniregistry.net",
    "hk": "whois.hknic.net.hk",
    "hm": "whois.registry.hm",
    "hn": "whois2.afilias-grs.net",
    "host": "whois.nic.host",
    "hr": "whois.dns.hr",
    "ht": "whois.nic.ht",
    "hu": "whois.nic.hu",
    "hu.com": "whois.centralnic.com",
    "id": "whois.pandi.or.id",
    "ie": "whois.domainregistry.ie",
    "il": "whois.isoc.org.il",
    "im": "whois.nic.im",
    "in": "whois.inregistry.net",
    "info": "whois.afilias.info",
    "ing": "domain-registry-whois.l.google.com",
    "ink": "whois.centralnic.com",
    "int": "whois.isi.edu",
    "io": "whois.nic.io",
    "iq": "whois.cmc.iq",
    "ir": "whois.nic.ir",
    "is": "whois.isnic.is",
    "it": "whois.nic.it",
    "je": "whois.je",
    "jobs": "jobswhois.verisign-grs.com",
    "jp": "whois.jprs.jp",
    "ke": "whois.kenic.or.ke",
    "kg": "whois.domain.kg",
    "ki": "whois.nic.ki",
    "kr": "whois.kr",
    "kz": "whois.nic.kz",
    "la": "whois2.afilias-grs.net",
    "li": "whois.nic.li",
    "london": "whois.nic.london",
    "lt": "whois.domreg.lt",
    "lu": "whois.restena.lu",
    "lv": "whois.nic.lv",
    "ly": "whois.lydomains.com",
    "ma": "whois.iam.net.ma",
    "mc": "whois.ripe.net",
    "md": "whois.nic.md",
    "me": "whois.nic.me",
    "mg": "whois.nic.mg",
    "mil": "whois.nic.mil",
    "mk": "whois.ripe.net",
    "ml": "whois.dot.ml",
    "mo": "whois.monic.mo",
    "mobi": "whois.dotmobiregistry.net",
    "ms": "whois.nic.ms",
    "mt": "whois.ripe.net",
    "mu": "whois.nic.mu",
    "museum": "whois.museum",
    "mx": "whois.nic.mx",
    "my": "whois.mynic.net.my",
    "mz": "whois.nic.mz",
    "na": "whois.na-nic.com.na",
    "name": "whois.nic.name",
    "nc": "whois.nc",
    "net": "whois.verisign-grs.com",
    "nf": "whois.nic.cx",
    "ng": "whois.nic.net.ng",
    "nl": "whois.domain-registry.nl",
    "no": "whois.norid.no",
    "no.com": "whois.centralnic.com",
    "nu": "whois.nic.nu",
    "nz": "whois.srs.net.nz",
    "om": "whois.registry.om",
    "ong": "whois.publicinterestregistry.net",
    "ooo": "whois.nic.ooo",
    "org": "whois.pir.org",
    "paris": "whois-paris.nic.fr",
    "pe": "kero.yachay.pe",
    "pf": "whois.registry.pf",
    "pics": "whois.uniregistry.net",
    "pl": "whois.dns.pl",
    "pm": "whois.nic.pm",
    "pr": "whois.nic.pr",
    "press": "whois.nic.press",
    "pro": "whois.registrypro.pro",
    "pt": "whois.dns.pt",
    "pub": "whois.unitedtld.com",
    "pw": "whois.nic.pw",
    "qa": "whois.registry.qa",
    "re": "whois.nic.re",
    "ro": "whois.rotld.ro",
    "rs": "whois.rnids.rs",
    "ru": "whois.tcinet.ru",
    "sa": "saudinic.net.sa",
    "sa.com": "whois.centralnic.com",
    "sb": "whois.nic.net.sb",
    "sc": "whois2.afilias-grs.net",
    "se": "whois.nic-se.se",
    "se.com": "whois.centralnic.com",
    "se.net": "whois.centralnic.com",
    "sg": "whois.nic.net.sg",
    "sh": "whois.nic.sh",
    "si": "whois.arnes.si",
    "sk": "whois.sk-nic.sk",
    "sm": "whois.nic.sm",
    "st": "whois.nic.st",
    "so": "whois.nic.so",
    "su": "whois.tcinet.ru",
    "sx": "whois.sx",
    "sy": "whois.tld.sy",
    "tc": "whois.adamsnames.tc",
    "tel": "whois.nic.tel",
    "tf": "whois.nic.tf",
    "th": "whois.thnic.net",
    "tj": "whois.nic.tj",
    "tk": "whois.nic.tk",
    "tl": "whois.domains.tl",
    "tm": "whois.nic.tm",
    "tn": "whois.ati.tn",
    "to": "whois.tonic.to",
    "top": "whois.nic.top",
    "tp": "whois.domains.tl",
    "tr": "whois.nic.tr",
    "travel": "whois.nic.travel",
    "tw": "whois.twnic.net.tw",
    "tv": "whois.nic.tv",
    "tz": "whois.tznic.or.tz",
    "ua": "whois.ua",
    "ug": "whois.co.ug",
    "uk": "whois.nic.uk",
    "uk.com": "whois.centralnic.com",
    "uk.net": "whois.centralnic.com",
    "ac.uk": "whois.ja.net",
    "gov.uk": "whois.ja.net",
    "us": "whois.nic.us",
    "us.com": "whois.centralnic.com",
    "uy": "nic.uy",
    "uy.com": "whois.centralnic.com",
    "uz": "whois.cctld.uz",
    "va": "whois.ripe.net",
    "vc": "whois2.afilias-grs.net",
    "ve": "whois.nic.ve",
    "vg": "ccwhois.ksregistry.net",
    "vu": "vunic.vu",
    "wang": "whois.nic.wang",
    "wf": "whois.nic.wf",
    "wiki": "whois.nic.wiki",
    "ws": "whois.website.ws",
    "xxx": "whois.nic.xxx",
    "xyz": "whois.nic.xyz",
    "yu": "whois.ripe.net",
    "za.com": "whois.centralnic.com"
}

SERVER_NOT_FOUND = "Server_not_found"
CREATION_DATE_NOT_FOUND = "Creation_date_not_found"


# Performing a WHOIS lookup for a given domain by connecting to the appropriate WHOIS server and retrieving the WHOIS information
def query_whois(domain):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server = fetch_server(domain)
        if not server:
            return SERVER_NOT_FOUND
        sock.connect((server, WHOIS_PORT))
        sock.send((domain + "\r\n").encode('utf-8'))
        whois_response = ''
        while len(whois_response) < WHOIS_RESPONSE_LEN_LIMIT:
            response_portion = sock.recv(WHOIS_PORTION_SIZE).decode('utf-8')
            if response_portion == '':
                break
            whois_response += response_portion
        sock.close()
    except:
        return SERVER_NOT_FOUND
    return whois_response


# Selecting appropriate WHOIS server for a given domain based on its top-level domain (TLD)
def fetch_server(domain):
    domain_extension = domain.split(".")[-1]
    if domain_extension in SERVERS:
        return SERVERS[domain_extension]
    else:
        return None


MONTHS = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7,
          "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}

#Format dates to a single structure
def parse_date(date):
    pattern = "Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec"
    res = re.search(pattern, date, re.I)
    if res:  # 14 Apr 2018
        day = int(date[0:2])
        month = MONTHS[date[res.start():res.start() + 3]]
        year = int(date[res.end() + 1: res.end() + 5])
    elif '/' in date and date[2] == '/':  # DD/MM/YYY
        day = int(date[0:2])
        month = int(date[3:5])
        year = int(date[6:10])
    elif '/' in date:  # YYYY/MM/DD
        year = int(date[0:4])
        month = int(date[5:7])
        day = int(date[8:10])
    elif '-' in date and date[2] == '-':  # DD-MM-YYYY
        day = int(date[0:2])
        month = int(date[3:5])
        year = int(date[6:10])
    elif '-' in date:  # YYYY-MM-DD
        year = int(date[0:4])
        month = int(date[5:7])
        day = int(date[8:10])
    elif '.' in date and date[2] == '.':  # DD.MM.YYYY
        day = int(date[0:2])
        month = int(date[3:5])
        year = int(date[6:10])
    elif '.' in date:  # YYYY.MM.DD
        year = int(date[0:4])
        month = int(date[5:7])
        day = int(date[8:10])
    else:  # YYYYMMDD
        year = int(date[0:4])
        month = int(date[4:6])
        day = int(date[6:8])
    date = datetime(year, month, day)
    return date.date()

# Extract the creation date of a domain from the WHOIS information
def get_domain_creation_date(domain):
    try:
        whois_response = query_whois(domain)
        if whois_response == SERVER_NOT_FOUND:
            return CREATION_DATE_NOT_FOUND
        pattern = r"Creation Date|created|Created On|Creation date|Created|Domain Name Commencement Date|登録年月日|Registration Time|Registered on|registered"
        res = re.search(pattern, whois_response)
        if not res:
            return CREATION_DATE_NOT_FOUND
        creation_date_start = res.start()
        creation_date = whois_response[creation_date_start:creation_date_start + 50]
        date = re.search(r'\d', creation_date)
        if not date:
            return CREATION_DATE_NOT_FOUND
        start_index = date.start()
        date = creation_date[start_index:]
        return parse_date(date)
    except:
        return CREATION_DATE_NOT_FOUND


# print(get_domain_creation_date("amazon.in"))

#Caluculating the difference from start date
def days_passed_since(date_input):
    if isinstance(date_input, date):
        parsed_date = date_input
    else:
        try:
            parsed_date = datetime.strptime(date_input, "%Y-%m-%d").date()
        except ValueError:
            return -1

    current_date = datetime.now().date()
    difference = current_date - parsed_date
    days_passed = difference.days

    return days_passed


# # Example usage:
# date_str = datetime.now().date()
# days_passed = days_passed_since(get_domain_creation_date("amazon.com"))
# print("Number of days passed since", date_str, ":", days_passed)

#Getting root domain from url
def get_root_domain(url):
    try:
        extracted = tldextract.extract(url)
        root_domain = "{}.{}".format(extracted.domain, extracted.suffix)
        return root_domain
    except:
        return -1

#Updating the existing csv
# df = pd.read_csv('legitimate_500.csv')
# df['root_domain'] = df['urls'].apply(get_root_domain)
# df['domain_age'] = df['root_domain'].apply(lambda domain: days_passed_since(get_domain_creation_date(domain)))
# df.to_csv('legitimate_500.csv', index=False)

