class ProductTagProps:
    def __init__(self, meta,ele,attr):
        self._meta = meta
        self._element_tag = ele
        self._attributes = attr

    def get_meta(self):
        return self._meta

    def set_meta(self, value):
        self._meta = value

    def get_element_tag(self):
        return self._element_tag

    def set_element_tag(self, value):
        self._element_tag = value

    def get_attributes(self):
        return self._attributes

    def set_attributes(self, value):
        self._attributes = value

    meta = property(get_meta, set_meta)
    element_tag = property(get_element_tag, set_element_tag)
    attributes = property(get_attributes, set_attributes)