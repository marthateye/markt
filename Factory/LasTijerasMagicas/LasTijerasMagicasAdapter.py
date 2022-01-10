from Models.ProductTagProps import ProductTagProps
#from Models.ProductMeta import ProductMeta
from Models.BrandSearchModel import BrandSearchModel
from Utils.WebScrapper import WebScrapper
from Utils.ProductPageReader import ProductPageReader
from DB.ProductDBModelAdapter import ProductDBModelAdapter


def set_brand_params():
    brand_params = [BrandSearchModel('DMC', ['Natura XL'],'https://www.lastijerasmagicas.com/en/dmc-yarns-188?page={}'),
                    BrandSearchModel('Drops', ['Safran', 'Baby Merino Mix'],'https://www.lastijerasmagicas.com/en/drops-yarn-187?page={}')
                    ]

    return brand_params


def set_props():
    target_element_properties = [ProductTagProps('Name', 'div', {"class" : "product-name"}),
                                 ProductTagProps('Price', 'div', {"class": "current-price"}),
                                 ProductTagProps('Description','div',{"id": "product-description-short"})]
    return target_element_properties


class LasTijerasMagicasAdapter:
    def __init__(self):
        self.brand_search_params = set_brand_params()
        self.target_element_properties = set_props()
        self.max_pages = 10
        self.results_per_page = 12
        self.store = "LasTijerasMagicas"

    def read_website_info(self):

        web_scrapper = WebScrapper()
        product_page_reader = ProductPageReader()
        product_db_adapter = ProductDBModelAdapter()

        products = []

        for brand_meta in self.brand_search_params:
            is_page_complete = False
            starting_page = 1

            while is_page_complete == False:
                target_url = brand_meta.url.format(starting_page)
                html_markup = web_scrapper.get_html_markup(target_url)

                print('Scrapping brand ({}) from {} , on Page = {}'.format(brand_meta.brand_name,target_url,starting_page))

                # read products
                product_list = html_markup.find_all("article", {"class": "product-miniature"})
                print('{} products found'.format(len(product_list)))
                for product in product_list:

                    product_name = product.find("h3",{"class":"product-title"}).text.replace('\n', "")
                    selected_keyword = None

                    is_match = False
                    for keyword in brand_meta.keywords:
                        if keyword.lower() in product_name.lower():
                            is_match = True
                            selected_keyword = keyword
                            break

                    if is_match == False:
                        continue

                    link = product.find("a", {"class": "product-thumbnail"}).get('href')
                    image = product.find("img", {}).get('src')

                    base_product = dict(Store=self.store, Brand=brand_meta.brand_name, Link=link,
                                        Image = image, ShortName = product_name, Currency = '€',Keyword=selected_keyword)


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
                currency = str(matching_values['Currency'])
    
                if matching_values['Price'] != None:
                    matching_values['Price'] = str(matching_values['Price']).replace(currency, '')
    
                features = html_markup.find('section', {"class": "product-features"})
                all_features = features.find_all("li")  # contains 2 rows
    
                for feature in all_features:
                    column_title = feature.find('span', {"class": "name"}).text.lower()
                    if 'size' in column_title:
                        print(column_title)
                        matching_values['Size'] = feature.find('span', {"class": "value"}).text.replace('\n', "")
    
                descriptions = str(matching_values['Description']).split('\n')
    
                if len(descriptions) > 0:
                    matching_values['Composition'] = descriptions[0]
                    print(descriptions[0])
            except:
                matching_values['Composition'] = None
                matching_values['Size'] = None
    
            return matching_values