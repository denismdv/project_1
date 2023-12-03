import requests
from bs4 import BeautifulSoup
import data_client



class Parser:
    links_to_pars = [
    "https://www.kufar.by/l/mebel",
    "https://www.kufar.by/l/mebel?cursor=eyJ0IjoiYWJzIiwiZiI6dHJ1ZSwicCI6MiwicGl0IjoiMjgzNDczMTcifQ%3D%3D",
    "https://www.kufar.by/l/mebel?cursor=eyJ0IjoiYWJzIiwiZiI6dHJ1ZSwicCI6MywicGl0IjoiMjgzNDg0OTIifQ%3D%3D"
                 ]
    
    data_client_imp = data_client.PostgresClient()
    # data_client_imp = data_client.SqliteClient()
    # data_client_imp = data_client.CsvClient()

    
    @staticmethod
    def get_mebel_items(url):
        response = requests.get(url)
        mebel_data = response.text
        soup = BeautifulSoup(mebel_data, 'html.parser')
        
        mebel_items = []
        for elem in soup.find_all('a', class_='styles_wrapper__5FoK7'):
            try:
                price, decription = elem.text.split('р.')
                mebel_items.append((
                    elem['href'],
                    int(price.replace(' ', '')),
                    decription
                ))
            except:
                print(f'Цена не была указана. {elem.text}')
        
        return mebel_items
        
    def save_to_postgres(self, mebel_items):
        self.data_client_imp.create_mebel_table()
        for item in mebel_items:
            self.data_client_imp.insert_items(item[0], item[1], item[2])
        
    def run(self):
        mebel_items = []
        for url in self.links_to_pars:
            mebel_items.extend(self.get_mebel_items(url))
        self.save_to_postgres(mebel_items)


Parser().run()