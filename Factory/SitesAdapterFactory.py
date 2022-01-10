from Factory.WollPlatz.WollPlatzAdapter import WollPLatzAdapter
#from Factory.MarketExpress.MarketExpressAdapter import MarketExpressAdapter
from Factory.LasTijerasMagicas.LasTijerasMagicasAdapter import LasTijerasMagicasAdapter
from Factory.WoolHouse.WoolHouseAdapter import WoolHouseAdapter
from Factory.YarnPlaza.YarnPlazaAdapter import YarnPlazaAdapter

class SitesAdapterFactory:

    def __init__(self):
        self.adapters = dict (
            WollPlatz = WollPLatzAdapter(),
            LasTijerasMagicas = LasTijerasMagicasAdapter(),
            WoolHouse = WoolHouseAdapter(),
            YarnPlaza = YarnPlazaAdapter()
            #MarketExpress=MarketExpressAdapter(),
            #Other Website Adapters will be initialized here
        )

    def initialize_scrapping(self):
        all_products = dict()

        for site in self.adapters:
             all_products[site] = self.adapters[site].read_website_info()

        return all_products

