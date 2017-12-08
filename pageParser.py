import html.parser
import urllib.request
import urllib.parse
import random
import os


class LinkParser(html.parser.HTMLParser):
    def __init__(self):
        self.currentPK = ''
        self.currentAddress = []
        self.accounts = []
        self.baseUrl = ''
        html.parser.HTMLParser.__init__(self)

        # proxy_url = 'someproxy.com:80'
        # s_proxy_url = 'someproxy.com:80'
        # proxy_support = urllib.request.ProxyHandler({'http': proxy_url})
        # s_proxy_support = urllib.request.ProxyHandler({'https': s_proxy_url})
        opener = urllib.request.build_opener(urllib.request.HTTPHandler)
        # opener.add_handler(s_proxy_support)
        urllib.request.install_opener(opener)

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    if 'querypk' in value:
                        pkRawArr = value.split('/')
                        self.currentPK = pkRawArr[len(pkRawArr) - 1]
                    if 'okcoin.cn' in value:
                        addressRawArr = value.split('/')
                        self.currentAddress.append(addressRawArr[len(addressRawArr) - 1])
                        if len(self.currentAddress) == 2 and self.currentPK and not self.currentPK.isspace():
                            acct = [self.currentPK, self.currentAddress]
                            self.accounts.append(acct)
                            self.currentPK = ''
                            self.currentAddress = []

    def getPage(self, url):
        self.currentPK = ''
        self.currentAddress = []
        self.accounts = []

        try:
            self.baseUrl = url
            user_agent = 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'  # pass bot stuff
            headers = {'User-Agent': user_agent}

            request = urllib.request.Request(self.baseUrl, data=None, headers=headers, unverifiable=False, method='GET')
            response = urllib.request.urlopen(request)

            if response.getheader('Content-Type').lower().startswith('text/html'):
                htmlBytes = response.read()
                htmlString = htmlBytes.decode("utf-8")
                self.feed(htmlString)
                return htmlString.lower()
            else:
                return "", [], False
        except Exception as e:
            print(e)
            return "", [], False


def spider():
    parser = LinkParser()
    maximumCheck = 0

    while maximumCheck < 1000000:
        seed = random.getrandbits(64)
        print(seed)
        pageNumber = seed

        if not os.path.exists("C:\\Users\\n644d\\code\\accts\\{}".format(seed)):
            os.makedirs("C:\\Users\\n644d\\code\\accts\\{}".format(seed))

        while pageNumber >= seed:
            parser.getPage("http://washen.me/{}".format(seed))

            with open("C:\\Users\\n644d\\code\\accts\\{}\\{}.txt".format(seed, pageNumber), "w") as savFile:
                for acct in parser.accounts:
                    savFile.write("{}, {}, {}\n".format(acct[0], acct[1][0], acct[1][1]))
            print('Page #{} saved!'.format(pageNumber))
            pageNumber = pageNumber + 1
            maximumCheck = maximumCheck + 1
            if pageNumber == (seed + 1000):
                break



