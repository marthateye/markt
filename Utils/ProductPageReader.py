from Utils.WebScrapper import WebScrapper
from DB.ProductDBModelAdapter import ProductDBModelAdapter

class ProductPageReader:
    def get_prop_values(self,base_product,target_elements,keywords,adapter,product_db_adapter):
        web_scrapper = WebScrapper()
        html_markup = web_scrapper.get_html_markup_with_header(base_product['Link'])

        matching_products = base_product
        is_match = False
        for props in target_elements:
            try:
                value = html_markup.find(props.element_tag, props.attributes).text.replace('\n', "")
                print('searching for {}, found => value={}'.format(props.meta, value))

                for keyword in keywords:
                    if keyword.lower() in value.lower():
                        is_match = True

            except:
                try:
                    value = html_markup.find(props.element_tag, props.attributes)
                except:
                    value = None

            matching_products[props.meta] = value

        if is_match == False:
            return None


        product_info = adapter.run_custom_prop_values(html_markup,matching_products)
        print('match found')
        print(product_info)

        if product_db_adapter.merge_products(product_info) :
            print('INFO MERGED!')

        return product_info