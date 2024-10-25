import re
from urllib.parse import urlparse
from logger.loging import logs
import requests
from bs4 import BeautifulSoup
import whois
from src.wordsDetails import words_raw_extraction
from src.domainDetails import get_domain_subdomain_path
from src.getPageContent import URLDataExtractor
import time
import datetime
import dns.resolver
import ssl
import socket




class Features():
    def __init__(self, url):
        self.url = url
        protocol, self.domain, subdomain, tld, path, Hostname = get_domain_subdomain_path(url=url)
        words_raw, words_raw_host, words_raw_path = words_raw_extraction(domain=self.domain, subdomain=subdomain, path=path)
        extractor = URLDataExtractor(url)

        _, content = extractor.get_page_content()
        self.content = content
        self.extractor = extractor
        self.extractor.extract_data()

        self.Href = extractor.Href
        self.Link = extractor.Link
        self.Anchor = extractor.Anchor
        self.Media = extractor.Media
        self.Form = extractor.Form
        self.CSS = extractor.CSS
        self.Favicon = extractor.Favicon
        self.IFrame = extractor.IFrame
        self.Title = extractor.Title
        self.Text = extractor.Text

    def count_redirections(self):
        try:

            response = requests.get(self.url, allow_redirects=True)
            redirections = len(response.history)
            return redirections
        except Exception as e:
            logs.error(
                message=f"in count_redirections function in features/internalFeatures.py-->{str(e)}, input is {self.url})")
            return "error"

    def count_external_redirections(self):
        try:
            redirection_count = 0
            while True:
                response = requests.get(self.url, allow_redirects=False)
                if response.status_code // 100 == 3:  # Check if it's a redirect response
                    redirection_count += 1
                    location = response.headers['Location']
                    parsed_location = urlparse(location)
                    if parsed_location.netloc != '' and parsed_location.netloc != urlparse(self.url).netloc:
                        print(f"Redirected to: {location}")
                else:
                    break
                self.url = location  # Update the URL to follow the redirection
            return redirection_count
        except Exception as e:
            logs.error(
                message=f"in count_external_redirections function in features/internalFeatures.py-->{str(e)}, input is {self.url})")
            return "error"



    def count_hyperlinks(self):
        try:
            # Fetch the content of the URL
            response = requests.get(self.url)
            response.raise_for_status()  # Raise an error for bad status codes

            soup = BeautifulSoup(response.content, 'html.parser')
            hyperlinks = soup.find_all('a')
            return len(hyperlinks)

        except Exception as e:
            logs.error(
                message=f"in count_hyperlinks function in features/internalFeatures.py-->{str(e)}, input is {self.url})")
            return "error"

    def _nb_hyperlinks(self):
        if self.Form is None:
            return None
        return len(self.Href['internals']) + len(self.Href['externals']) + \
            len(self.Link['internals']) + len(self.Link['externals']) + \
            len(self.Media['internals']) + len(self.Media['externals']) + \
            len(self.Form['internals']) + len(self.Form['externals']) + \
            len(self.CSS['internals']) + len(self.CSS['externals']) + \
            len(self.Favicon['internals']) + len(self.Favicon['externals'])
    def _h_total(self):
        if self.Form is None:
            return None
        return self._nb_hyperlinks()# (self.Href, self.Link, self.Media, self.Form, self.CSS, self.Favicon)

    def _h_internal(self):
        if self.Form is None:
            return None
        return len(self.Href['internals']) + len(self.Link['internals']) + len(self.Media['internals']) + \
            len(self.Form['internals']) + len(self.CSS['internals']) + len(self.Favicon['internals'])

    def internal_hyperlinks_ratio(self):
        try:
            if self.Form is None:
                return None
            total = self._h_total()
            if total == 0:
                return 0
            else:
                return self._h_internal() / total
        except Exception as e:
            logs.error(
                message=f"in internal_hyperlinks_ratio function in features/internalFeatures.py-->{str(e)}, input is {self.url})")
            return "error"

    def _h_external(self):
        if self.Form is None:
            return None
        return len(self.Href['externals']) + len(self.Link['externals']) + len(self.Media['externals']) + \
            len(self.Form['externals']) + len(self.CSS['externals']) + len(self.Favicon['externals'])

    def external_hyperlinks_ratio(self):
        try:
            if self.Form is None:
                return None
            total = self._h_total()
            if total == 0:
                return 0
            else:
                return self._h_external() / total
        except Exception as e:
            logs.error(
                message=f"in external_hyperlinks_ratio function in features/internalFeatures.py-->{str(e)}, input is {self.url})")
            return "error"

    def _h_null(self):
        if self.Form is None:
            return None
        return len(self.Href['null']) + len(self.Link['null']) + len(self.Media['null']) + len(self.Form['null']) + len(self.CSS['null']) + len(
            self.Favicon['null'])

    def null_hyperlinks_ratio(self):
        try:
            if self.Form is None:
                return None
            total = self._h_total()
            if total == 0:
                return 0
            return self._h_null() / total
        except Exception as e:
            logs.error(
                message=f"in null_hyperlinks_ratio function in features/internalFeatures.py-->{str(e)}, input is {self.url})")
            return "error"

    def external_css(self):
        try:
            if self.CSS is None:
                return None
            return len(self.CSS['externals'])
        except Exception as e:
            logs.error(
                message=f"in external_css function in features/internalFeatures.py-->{str(e)}, input is {self.url})")
            return "error"

    def _h_i_redirect(self):
        if self.Form is None:
            return None
        count = 0
        for link in self.Href['internals']:
            try:
                r = requests.get(link)
                if len(r.history) > 0:
                    count += 1
            except:
                continue
        for link in self.Link['internals']:
            try:
                r = requests.get(link)
                if len(r.history) > 0:
                    count += 1
            except:
                continue
        for link in self.Media['internals']:
            try:
                r = requests.get(link)
                if len(r.history) > 0:
                    count += 1
            except:
                continue
        for link in self.Form['internals']:
            try:
                r = requests.get(link)
                if len(r.history) > 0:
                    count += 1
            except:
                continue
        for link in self.CSS['internals']:
            try:
                r = requests.get(link)
                if len(r.history) > 0:
                    count += 1
            except:
                continue
        for link in self.Favicon['internals']:
            try:
                r = requests.get(link)
                if len(r.history) > 0:
                    count += 1
            except:
                continue
        return count
    # def _h_internal(self):
    #     if self.Form is None:
    #         return None
    #     return len(self.Href['internals']) + len(self.Link['internals']) + len(self.Media['internals']) + \
    #         len(self.Form['internals']) + len(self.CSS['internals']) + len(self.Favicon['internals'])

    def internal_redirection(self):
        try:
            if self.Form is None:
                return None
            internals_value = self._h_internal()
            if (internals_value > 0):
                return self._h_i_redirect() / internals_value
            return 0
        except Exception as e:
            logs.error(
                message=f"in internal_redirection function in features/internalFeatures.py-->{str(e)}, input is {self.url})")
            return "error"

    # def _h_external(self):
    #     if self.Form is None:
    #         return None
    #     return len(self.Href['externals']) + len(self.Link['externals']) + len(self.Media['externals']) + \
    #         len(self.Form['externals']) + len(self.CSS['externals']) + len(self.Favicon['externals'])

    def _h_e_redirect(self):
        if self.Form is None:
            return None
        count = 0
        for link in self.Href['externals']:
            try:
                r = requests.get(link)
                if len(r.history) > 0:
                    count += 1
            except:
                continue
        for link in self.Link['externals']:
            try:
                r = requests.get(link)
                if len(r.history) > 0:
                    count += 1
            except:
                continue
        for link in self.Media['externals']:
            try:
                r = requests.get(link)
                if len(r.history) > 0:
                    count += 1
            except:
                continue
        for link in self.Media['externals']:
            try:
                r = requests.get(link)
                if len(r.history) > 0:
                    count += 1
            except:
                continue
        for link in self.Form['externals']:
            try:
                r = requests.get(link)
                if len(r.history) > 0:
                    count += 1
            except:
                continue
        for link in self.CSS['externals']:
            try:
                r = requests.get(link)
                if len(r.history) > 0:
                    count += 1
            except:
                continue
        for link in self.Favicon['externals']:
            try:
                r = requests.get(link)
                if len(r.history) > 0:
                    count += 1
            except:
                continue
        return count

    def external_redirection(self):
        try:
            if self.Form is None:
                return None
            externals_value = self._h_external()
            if (externals_value > 0):
                return self._h_e_redirect() / externals_value
            return 0
        except Exception as e:
            logs.error(
                message=f"in external_redirection function in features/internalFeatures.py-->{str(e)}, input is {self.url})")
            return "error"

    def _h_i_error(self):
        if self.Form is None:
            return None
        count = 0
        for link in self.Href['internals']:
            try:
                if requests.get(link).status_code >= 400:
                    count += 1
            except:
                continue
        for link in self.Link['internals']:
            try:
                if requests.get(link).status_code >= 400:
                    count += 1
            except:
                continue
        for link in self.Media['internals']:
            try:
                if requests.get(link).status_code >= 400:
                    count += 1
            except:
                continue
        for link in self.Form['internals']:
            try:
                if requests.get(link).status_code >= 400:
                    count += 1
            except:
                continue
        for link in self.CSS['internals']:
            try:
                if requests.get(link).status_code >= 400:
                    count += 1
            except:
                continue
        for link in self.Favicon['internals']:
            try:
                if requests.get(link).status_code >= 400:
                    count += 1
            except:
                continue
        return count

    def internal_errors(self):
        try:
            if self.Form is None:
                return None
            internals_value = self._h_internal()
            if (internals_value > 0):
                return self._h_i_error() / internals_value
            return 0
        except Exception as e:
            logs.error(
                message=f"in internal_errors function in features/internalFeatures.py-->{str(e)}, input is {self.url})")
            return "error"

    def _h_e_error(self):
        if self.Form is None:
            return None
        count = 0
        for link in self.Href['externals']:
            try:
                if requests.get(link).status_code >= 400:
                    count += 1
            except:
                continue
        for link in self.Link['externals']:
            try:
                if requests.get(link).status_code >= 400:
                    count += 1
            except:
                continue
        for link in self.Media['externals']:
            try:
                if requests.get(link).status_code >= 400:
                    count += 1
            except:
                continue
        for link in self.Form['externals']:
            try:
                if requests.get(link).status_code >= 400:
                    count += 1
            except:
                continue
        for link in self.CSS['externals']:
            try:
                if requests.get(link).status_code >= 400:
                    count += 1
            except:
                continue
        for link in self.Favicon['externals']:
            try:
                if requests.get(link).status_code >= 400:
                    count += 1
            except:
                continue
        return count

    def external_errors(self):
        try:
            if self.Form is None:
                return None
            externals_values = self._h_external()
            if (externals_values > 0):
                return self._h_e_error() / externals_values
            return 0
        except Exception as e:
            logs.error(
                message=f"in external_errors function in features/internalFeatures.py-->{str(e)}, input is {self.url})")
            return "error"

    def login_form(self):
        try:
            if self.Form is None:
                return None
            p = re.compile('([a-zA-Z0-9\_])+.php')
            if len(self.Form['externals']) > 0 or len(self.Form['null']) > 0:
                return 1
            for form in self.Form['internals'] + self.Form['externals']:
                if p.match(form) != None:
                    return 0
            return 1
        except Exception as e:
            logs.error(
                message=f"in login_form function in features/internalFeatures.py-->{str(e)}, input is {self.url})")
            return "error"

    def external_favicon(self):
        try:
            if self.Favicon is None:
                return None
            if len(self.Favicon['externals']) > 0:
                return 0
            return 1
        except Exception as e:
            logs.error(
                message=f"in external_favicon function in features/internalFeatures.py-->{str(e)}, input is {self.url})")
            return "error"
    #
    # def links_in_tags(self):
    #
    #     if self.Link is None:
    #         return None
    #     total = len(self.Link['internals']) + len(self.Link['externals'])
    #     internals = len(self.Link['internals'])
    #     try:
    #         percentile = internals / float(total) * 100
    #     except:
    #         return 0
    #     return percentile

    # def submitting_to_email(self):
    #     try:
    #         if self.Form is None:
    #             return None
    #         for form in self.Form['internals'] + self.Form['externals']:
    #             if "mailto:" in form or "mail()" in form:
    #                 return 1
    #             else:
    #                 return 0
    #         return 0
    #     except Exception as e:
    #         logs.error(
    #             message=f"in submitting_to_email function in features/internalFeatures.py-->{str(e)}, input is {self.url})")
    #         return "error"

    def internal_media(self):
        if self.Media is None:
            return None
        total = len(self.Media['internals']) + len(self.Media['externals'])
        internals = len(self.Media['internals'])
        try:
            percentile = internals / float(total) * 100
        except:
            return 0

        return percentile

    def external_media(self):
        if self.Media is None:
            return None
        total = len(self.Media['internals']) + len(self.Media['externals'])
        externals = len(self.Media['externals'])
        try:
            percentile = externals / float(total) * 100
        except:
            return 0

        return percentile

    # def sfh(self):
    #     try:
    #         if self.Form is None:
    #             return None
    #         if len(self.Form['null']) > 0:
    #             return 1
    #         return 0
    #     except Exception as e:
    #         logs.error(
    #             message=f"in sfh function in features/internalFeatures.py-->{str(e)}, input is {self.url})")
    #         return "error"

    # def iframe(self):
    #     try:
    #         if self.IFrame is None:
    #             return None
    #         if len(self.IFrame['invisible']) > 0:
    #             return 1
    #         return 0
    #     except Exception as e:
    #         logs.error(
    #             message=f"in iframe function in features/internalFeatures.py-->{str(e)}, input is {self.url})")
    #         return "error"
    #
    # def popup_window(self):
    #     try:
    #         if self.content is None:
    #             return None
    #         if "prompt(" in str(self.content).lower():
    #             return 1
    #         else:
    #             return 0
    #     except Exception as e:
    #         logs.error(
    #             message=f"in popup_window function in features/internalFeatures.py-->{str(e)}, input is {self.url})")
    #         return "error"

    def safe_anchor(self):
        if self.Anchor is None:
            return None
        total = len(self.Anchor['safe']) + len(self.Anchor['unsafe'])
        unsafe = len(self.Anchor['unsafe'])
        try:
            percentile = unsafe / float(total) * 100
        except:
            return 0
        return percentile

    # def onmouseover(self):
    #     try:
    #         if self.content is None:
    #             return None
    #         if 'onmouseover="window.status=' in str(self.content).lower().replace(" ", ""):
    #             return 0
    #         else:
    #             return 1
    #     except Exception as e:
    #         logs.error(
    #             message=f"in onmouseover function in features/internalFeatures.py-->{str(e)}, input is {self.url})")
    #         return "error"

    # def right_clic(self):
    #     try:
    #         if self.content is None:
    #             return None
    #         if re.findall(r"event.button ?== ?2", self.content):
    #             return 1
    #         else:
    #             return 0
    #     except Exception as e:
    #         logs.error(
    #             message=f"in right_clic function in features/internalFeatures.py-->{str(e)}, input is {self.url})")
    #         return "error"

    def empty_title(self):
        try:
            if self.Title is None:
                return None
            if self.Title:
                return 0
            return 1
        except Exception as e:
            logs.error(
                message=f"in empty_title function in features/internalFeatures.py-->{str(e)}, input is {self.url})")
            return "error"

    def domain_in_title(self):
        try:
            if self.domain is None or self.Title is None:
                return None
            if self.domain.lower() in self.Title.lower():
                return 0
            return 1
        except Exception as e:
            logs.error(
                message=f"in domain_in_title function in features/internalFeatures.py-->{str(e)}, input is {self.url})")
            return "error"

    # def domain_with_copyright(self):
    #     if self.content is None:
    #         return None
    #     try:
    #         m = re.search(u'(\N{COPYRIGHT SIGN}|\N{TRADE MARK SIGN}|\N{REGISTERED SIGN})', self.content)
    #         _copyright = self.content[m.span()[0] - 50:m.span()[0] + 50]
    #         if self.domain.lower() in _copyright.lower():
    #             return 0
    #         else:
    #             return 1
    #     except Exception as e:
    #             logs.error(
    #                 message=f"n domain_with_copyright function in features/internalFeatures.py-->{str(e)}")
    #             return 0

    def whois_registered_domain(self):
        try:
            hostname = whois.whois(self.domain).domain_name
            if type(hostname) == list:
                for host in hostname:
                    if re.search(host.lower(), self.domain):
                        return 0
                return 1
            else:
                if re.search(hostname.lower(), self.domain):
                    return 0
                else:
                    return 1
        except Exception as e:
            logs.error(
                message=f"n whois_registered_domain function in features/internalFeatures.py-->{str(e)}")
            return 1

    def domain_registration_length(self):
        try:
            res = whois.whois(self.domain)
            expiration_date = res.expiration_date
            today = datetime.datetime.now()

            if expiration_date:
                if isinstance(expiration_date, list):
                    expiration_date = min(expiration_date)
                return abs((expiration_date - today).days)
            else:
                return 0
        except Exception as e:
            logs.error(message=f"n domain_registration_length function in features/internalFeatures.py-->{str(e)}")
            return -1

    def domain_age(self):
        try:
            res = whois.whois(self.url)
            creation_date = res.creation_date
            today = datetime.datetime.now()
            age = (today - creation_date).days
            # if creation_date:
            #     if isinstance(creation_date, list):
            #         creation_date = min(creation_date)
            #     # Ensure creation_date is a datetime object
            #     if not isinstance(creation_date, datetime):
            #         creation_date = datetime.datetime.strptime(str(creation_date), '%Y-%m-%d %H:%M:%S')

            return age
            # else:
            #     return "Creation date not available"
        except Exception as e:
            logs.error(message=f" domain_age function in features/internalFeatures.py-->{str(e)}, input is {self.url}")
            return "Error"

    def get_qty_nameservers(self):
        try:
            answers = dns.resolver.resolve(self.domain, 'NS')
            return len(answers)
        except Exception as e:

            logs.error(message=f" get_qty_nameservers function in features/internalFeatures.py-->{str(e)}, input is {self.url}")
            return "Error"

    def get_qty_mx_servers(self):
        try:
            answers = dns.resolver.resolve(self.domain, 'MX')
            return len(answers)
        except Exception as e:

            logs.error(
                message=f" get_qty_mx_servers function in features/internalFeatures.py-->{str(e)}, input is {self.url}")
            return "Error"

    def get_ttl_hostname(self):
        try:
            answers = dns.resolver.resolve(self.domain, 'A')
            return answers.rrset.ttl
        except Exception as e:

            logs.error(
                message=f" get_ttl_hostname function in features/internalFeatures.py-->{str(e)}, input is {self.url}")
            return "Error"

    def is_tls_ssl_certificate_valid(self):
        try:
            context = ssl.create_default_context()
            with socket.create_connection((self.domain, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=self.domain) as ssock:
                    ssock.getpeercert()
                    return True
        except Exception as e:
                    logs.error(
                        message=f" is_tls_ssl_certificate_valid function in features/internalFeatures.py-->{str(e)}, input is {self.url}")
                    return "Error"

    def get_open_pagerank(self):
        try:
            print("url is -->", self.url)
            endpoint = "https://openpagerank.com/api/v1.0/getPageRank"
            api_key = "gcgo8occs40w4kooo8wog8k00co0ok8cwo4ksww8"
            """
            sagnik = ccgc8g8cs4wkk48kg4wkcc00gswsccks4gco4ww0
            ashis = gcgo8occs40w4kooo8wog8k00co0ok8cwo4ksww8
            sachin = ck4o408g8swssw4w044wkosowkkccsk8sw0cw4os
            diti = 0sggoc8cg8k00wc4cgo48k84gk0sgg8www8k480o
            """
            headers = {
                "API-OPR": api_key
            }
            params = {
                "domains[]": self.domain
            }

            response = requests.get(endpoint, headers=headers, params=params)

            if response.status_code == 200:
                data = response.json()

                print("rank is -->", data['response'][0]['page_rank_integer'])
                return data['response'][0]['page_rank_integer']

        except Exception as e:
                    logs.error(
                        message=f" get_open_pagerank function in features/internalFeatures.py-->{str(e)}, input is {self.url}")
                    return "Error"
