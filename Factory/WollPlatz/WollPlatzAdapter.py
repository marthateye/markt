from Models.ProductTagProps import ProductTagProps
from Models.ProductMeta import ProductMeta
from Models.BrandSearchModel import BrandSearchModel
from Utils.WebScrapper import WebScrapper
from Utils.ProductPageReader import ProductPageReader
from DB.ProductDBModelAdapter import ProductDBModelAdapter


def set_brand_params():
    brand_params = [BrandSearchModel('DMC', ['Natura XL']),
                    BrandSearchModel('Drops', ['Safran', 'Baby Merino Mix']),
                    BrandSearchModel('Stylecraft', ['Special DK'])]

    return brand_params


def set_props():
    target_element_properties = [ProductTagProps('Name', 'h1', {"id" : "pageheadertitle"}),
                                 ProductTagProps('Price', 'span', {"class": "product-price-amount"}),
                                 ProductTagProps('Currency','span',{"class": "product-price-currency"})]
    return target_element_properties


class WollPLatzAdapter:
    def __init__(self):
        self.brand_search_params = set_brand_params()
        self.target_element_properties = set_props()
        self.brand_url = 'https://www.wollplatz.de/wolle/{}?page={}'
        self.max_pages = 10
        self.results_per_page = 24
        self.store = "WollPlatz"

    def read_website_info(self):

        web_scrapper = WebScrapper()
        product_page_reader = ProductPageReader()
        product_db_adapter = ProductDBModelAdapter()

        products = []

        for brand_meta in self.brand_search_params:
            is_page_complete = False
            starting_page = 1

            while is_page_complete == False:
                target_url = self.brand_url.format(brand_meta.brand_name, starting_page)
                html_markup = web_scrapper.get_html_markup(target_url)

                print('Scrapping brand ({}) from {} , on Page = {}'.format(brand_meta.brand_name,target_url,starting_page))

                # read products
                product_list = html_markup.find_all("div", {"class": "productlistholder"})
                print('{} products found'.format(len(product_list)))
                for product in product_list:
                    product_name = product.find("h3", {"class": "productlist-title"}).text.replace('\n', "")

                    selected_keyword = None

                    is_match = False
                    for keyword in brand_meta.keywords:
                        if keyword.lower() in product_name.lower():
                            is_match = True
                            selected_keyword = keyword
                            break

                    if is_match == False:
                        continue

                    link = product.find("a", {"class": "productlist-imgholder"}).get('href')
                    image = product.find("img", {}).get('data-src')

                    base_product = dict(Store=self.store, Brand=brand_meta.brand_name, Link=link,
                                        Image = image, ShortName = product_name,Keyword=selected_keyword)

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

            gdp_table = html_markup.find("div", {"id": "pdetailTableSpecs"})
            table = gdp_table.find('table', {})
            gdp_table_data = table.find_all("tr")

            for table_row in gdp_table_data:
                columns = table_row.find_all("td")
                column_title = columns[0].text.lower()
                if 'nadelstärke' in column_title:
                    print(column_title)
                    matching_values['Size'] = columns[1].text.replace('\n', "")
                if 'zusammenstellung' in column_title:
                    print(column_title)
                    matching_values['Composition'] = columns[1].text.replace('\n', "")

        except:
            matching_values['Composition'] = None
            matching_values['Size'] = None

        return matching_values