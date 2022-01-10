class ProductMeta:
    def __init__(self,kwargs):
        self._name = kwargs.get('name','')
        self._short_name = kwargs.get('short_name', '')
        self._brand = kwargs.get('brand','')
        self._price = kwargs.get('price','')
        self._currency = kwargs.get('currency', '')
        self._delivery_time = kwargs.get('delivery_time','unknown')
        self._size = kwargs.get('size','')
        self._composition = kwargs.get('composition','')

    def get_name(self):
        return self._name

    def set_name(self, value):
        self._name = value

    def get_short_name(self):
        return self._short_name

    def set_short_name(self, value):
        self._short_name = value

    def get_brand(self):
        return self._brand

    def set_brand(self, value):
        self._brand = value

    def get_price(self):
        return self._price

    def set_price(self, value):
        self._price = value

    def get_currency(self):
        return self._currency

    def set_currency(self, value):
        self._currency = value

    def get_delivery_time(self):
        return self._delivery_time

    def set_delivery_time(self, value):
        self._delivery_time = value

    def get_size(self):
        return self._size

    def set_size(self, value):
        self._size = value

    def get_composition(self):
        return self._composition

    def set_composition(self, value):
        self._composition = value

    name = property(get_name,set_name)
    short_name = property(get_short_name,set_short_name)
    brand = property(get_brand, set_brand)
    price = property(get_price, set_price)
    currency = property(get_currency,set_currency)
    delivery_time = property(get_delivery_time, set_delivery_time)
    size = property(get_size, set_size)
    composition = property(get_composition, set_composition)