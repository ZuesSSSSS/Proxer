from cmd import Cmd
from os import system
import requests, json, random
from colorama import Fore, Back, Style
from pyfiglet import Figlet
f = Figlet(font='slant')

class MyPrompt(Cmd):

    def do_proxy(self, args):
        """Interactive Proxy CLI"""
        url = 'https://www.proxy-list.download/api/v1/get'

        type = input("http, https, socks4, socks5: ").lower()
        if (type in ['http', 'https', 'socks4', 'socks5']):
            url += '?type=%s' % type
        else:
            print(Fore.RED, "Error; type not recognized", Style.RESET_ALL)
            return
        if (input("Choose Anonymity? (Y/N)").lower() in ['y', 'ye', 'yes']):
            anon = input("Transparent, Anonymous, Elite: ").lower()
            if (anon in ['transparent', 'anonymous', 'elite']):
                url += '&anon=%s' % anon
            else:
                print(Fore.MAGENTA, f"\'{anon}\' Not Supported", Style.RESET_ALL)
                print(Fore.YELLOW, "--IGNORING--", Style.RESET_ALL)
        if (input("Choose Country? (Y/N)").lower() in ['y', 'ye', 'yes']):
            print("Examples: United States: US | Canada: CA | China: CN | Russia: RU")
            country = input("Country Code (Alpha 2): ").upper()
            with open('country_codes.txt',) as f:
                if (country in f.read()):
                    url+= '&country=%s' % country
                else:
                    print(Fore.RED, "Country Code Not Recognized", Style.RESET_ALL)
                    return
        r = requests.get(url)
        if (r.status_code == 200):
            data = (r.text)
            data = data.replace('b', '')
            data = data.split('\r\n')
            data.pop()
            if (len(data) < 1):
                print(url)
                print(Fore.YELLOW, "No Proxies Found", Style.RESET_ALL)
                return
            output = input("Do you want more than one? (Y/N)")
            system('cls')
            print(Figlet(font='slant').renderText('Interactive Proxy CLI'))
            print(Fore.GREEN, "API ONLINE", Style.RESET_ALL)
            if (output in ['y', 'ye', 'yes']):
                with open('proxies.txt', 'w') as f:
                    for item in data:
                        f.write("%s\n" % item)
                print("Proxies.txt is updated")
            else:
                if (len(data) == 1):
                    index = 0
                else:
                    index = random.randint(0, len(data))
                temp = data[index].split(":")
                print("Address: %s" % temp[0])
                print("Port: %s" % temp[1])
        else:
            print(Fore.RED, "API OFFLINE", Style.RESET_ALL)
            return

    def do_country(self, args):
        """Country Codes (Alpha 2)"""
        with open("countries.txt") as textfile1, open("country_codes.txt") as textfile2:
            for x, y in zip(textfile1, textfile2):
                x = x.strip()
                y = y.strip()
                print(f"{x:<45}{y:>10}")

    def do_list(self, args):
        """Amount of Proxies in Countries and which Anonymity"""
        url = 'https://www.proxy-list.download/api/v1/get?type='
        types=('http','https','socks4','socks5')
        with open("countries.txt") as textfile1, open("country_codes.txt") as textfile2:
            print("Country (Country Code) | HTTP | HTTPS | SOCKS4 | SOCKS5")
            for x, y in zip(textfile1, textfile2):
                country = x.strip()
                countryCode = y.strip()
                tempData = {'http':0,'https':0,'socks4':0,'socks5':0}
                i=0
                for x in types:
                    tempUrl = (url + x)
                    r = requests.get(tempUrl)
                    if (r.status_code == 200):
                        data = (r.text)
                        data = data.replace('b', '')
                        data = data.split('\r\n')
                        data.pop()
                        tempData.update({x:len(data)})
                        i+=1
                        if (i == 4):
                            print(f"{country} ({countryCode}) | {tempData['http']} | {tempData['https']} | {tempData['socks4']} | {tempData['socks5']}")
                    if (r.status_code != 200):
                        print(Fore.RED, "API OFFLINE", Style.RESET_ALL)


    def do_quit(self, args):
        """Quits the program"""
        raise SystemExit


if __name__ == '__main__':
    system('cls')
    prompt = MyPrompt()
    prompt.prompt = '> '
    prompt.cmdloop(f.renderText('Interactive Proxy CLI'))
