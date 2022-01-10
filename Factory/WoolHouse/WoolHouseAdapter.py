from DB.ProductDBModelAdapter import ProductDBModelAdapter
from Models.ProductTagProps import ProductTagProps
#from Models.ProductMeta import ProductMeta
from Models.BrandSearchModel import BrandSearchModel
from Utils.WebScrapper import WebScrapper
from Utils.ProductPageReader import ProductPageReader


def set_brand_params():
    brand_params = [BrandSearchModel('DMC', ['Natura XL'], 'https://www.woolwarehouse.co.uk/yarn?brand_nav=46055&p={}'),
                    BrandSearchModel('Drops', ['Safran', 'Baby Merino'], 'https://www.woolwarehouse.co.uk/yarn?brand_nav=42172&p={}'),
                    BrandSearchModel('Stylecraft', ['Special DK'], 'https://www.woolwarehouse.co.uk/yarn?brand_nav=39432&p={}')]

    return brand_params


def set_props():
    target_element_properties = [ProductTagProps('Name', 'div',{"class": "product-name"}),
                                 ProductTagProps('Description', 'div', {"class": "std"}),
                                 ProductTagProps('Price', 'span', {"class": "gbp-price-value"})]
    return target_element_properties


class WoolHouseAdapter:
    def __init__(self):
        self.brand_search_params = set_brand_params()
        self.target_element_properties = set_props()
        self.max_pages = 10
        self.results_per_page = 12
        self.store = "WoolWareHouse"

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

                print('Scrapping brand ({}) from {} , on Page = {}'.format(brand_meta.brand_name, target_url,
                                                                           starting_page))

                # read products
                product_list = html_markup.find_all("li", {"class": "item"})
                print('{} products found'.format(len(product_list)))

                for product in product_list:

                    product_name = product.find("h2", {"class": "product-name"}).text.replace('\n', "")
                    selected_keyword = None

                    is_match = False
                    for keyword in brand_meta.keywords:
                        if keyword.lower() in product_name.lower():
                            is_match = True
                            selected_keyword = keyword
                            break

                    if is_match == False:
                        continue

                    link = product.find("a", {"class": "product-image"}).get('href')
                    image = product.find("img", {}).get('src')

                    base_product = dict(Store=self.store, Brand=brand_meta.brand_name, Link=link,
                                        Image=image, ShortName=product_name, Currency='£', Keyword=selected_keyword)

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
                else:
                    starting_page += 1

        return products

    def run_custom_prop_values(self, html_markup, matching_values):
        try:
            currency = str(matching_values['Currency'])

            if matching_values['Price'] != None:
                matching_values['Price'] = str(matching_values['Price']).replace(currency, '')

            gdp_table = html_markup.find("div", {"class": "product-info-table"})
            table = gdp_table.find('table', {"id": "product-attribute-specs-table"})
            gdp_table_data = table.find_all("tr")  # contains 2 rows

            for table_row in gdp_table_data:
                column_title = table_row.find('th', {}).text.lower()
                if 'size' in column_title:
                    print(column_title)
                    matching_values['Size'] = table_row.find('td', {}).text.replace('\n', "")
                if 'blend' in column_title:
                    print(column_title)
                    matching_values['Composition'] = table_row.find('td', {}).text.replace('\n', "")
        except:
            matching_values['Composition'] = None
            matching_values['Size'] = None

        print(matching_values)
        return matching_values