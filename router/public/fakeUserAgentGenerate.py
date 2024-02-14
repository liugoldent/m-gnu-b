import random

def userAgentRoute():
    ieAgent = 'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)'
    operaAgent = 'Opera/9.80(X11; Linux i686; U; ru) Presto/2.8.131 Version/11.11'
    chromeAgent = 'Mozilla/5.0(Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2'
    googleAgent = 'Mozilla/5.0(Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13'
    chromeAgent =  'Mozilla/5.0(X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11'
    firefoxAgent = 'Mozilla/5.0(Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1'
    ffAgent = 'Mozilla/5.0(X11; Ubuntu; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0.1'
    safariAgent = 'Mozilla/5.0(iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25'
    agentList = [ieAgent, operaAgent, chromeAgent, googleAgent, firefoxAgent, ffAgent, safariAgent]
    randomNum = random.randint(0, len(agentList)-1)
    return agentList[randomNum]