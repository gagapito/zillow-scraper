from bs4 import BeautifulSoup
import requests
import json
import time
import csv
import os

class ZillowScrapper():

    results = []

    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'cookie': 'zguid=23|%245274b5f4-143e-4d4f-a089-82e7d57e23e8; zgsession=1|3670c721-3ccc-4238-b01f-2820fa16a480; _ga=GA1.2.61196005.1638382908; _gid=GA1.2.146855758.1638382908; zjs_user_id=null; zjs_anonymous_id=%225274b5f4-143e-4d4f-a089-82e7d57e23e8%22; _pxvid=8c1c2062-52d3-11ec-b21c-6270424f7549; _gcl_au=1.1.1480610121.1638382912; KruxPixel=true; DoubleClickSession=true; __pdst=79f93aa412ea487b8b84c1368dd53719; _pin_unauth=dWlkPVpESTFNR1V3WkRNdE9HUXpaQzAwTTJGakxUazBPR1l0WmpVNE1qTXpOV1kzTTJNdw; KruxAddition=true; g_state={"i_p":1638500375159,"i_l":2}; JSESSIONID=BEC7D6CFFAA2013D1B04A4ECAEDE5F66; utag_main=v_id:017d773b46da00a99c0afca3a51805078003107000942$_sn:2$_se:1$_ss:1$_st:1638481733703$dc_visit:1$ses_id:1638479933703%3Bexp-session$_pn:1%3Bexp-session; _cs_c=0; _pxff_bsco=1; _pxff_tm=1; _gat=1; _cs_id=30ce4818-b0f7-ac08-de59-6485ea2267fc.1638480002.1.1638480500.1638480002.1.1672644002876; _cs_s=3.5.0.1638482300418; _px3=58fc46663d1436e0d716aefc20b2f4a9d78ac1c41ac0290b4ff3dcd284bcf4ff:IXV/XTx9au2a0Y48ShtF6k1pJZNbo736Osec5xlxvH1Kb6simadKteMBy5EqaiPLWcPouCaqiooFw/vjCWew8w==:1000:fHUq/Njaxhjx8bMk6b/r/E5L6zMm2eCIdFvpw8HQx9E4rRbnHQZ2s/wIFfVOrI5ixAKEzyuHdbIo72axAeUC/V7npOV8Hdi8DmzIjz4jXNPBwKz5NPV69iiiB6x3TnIOAeCCnuCV3Wyy5/1EBnA/pNpbU+MJC+Tk0OqAi4VqqMjOhB7CGQ6z+TVIou2IH3ZmSe0cjLp9KHsjcxgiI8ksPw==; _uetsid=8ef33c8052d311ec9740c513635fdb82; _uetvid=8ef4089052d311eca78e410bed5dc851; AWSALB=Yv9GG03MC9PrHcfZ5Th72QaXRJlo/3ZpFVamuNXCLVgm1Y9BGZOQgj4M1mRrtc97lTdL0DwSw+isveR9ywiulUjXXbXb3Lf19FeFaf0yxWXtyHLRsXrEjuIH7HER; AWSALBCORS=Yv9GG03MC9PrHcfZ5Th72QaXRJlo/3ZpFVamuNXCLVgm1Y9BGZOQgj4M1mRrtc97lTdL0DwSw+isveR9ywiulUjXXbXb3Lf19FeFaf0yxWXtyHLRsXrEjuIH7HER; search=6|1641072516930%7Crect%3D34.36695177140153%252C-117.96472627441406%252C33.673773605506085%252C-118.85873872558594%26rid%3D12447%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26z%3D1%26fs%3D1%26fr%3D0%26mmm%3D0%26rs%3D0%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%26featuredMultiFamilyBuilding%3D0%09%0912447%09%09%09%09%09%09',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36'
    }

    def fetch(self, url, params):
        response = requests.get(url, headers=self.headers, params=params)
        print(response.status_code)
        return response

    def parse(self, response):
        content = BeautifulSoup(response, 'lxml')
        deck = content.find('ul', {'class': 'photo-cards photo-cards_wow photo-cards_short photo-cards_extra-attribution'})
        for card in deck.contents:
            script = card.find('script', {'type': 'application/ld+json'})
            if script:
                script_json = json.loads(script.contents[0])
                
                self.results.append({
                    'address': script_json['name'],
                    'latitude': script_json.get('geo').get('latitude'),
                    'longitude': script_json.get('geo').get('longitude'),
                    'floorSize': script_json['floorSize']['value'],
                    'price': card.find('div', {'class': 'list-card-price'}).text,
                    'url': script_json['url']       
                })

    def to_csv(self):
        with open('zillow.csv', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())
            writer.writeheader()

            for row in self.results:
                writer.writerow(row)
        
    def run(self):
        url = 'https://www.zillow.com/los-angeles-ca/'

        for page in range(1,21):
            params = {
            'searchQueryState': '{"pagination":{"currentPage": %s},"usersSearchTerm":"Los Angeles, CA","mapBounds":{"west":-118.85873872558594,"east":-117.96472627441406,"south":33.673773605506085,"north":34.36695177140153},"regionSelection":[{"regionId":12447,"regionType":6}],"isMapVisible":true,"filterState":{"sort":{"value":"globalrelevanceex"},"ah":{"value":true}},"isListVisible":true}' %page
            }
            res = self.fetch(url, params)
            self.parse(res.text)
            time.sleep(2)
        self.to_csv()


if __name__ == '__main__':
    scraper = ZillowScrapper()
    scraper.run()