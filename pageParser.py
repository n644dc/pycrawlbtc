import html.parser
import urllib.request
import urllib.parse


class LinkParser(html.parser.HTMLParser):
  def __init__(self):
    html.parser.HTMLParser.__init__(self)
    proxy_url = 'dfw-proxy.ext.ray.com:80'
    s_proxy_url = 'dfw-proxy.ext.ray.com:80'
    proxy_support = urllib.request.ProxyHandler({'http': proxy_url})
    s_proxy_support = urllib.request.ProxyHandler({'https': s_proxy_url})
    opener = urllib.request.build_opener(proxy_support, urllib.request.HTTPHandler)
    opener.add_handler(s_proxy_support)
    urllib.request.install_opener(opener)


  def handle_starttag(self, tag, attrs):
    if tag == 'a':
      for (key, value) in attrs:
        if key == 'href':
          if 'querypk' in value:
            pkRawArr = value.split('/')
            self.currentPK = pkRawArr[len(pkRawArr)-1]
          if 'okcoin.cn' in value:
            addressRawArr = value.split('/')
            self.currentAddress.append(addressRawArr[len(addressRawArr)-1])
            if len(self.currentAddress) == 2 and self.currentPK and not self.currentPK.isspace():
              acct = []
              acct.append(self.currentPK, self.currentAddress)
              self.accts.append(acct)
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


def spider(seed):
  parser = LinkParser()
  numberChecked = 0

  parser.getPage('http://washen.me/800')

  for acct in parser.accts:
    print(acct)
