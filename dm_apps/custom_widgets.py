from django.db import models
from django.forms import TextInput


class OracleTextField(models.TextField):
    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.oracle':
            return 'NVARCHAR2(2000)'
        else:
            return super().db_type(connection)


class SelectAdd(TextInput):
    def __init__(self, data_list, name, *args, **kwargs):
        super(SelectAdd, self).__init__(*args, **kwargs)
        self._name = name
        self._list = data_list
        self.attrs.update({'list': 'list__%s' % self._name})

    def render(self, name, value, attrs=None, renderer=None):
        text_html = super(SelectAdd, self).render(name, value, attrs=attrs)
        data_list = '<datalist id="list__%s">' % self._name
        for item in self._list:
            data_list += '<option value="%s">' % item
        data_list += '</datalist>'

        return "{}{}".format(text_html, data_list)