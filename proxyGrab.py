from bs4 import BeautifulSoup as bs
import requests
# url="https://free-proxy-list.net/"
url = "https://www.proxy-list.download/api/v1"

result = requests.get(url)
content = result.content
soup = bs(content, "html.parser")
table = soup.find_all("tr")

for data in table:
    print("Ip Address: %s") % data[0]
    print("Port: %s") % data[1]
    print("Code: %s") % data[2]
    print("Anonymity %s") % data[3]
    print("Https: %s") % data[4]
    print("Updated: %s") % data[7]
