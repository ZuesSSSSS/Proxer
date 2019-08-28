from cmd import Cmd
from os import system
import requests
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
        if (200 in r):
            print(Fore.GREEN, "API ONLINE", Style.RESET_ALL)
        else:
            print(Fore.RED, "API OFFLINE", Style.RESET_ALL)
        # print(r.content)
    def do_country(self, args):
        """Country Codes (Alpha 2)"""
        print("all country codes and countries")

    def do_list(self, args):
        """Amount of Proxies in Countries and which Anonymity"""
        print("countries && check amount of proxies in that country && amount of which type (anon)")

    def do_quit(self, args):
        """Quits the program"""
        raise SystemExit


if __name__ == '__main__':
    system('cls')
    prompt = MyPrompt()
    prompt.prompt = '> '
    prompt.cmdloop(f.renderText('Interactive Proxy CLI'))
