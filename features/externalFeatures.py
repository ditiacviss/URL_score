from logger.loging import logs
import string
from src.wordsDetails import words_raw_extraction
from src.domainDetails import get_domain_subdomain_path
from src.brands import brands
import re
import socket
import nltk
from nltk.corpus import words
from urllib.parse import urlparse
import pickle



import re
class Features():
    def __init__(self, string):
        self.string = string
        self.protocol, self.domain, self.subdomain, self.tld, self.path, self.Hostname = get_domain_subdomain_path(url = string)
        self.words_raw, self.words_raw_host, self.words_raw_path = words_raw_extraction(domain=self.domain, subdomain=self.subdomain, path=self.path)
        self.brands = brands
        # Load the list of words from the file
        with open('features/words_list.pkl', 'rb') as f:
            word_list = pickle.load(f)
        self.word_list = word_list

    def input_length(self):
        try:
            return len(self.string)
        except Exception as e:

            logs.error(message=f"in input_length function in features/externalFeatures.py-->{str(e)}, (0 means yes 1 means no)")
            return "error"



    def having_ip_address(self):
        try:
            match = re.search(
                '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
                '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
                '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)|'  # IPv4 in hexadecimal
                '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}|'
                '[0-9a-fA-F]{7}', self.string)  # Ipv6
            if match:
                return 0
            else:
                return 1
        except Exception as e:
            logs.error(message=f"in having_ip_address function in features/externalFeatures.py-->{str(e)}, url is {self.string}")
            return "error"



    def count_special_characters(self):
        try:
            special_characters_mapping = {
                '!': 'no_of_exclamationmark',
                '"': 'no_of_doublequote',
                '#': 'no_of_hash',
                '$': 'no_of_dollar',
                '%': 'no_of_percent',
                '&': 'no_of_ampersand',
                "'": 'no_of_apostrophe',
                '(': 'no_of_leftparenthesis',
                ')': 'no_of_rightparenthesis',
                '*': 'no_of_asterisk',
                '+': 'no_of_plus',
                ',': 'no_of_comma',
                '-': 'no_of_hyphen',
                '.': 'no_of_period',
                '/': 'no_of_slash',
                ':': 'no_of_colon',
                ';': 'no_of_semicolon',
                '<': 'no_of_lessthan',
                '=': 'no_of_equal',
                '>': 'no_of_greaterthan',
                '?': 'no_of_questionmark',
                '@': 'no_of_at',
                '[': 'no_of_leftbracket',
                '\\': 'no_of_double_backslash',
                '\'': 'no_of_backslash',
                ']': 'no_of_rightbracket',
                '^': 'no_of_caret',
                '_': 'no_of_underscore',
                '`': 'no_of_backtick',
                '{': 'no_of_leftbrace',
                '|': 'no_of_pipe',
                '}': 'no_of_rightbrace',
                '~': 'no_of_tilde',
                " ": "space"}
            special_counts = {char: 0 for char in special_characters_mapping.values()}  # Initialize counts to 0

            for char in self.string:
                if char in string.punctuation:
                    descriptive_name = special_characters_mapping.get(char, 'unknown')
                    special_counts[descriptive_name] += 1

            return special_counts
        except Exception as e:

            logs.error(message=f"in count_special_characters function in features/externalFeatures.py-->{str(e)}, url is {self.string}")
            return "error"


    def check_www(self):
        try:
            count = 0
            for word in self.words_raw:
                if not word.find('www') == -1:
                    count += 1
            return count
        except Exception as e:
            logs.error(message=f"in check_www function in features/externalFeatures.py-->{str(e)},url is {self.string}, input is {self.words_raw}")
            return "error"

    def check_com(self):
        try:
            count = 0
            for word in self.words_raw:
                if not word.find('com') == -1:
                    count += 1
            return count
        except Exception as e:
            logs.error(message=f"in check_com function in features/externalFeatures.py-->{str(e)},url is {self.string}, input is {self.words_raw}")
            return "error"

    def count_http_url(self):
        try:
            return self.string.count('http')
        except Exception as e:
            logs.error(message=f"in count_http_url function in features/externalFeatures.py-->{str(e)},url is {self.string}")
            return "error"

    def https_token(self):
        try:
            if self.protocol == 'https':
                return 0
            return 1
        except Exception as e:
            logs.error(message=f"in https_token function in features/externalFeatures.py-->{str(e)},url is {self.string}, input is {self.protocol}")
            return "error"

    def ratio_digits_url(self):
        try:
            return len(re.sub("[^0-9]", "", self.string)) / len(self.string)
        except Exception as e:
            logs.error(message=f"in ratio_digits_url function in features/externalFeatures.py-->{str(e)}, url is {self.string}")
            return "error"
    def ratio_digits_hostname(self):
        try:
            return len(re.sub("[^0-9]", "", self.Hostname)) / len(self.Hostname)
        except Exception as e:
            logs.error(message=f"in ratio_digits_hostname function in features/externalFeatures.py-->{str(e)},url is {self.string}, input is {self.Hostname}")
            return "error"

    # def punycode(self):
    #     try:
    #         if self.string.startswith("http://xn--") or self.string.startswith("https://xn--"):
    #             return 0
    #         else:
    #             return 1
    #     except Exception as e:
    #         logs.error(message=f"in punycode function in features/externalFeatures.py-->{str(e)}, input is {self.string}")
    #         return "error"

    def port(self):
        try:
            if re.search(r"^[a-z][a-z0-9+\-.]*://([a-z0-9\-._~%!$&'()*+,;=]+@)?([a-z0-9\-._~%]+|\[[a-z0-9\-._~%!$&'()*+,;=:]+\]):([0-9]+)", self.string):
                return 0
            return 1
        except Exception as e:
            logs.error(message=f"in port function in features/externalFeatures.py-->{str(e)}, input is {self.string}")
            return "error"

    def tld_in_path(self):
        try:

            if self.path.lower().count(self.tld) > 0:
                return 0
            return 1
        except Exception as e:
            logs.error(message=f"in tld_in_path function in features/externalFeatures.py-->{str(e)},url is {self.string}, input is {self.path} and {self.tld}")
            return "error"

    def tld_in_subdomain(self):
        try:
            if self.subdomain.count(self.tld) > 0:
                return 0
            return 1
        except Exception as e:
            logs.error(message=f"in tld_in_subdomain function in features/externalFeatures.py-->{str(e)}, url is {self.string}, input is {self.tld}")
            return "error"

    def abnormal_subdomain(self):
        try:
            if re.search('(http[s]?://(w[w]?|\d))([w]?(\d|-))', self.string):
                return 0
            return 1
        except Exception as e:
            logs.error(message=f"in abnormal_subdomain function in features/externalFeatures.py-->{str(e)}, input is {self.string}")
            return "error"

    def count_subdomain(self):
        try:
            if len(re.findall("\.", self.string)) == 1:
                return 1
            elif len(re.findall("\.", self.string)) == 2:
                return 2
            else:
                return 3

        except Exception as e:
            logs.error(message=f"in count_subdomain function in features/externalFeatures.py-->{str(e)}, input is {self.string}")
            return "error"

    def prefix_suffix(self):
        try:
            if re.findall(r"https?://[^\-]+-[^\-]+/", self.string):
                return 0
            else:
                return 1

        except Exception as e:
            logs.error(message=f"in prefix_suffix function in features/externalFeatures.py-->{str(e)}, input is {self.string}")
            return "error"



    def is_random_domain(self):
        try:

            # Check if the domain is too short or too long
            if len(self.domain) < 5 or len(self.domain) > 20:
                return 0

            # Check if the domain contains non-alphanumeric characters
            if not re.match("^[a-zA-Z0-9.-]+$", self.domain):
                return 0

            # Check if the domain consists mostly of numbers
            if len(re.findall("[0-9]", self.domain)) / len(self.domain) > 0.5:
                return 0

            # Check if the domain starts with "www"
            if self.domain.startswith("www"):
                return 0

            # Check if the domain is an IP address
            if re.match("^(\d{1,3}\.){3}\d{1,3}$", self.domain):
                return 0

            # Check if the domain contains only one character repeated multiple times
            if len(set(self.domain)) == 1:
                return 0

            # Check if the domain contains a suspiciously high number of hyphens
            if self.domain.count("-") > len(self.domain) / 4:
                return 0

            # Check if the domain contains a suspiciously high number of consecutive characters
            if max([len(s) for s in re.findall(r"([a-zA-Z0-9.])\1*", self.domain)]) > len(self.domain) / 3:
                return 0

            # If none of the above conditions are met, the domain is considered random
            return 1
        except Exception as e:
            logs.error(
                message=f"in is_random_domain function in features/externalFeatures.py-->{str(e)}, input is {self.domain}, url is {self.string}")
            return "error"

    def shortening_service(self):
        try:
            match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                              'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                              'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                              'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                              'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                              'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                              'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|'
                              'tr\.im|link\.zip\.net',
                              self.string)
            if match:
                return 0
            else:
                return 1
        except Exception as e:
            logs.error(
                message=f"in shortening_service function in features/externalFeatures.py-->{str(e)}, input is {self.string}")
            return "error"

    def path_extension(self):
        try:
            # List of unnatural path extensions to check for
            unnatural_extensions = ['.txt', '.php', '.exe', '.bat', '.cmd', '.jar', '.py']

            # Check if the URL path ends with any of the unnatural extensions
            for extension in unnatural_extensions:
                if self.string.endswith(extension):
                    return 0

            # If none of the unnatural extensions are found, return 1
            return 1
        except Exception as e:
            logs.error(
                message=f"in path_extension function in features/externalFeatures.py-->{str(e)}, input is {self.string}")
            return "error"

    def length_word_raw(self):
        try:
            return len(self.words_raw)
        except Exception as e:
            logs.error(
                message=f"in length_word_raw function in features/externalFeatures.py-->{str(e)}, url is {self.string}, input is {self.words_raw}")
            return "error"

    def count_repeated_words(self):
        try:
            word_count = {}
            repeated_count = 0

            # Count occurrences of each word
            for word in self.words_raw:
                if word in word_count:
                    word_count[word] += 1
                    if word_count[word] == 2:
                        repeated_count += 1
                else:
                    word_count[word] = 1

            return repeated_count
        except Exception as e:
            logs.error(
                message=f"in count_repeated_words function in features/externalFeatures.py-->{str(e)}, url is {self.string}, input is {self.words_raw}")
            return "error"

    def shortest_length(self, input):
        try:
            if len(input) == 0:
                return 0
            return min(len(word) for word in input)
        except Exception as e:
            logs.error(
                message=f"in shortest_length function in features/externalFeatures.py-->{str(e)}, url is {self.string}, input is {input}")
            return "error"

    def average_word_length(self, input):
        try:
            if len(input) == 0:
                return 0
            return sum(len(word) for word in input) / len(input)
        except Exception as e:
            logs.error(
                message=f"in average_word_length function in features/externalFeatures.py-->{str(e)}, url is {self.string}, input is {input}")
            return "error"


    def longest_word_length(self, input):
        try:
            if len(input) == 0:
                return 0
            return max(len(word) for word in input)

        except Exception as e:
            logs.error(
                message=f"in longest_word_length function in features/externalFeatures.py-->{str(e)}, url is {self.string}, input is {input}")
            return "error"

    def phish_hints(self):
        try:
            HINTS = [
                'wp', 'login', 'includes', 'admin', 'content', 'site', 'images', 'js',
                'alibaba', 'css', 'myaccount', 'dropbox', 'themes', 'plugins', 'signin',
                'view', 'secure', 'update', 'verification', 'banking', 'account', 'confirm',
                'verification', 'paypal', 'ebay', 'apple', 'google', 'outlook', 'microsoft',
                'security', 'amazon', 'password', 'billing', 'invoice', 'facebook', 'twitter',
                'youtube', 'linkedin', 'support', 'service', 'helpdesk', 'email', 'client',
                'webscr', 'authentication', 'validate', 'transaction', 'verification'
            ]

            count = 0
            for hint in HINTS:
                count += self.string.lower().count(hint)
            return count
        except Exception as e:
            logs.error(
                message=f"in phish_hints function in features/externalFeatures.py-->{str(e)}, url is {self.string}")
            return "error"
    def brand_in_domain(self):
        try:

            domain_name = self.domain.split('.')[0].lower()
            if domain_name in self.brands:
                return 0
            else:
                return 1
        except Exception as e:
            logs.error(
                message=f"in brand_in_domain function in features/externalFeatures.py-->{str(e)}, url is {self.string}, input is {self.domain}")
            return "error"

    def brand_in_url(self):
        try:
            url_lower = self.string.lower()

            for brand in self.brands:
                if brand in url_lower:
                    return 0
            return 1
        except Exception as e:
            logs.error(
                message=f"in brand_in_url function in features/externalFeatures.py --> {str(e)}, url is {self.string}"
            )
            return "error"

    def brand_in_subdomain(self):
        try:
            subdomain = self.subdomain.lower()

            for brand in self.brands:
                if brand in subdomain:
                    return 0
            return 1
        except Exception as e:
            logs.error(
                message=f"in brand_in_subdomain function in features/externalFeatures.py --> {str(e)}, url is {self.string}"
            )
            return "error"

    def brand_in_path(self):
        try:
            path = self.path.lower()

            for brand in self.brands:
                if brand in path:
                    return 0
            return 1
        except Exception as e:
            logs.error(
                message=f"in brand_in_subdomain function in features/externalFeatures.py --> {str(e)}, url is {self.string}"
            )
            return "error"


    def suspicious_tld(self):
        try:
            suspicious_tld = ['fit', 'tk', 'gp', 'ga', 'work', 'ml', 'date', 'wang', 'men', 'icu', 'online', 'click',
                               # Spamhaus
                               'country', 'stream', 'download', 'xin', 'racing', 'jetzt',
                               'ren', 'mom', 'party', 'review', 'trade', 'accountants',
                               'science', 'work', 'ninja', 'xyz', 'faith', 'zip', 'cricket', 'win',
                               'accountant', 'realtor', 'top', 'christmas', 'gdn',  # Shady Top-Level Domains
                               'link',  # Blue Coat Systems
                               'asia', 'club', 'la', 'ae', 'exposed', 'pe', 'go.id', 'rs', 'k12.pa.us', 'or.kr',
                               'ce.ke', 'audio', 'gob.pe', 'gov.az', 'website', 'bj', 'mx', 'media', 'sa.gov.au'
                               # statistics
                               ]

            if self.tld in suspicious_tld:
                return 0
            return 1
        except Exception as e:
            logs.error(
                message=f"in suspicious_tld function in features/externalFeatures.py --> {str(e)}, url is {self.string}"
            )
            return "error"



    # def statistical_report(self):
    #     url_match = re.search(
    #         'at\.ua|usa\.cc|baltazarpresentes\.com\.br|pe\.hu|esy\.es|hol\.es|sweddy\.com|myjino\.ru|96\.lt|ow\.ly',
    #         self.string)
    #     try:
    #         ip_address = socket.gethostbyname(self.domain)
    #         ip_match = re.search(
    #             '146\.112\.61\.108|213\.174\.157\.151|121\.50\.168\.88|192\.185\.217\.116|78\.46\.211\.158|181\.174\.165\.13|46\.242\.145\.103|121\.50\.168\.40|83\.125\.22\.219|46\.242\.145\.98|'
    #             '107\.151\.148\.44|107\.151\.148\.107|64\.70\.19\.203|199\.184\.144\.27|107\.151\.148\.108|107\.151\.148\.109|119\.28\.52\.61|54\.83\.43\.69|52\.69\.166\.231|216\.58\.192\.225|'
    #             '118\.184\.25\.86|67\.208\.74\.71|23\.253\.126\.58|104\.239\.157\.210|175\.126\.123\.219|141\.8\.224\.221|10\.10\.10\.10|43\.229\.108\.32|103\.232\.215\.140|69\.172\.201\.153|'
    #             '216\.218\.185\.162|54\.225\.104\.146|103\.243\.24\.98|199\.59\.243\.120|31\.170\.160\.61|213\.19\.128\.77|62\.113\.226\.131|208\.100\.26\.234|195\.16\.127\.102|195\.16\.127\.157|'
    #             '34\.196\.13\.28|103\.224\.212\.222|172\.217\.4\.225|54\.72\.9\.51|192\.64\.147\.141|198\.200\.56\.183|23\.253\.164\.103|52\.48\.191\.26|52\.214\.197\.72|87\.98\.255\.18|209\.99\.17\.27|'
    #             '216\.38\.62\.18|104\.130\.124\.96|47\.89\.58\.141|78\.46\.211\.158|54\.86\.225\.156|54\.82\.156\.19|37\.157\.192\.102|204\.11\.56\.48|110\.34\.231\.42',
    #             ip_address)
    #         if url_match or ip_match:
    #             return 0
    #         else:
    #             return 1
    #     except Exception as e:
    #             logs.error(
    #                 message=f"in suspicious_tld function in features/externalFeatures.py --> {str(e)}, url is {self.string}, input is domain {self.domain}"
    #             )
    #             return "error"

    def getWordsFromURL(self):
        try:
            # nltk.download('words')
            # word_list = set(words.words())
            word_list = self.word_list
            parsed_url = urlparse(self.string)
            url_parts = parsed_url.hostname + parsed_url.path + parsed_url.query + parsed_url.fragment
            url_parts = url_parts.replace('.', ' ').replace('/', ' ').replace('?', ' ').replace('=', ' ').replace('&',
                                                                                                                  ' ') \
                .replace('-', ' ').replace(':', ' ').replace('~', ' ').replace('%', ' ').replace(',', ' ')
            tokens = url_parts.split()

            separated_tokens = []
            for token in tokens:
                separated_tokens.extend(re.findall(r'[A-Za-z]+|\d+', token))

            # Count the number of valid words in the tokens
            count = sum(1 for token in separated_tokens if token.lower() in word_list or token.isdigit())
            if count >= 1:
                return 1
            else:
                return 0
        except Exception as e:
                logs.error(
                    message=f"in getWordsFromURL function in features/externalFeatures.py --> {str(e)}, url is {self.string}"
                )
                return "error"
