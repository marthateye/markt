from DB.ProductDBModelAdapter import ProductDBModelAdapter
from Models.ProductTagProps import ProductTagProps
from Models.ProductMeta import ProductMeta
from Models.BrandSearchModel import BrandSearchModel
from Utils.WebScrapper import WebScrapper
from Utils.ProductPageReader import ProductPageReader


def set_brand_params():
    brand_params = [BrandSearchModel('bulk-store', ['Rice', 'Water']),
                    BrandSearchModel('drinks', ['Milk', 'Alcohol'])]

    return brand_params


def set_props():
    target_element_properties = [ProductTagProps('Name', 'h1', {"class" : "page-title"}),
                                 ProductTagProps('ShortName', 'h1', {"class": "page-title"}),
                                 ProductTagProps('Price', 'span', {"class": "current-price"}),
                                 ProductTagProps('Currency','span',{"class":"current-price"}),
                                 ProductTagProps('Description','div',{"class":"product-description"})]
    return target_element_properties


class MarketExpressAdapter:
    def __init__(self):
        self.brand_search_params = set_brand_params()
        self.target_element_properties = set_props()
        self.results_per_page = 100
        self.brand_url = 'https://marketexpress.com.gh/{}?page={}&resultsPerPage={}'
        self.max_pages = 3
        self.store = "MarketExpress"


    def read_website_info(self):

        web_scrapper = WebScrapper()
        product_page_reader = ProductPageReader()
        product_db_adapter = ProductDBModelAdapter()


        products = []

        for brand_meta in self.brand_search_params:
            is_page_complete = False
            starting_page = 1

            while is_page_complete == False:
                target_url = self.brand_url.format(brand_meta.brand_name, starting_page,self.results_per_page)
                html_markup = web_scrapper.get_html_markup(target_url)

                print('Scrapping brand ({}) from {} , on Page = {}'.format(brand_meta.brand_name,target_url,starting_page))

                product_list = html_markup.find_all("div", {"class": "js-product-miniature-wrapper"})
                # read products
                print('{} products found'.format(len(product_list)))
                for product in product_list:
                    link = product.find("a", {"class": "product-thumbnail"}).get('href')
                    image = product.find("img", {"class": "js-lazy-product-image"}).get('src')

                    base_product = dict(Store=self.store, Brand=brand_meta.brand_name, Link=link, Image=image)

                    product_info = product_page_reader.get_prop_values(base_product,
                                                                       self.target_element_properties,
                                                                       brand_meta.keywords,
                                                                       self,
                                                                       product_db_adapter)
                    if product_info != None:
                        products.append(product_info)

                if len(product_list) < self.results_per_page:
                    is_page_complete = True
                elif starting_page >= self.max_pages:
                    is_page_complete = True
                else :
                    starting_page += 1

        return products

    def run_custom_prop_values(self, html_markup, matching_values):
        try:
            price = html_markup.find("span", {"class": "product-price"}).get('content')
        except:
            price = None

        if price != None:
            matching_values['Price'] = price
            currency = str(matching_values['Currency'])
            matching_values['Currency'] = str(currency).replace(price,'')

        return matching_values