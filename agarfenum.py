import requests, random, time
from optparse import OptionParser

parser = OptionParser()

parser.add_option('-u', '--url', dest = 'url', type = 'string')
parser.add_option('-w', '--wordlist', dest = 'file', metavar = "FILE")
parser.add_option('--waf-bypass', action='store_true', dest='waf')
(options, args) = parser.parse_args()

class bcolors:
    reset = "\033[0m"
    green = "\u001b[32m"
    yellow = "\u001b[33m"
    blue = "\u001b[34m"
    red = "\u001b[31m"

def Usage():
    print ('''{}VERSION:{}
agarfenum 1.0

{}USAGE:{}
agarfenum.py -u http://host.com -w /path/to/the/file

{}OPTIONS:{}
-w, --wordlist <FILE>   Wordlist path
-u, --url <URL>         The target URL
--waf-bypass            Alias for --random-user-agent '''.format(bcolors.red, bcolors.reset,bcolors.red, bcolors.reset,bcolors.red, bcolors.reset))


user_agent_list = [
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36'
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9',
    'Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/7.1.8 Safari/537.85.17',
    'Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4',
    'Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F69 Safari/600.1.4',
    'Mozilla/5.0 (Windows NT 6.1; rv:40.0) Gecko/20100101 Firefox/40.0'
]



if( options.url and options.file != None):
    if "http://" not in options.url and "https://" not in options.url:
        print('Missing "http://" or "https://" in url :)')
        exit()
    filename = open(options.file)
    wordlist = filename.readlines()
    number = 0
    if (options.waf):
            print("{}[!] WAF bypass enabled, the scan will take a little longer{}".format(bcolors.yellow, bcolors.reset))
            for directory in wordlist:
                user_agent = random.choice(user_agent_list)
                number += 1
                time.sleep(0.5)
                x = requests.get("{}/{}".format(options.url, directory.strip()), allow_redirects=True, headers = {'User-Agent': user_agent + str(number)})
                statusc = x.status_code
                if(statusc == 200):
                    print("{}/{} - {}{}{}".format(options.url, directory.strip(), bcolors.green, statusc, bcolors.reset))
                elif (statusc == 301):
                    print("{}/{} - {}{}{}".format(options.url, directory.strip(), bcolors.blue, statusc, bcolors.reset))
                elif (statusc == 403):
                    print("{}/{} - {}{}{}".format(options.url, directory.strip(), bcolors.yellow, statusc, bcolors.reset))
                else:
                    print("{}/{} - {}{}{}".format(options.url, directory.strip(), bcolors.red, statusc, bcolors.reset))
            filename.close()
    else:
        for directory in wordlist:
            user_agent = random.choice(user_agent_list)
            x = requests.get("{}/{}".format(options.url, directory.strip()), allow_redirects=True, headers = {'User-Agent': user_agent})
            statusc = x.status_code
            if(statusc == 200):
                print("{}/{} - {}{}{}".format(options.url, directory.strip(), bcolors.green, statusc, bcolors.reset))
            elif (statusc == 301):
                print("{}/{} - {}{}{}".format(options.url, directory.strip(), bcolors.blue, statusc, bcolors.reset))
            elif (statusc == 403):
                print("{}/{} - {}{}{}".format(options.url, directory.strip(), bcolors.yellow, statusc, bcolors.reset))
        filename.close()
else:
    Usage()