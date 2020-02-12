from django.db import models
from django.utils.translation import gettext_lazy as _


class Items(models.Model):
    unique_id = models.CharField(max_length=250, blank=False, null=False, verbose_name=_("Unique ID"))
    item_name = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Name of Item"))
    description = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Description"))
    owner = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Owner"))
    size = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Size (if applicable)"))
    container_space = models.IntegerField(null=True, blank=True, verbose_name=_("Container Space Available (if applicable)"))
    category = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Category"))
    type = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Type"))

    def __str__(self):
        return self.identifier_string

    def __str__(self):
        # check to see if a french value is given
        if getattr(self, str(_("name"))):

            return "{}".format(getattr(self, str(_("name"))))
        # if there is no translated term, just pull from the english field
        else:
            return "{}".format(self.name)

class Quantity(models.Model):
    items_quantity = models.ForeignKey(Items, on_delete=models.DO_NOTHING, related_name="items",
                      verbose_name=_("items"))
    unique_id = models.CharField(max_length=250, blank=True, null=True, verbose_name=_(""))
    serial_number = models.CharField(max_length=250, blank=True, null=True, verbose_name=_(""))
    quantity_oh = models.IntegerField(null=True, blank=True)
    quantity_oo = models.IntegerField(null=True, blank=True)
    last_audited = models.DateTimeField(blank=True, null=True)
    last_audited_by = models.CharField(max_length=250, blank=True, null=True, verbose_name=_(""))
    location_stored = models.CharField(max_length=250, blank=True, null=True, verbose_name=_(""))
    bin_id = models.CharField(max_length=250, blank=True, null=True, verbose_name=_(""))

class Supplier(models.Model):
    items_supplier = models.CharField(max_length=250, blank=True, null=True, verbose_name=_(""))
    supplier = models.CharField(max_length=250, blank=True, null=True, verbose_name=_(""))
    contact_number = models.CharField(max_length=250, blank=True, null=True, verbose_name=_(""))
    email = models.CharField(max_length=250, blank=True, null=True, verbose_name=_(""))
    last_invoice = models.CharField(max_length=250, blank=True, null=True, verbose_name=_(""))
    last_purchased = models.DateTimeField(blank=True, null=True)
    last_purchased_by = models.CharField(max_length=250, blank=True, null=True, verbose_name=_(""))

class Lending(models.Model):
    quantity_unique_id = models.ForeignKey(Quantity, on_delete=models.DO_NOTHING, related_name="items",
                      verbose_name=_("items"))
    quantity = models.IntegerField(null=True, blank=True)
    lent_to = models.CharField(max_length=250, blank=True, null=True, verbose_name=_(""))
    lent_date = models.DateTimeField(blank=True, null=True)




class Role(models.Model):
    name = models.CharField(max_length=255)
    nom = models.CharField(max_length=255, blank=True, null=True)


class Person(models.Model):
    first_name = models.CharField(max_length=250, blank=True, null=True, verbose_name=_(""))
    last_name = models.CharField(max_length=250, blank=True, null=True, verbose_name=_(""))
    organisation = models.CharField(max_length=250, blank=True, null=True, verbose_name=_(""))
    email = models.CharField(max_length=250, blank=True, null=True, verbose_name=_(""))
    # m2m
    roles = models.ManyToManyField(Role, verbose_name=_(""))


class MetadataField(models.Model):
    DATA_TYPE_CHOICES = (
        (1, _("integer/categorical")),
        (2, _("float")),
        (3, _("string")),
    )
    name = models.CharField(max_length=250, blank=True, null=True, verbose_name=_(""))
    nom = models.CharField(max_length=250, blank=True, null=True, verbose_name=_(""))
    description_eng = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("English description"))
    description_fra = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("French description"))
    data_type = models.IntegerField(choices=DATA_TYPE_CHOICES, verbose_name=_("data type"))


# used for defining metadata field categories, when applicable
