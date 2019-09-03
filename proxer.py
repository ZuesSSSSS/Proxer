from cmd import Cmd
from os import system
from colorama import Fore, Back, Style
from pyfiglet import Figlet
import requests, json, random, re, time

class proxy():

    yes = ['y', 'ye', 'yes']

    def tryAgain():

        print(Fore.YELLOW, "Try Again", Style.RESET_ALL)

    def noProxies(proxyAmount):

        if (proxyAmount < 1):
            return Fore.BLUE, "No Proxies Found", Style.RESET_ALL

    def saveFile(data):

        amountOfProxies = 0
        amountChoice = input("Do you want more than one proxy? (Y/N)")
        
        if (amountChoice in proxy.yes):
            
            with open('Proxies.txt', 'w') as f:
                for item in data:
                    amountOfProxies += 1
                    f.write("%s\n" % item)
            print(f"Proxies.txt is updated with {amountOfProxies} amount of proxies.")
        else:
            if (len(data) == 1):
                index = 0
            else:
                index = random.randint(0, len(data))
            temp = data[index].split(":")
            print(f"Address: {temp[0]}\nPort: {temp[1]}")

    @staticmethod
    def clean():

        f = Figlet(font='slant')

        system('cls')
        print(Figlet(font='slant').renderText('Interactive Proxy CLI'))
        print(Fore.GREEN, "API ONLINE", Style.RESET_ALL)
        
    @staticmethod
    def getProtocol():

        options = ['Http', 'Https', 'Socks4', 'Socks5']
        typeInput = input(f'{options} ').lower()

        if (typeInput.title() in options):
            typeChoice = f'?type={typeInput}'
            return typeChoice
        else:
            print(Fore.RED, "Error; type not recognized", Style.RESET_ALL)
            proxy.tryAgain()
            proxy.getProtocol()

    @staticmethod
    def getAnon():

        anon = input("Choose Anonymity? (Y/N)").lower()

        if (anon in proxy.yes):
            
            options = ['Transparent', 'Anonymous', 'Elite']
            anonInput = input(f'{options} ').lower()

            if (anonInput.title() in options):
                anonChoice = f'&anon={anonInput}'
                return anonChoice
            else:
                print(Fore.MAGENTA, f"\'{anonInput}\' Not Supported", Style.RESET_ALL)
                proxy.tryAgain()
                proxy.getAnon()

    @staticmethod
    def getCountry():

        country = input("Choose Country? (Y/N)").lower()

        if (country in proxy.yes):

            print("Examples: United States: US | Canada: CA | China: CN | Russia: RU")
            countryInput = input("Country Code (Alpha 2): ").upper()

            with open('country_codes.txt') as f:
                countryFound = re.search(rf'\b{countryInput}\b', f.read())
                if (countryFound):
                    countryChoice = f'&country={countryInput}'
                    return countryChoice
                else:
                    print(Fore.RED, "Country Code Not Recognized", Style.RESET_ALL)
                    proxy.tryAgain()
                    proxy.getCountry()

    @staticmethod
    def parseUrlArgs():

        url = 'https://www.proxy-list.download/api/v1/get' 

        urlType = proxy.getProtocol()
        urlAnon = proxy.getAnon()
        urlCountry = proxy.getCountry()

        url += urlType
        urlAnonExists = None
        urlCountryExists = None


        try:
            urlAnon
        except NameError: 
            pass
        try:
            urlCountry
        except NameError:
            pass

        if (urlAnonExists):
            url += urlAnon
        if (urlCountryExists):
            url += urlCountry

        return url
        
    @staticmethod
    def checkStatus(url):
        
        r =  requests.get(url)

        if (r.status_code == 200):
            return True
        else:
            return False
            
    @staticmethod
    def showProxies(url):

        r = requests.get(url)
        data = r.text
        data = data.replace('b', '')
        data = data.split('\r\n')
        data.pop()

        proxyAmount = len(data)
        proxy.noProxies(proxyAmount)
        proxy.printProxies(data)
        return data
      
    def printProxies(data):
        proxy.clean()
        proxy.saveFile(data)

class MyPrompt(Cmd):

    def do_proxy(self, args):
        """Interactive Proxy CLI"""

        url = proxy.parseUrlArgs()

        if (proxy.checkStatus(url)):
            proxy.showProxies(url)
        else:
            return Fore.RED, "API OFFLINE", Style.RESET_ALL

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
    prompt.cmdloop(proxy.clean())
