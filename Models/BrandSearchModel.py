class BrandSearchModel:
    def __init__(self, brand,keywords,url=None):
        self._brand = brand
        self._keywords = keywords
        self._url = url

    def get_brand(self):
        return self._brand

    def set_brand(self, value):
        self._brand = value

    def get_keywords(self):
        return self._keywords

    def set_keywords(self, value):
        self._keywords = value

    def get_url(self):
        return self._url

    def set_url(self, value):
        self._url = value

    brand_name = property(get_brand, set_brand)
    keywords = property(get_keywords, set_keywords)
    url = property(get_url,set_url)