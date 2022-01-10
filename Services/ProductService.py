#from Factory.SitesAdapterFactory import SitesAdapterFactory
from DB.ProductDBModelAdapter import ProductDBModelAdapter

class ProductService:
    def __init__(self):
        self.desc = "ProductService"

    def summary(self):
        products_db_adapter = ProductDBModelAdapter()
        products = products_db_adapter.get_products()
        summary = dict(
            Products = products,
            total_product_count = len(products),
            Stores = products_db_adapter.get_unique(),
            Brands = products_db_adapter.get_unique('Brand'),
            Keywords = products_db_adapter.get_unique('Keyword')
        )

        return summary

    def get_summary(self,products):
        products_db_adapter = ProductDBModelAdapter()
        summary = dict(
            Products = products,
            total_product_count = len(products),
            Stores = products_db_adapter.get_unique(),
            Brands = products_db_adapter.get_unique('Brand'),
            Keywords = products_db_adapter.get_unique('Keyword')
        )

        return summary