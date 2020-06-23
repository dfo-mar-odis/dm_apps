from django import template
from django.conf import settings
from django.core.exceptions import FieldDoesNotExist
from django.template.defaultfilters import yesno
from django.utils.safestring import SafeString, mark_safe
from django.utils.translation import gettext_lazy as _

import markdown

from lib.templatetags.custom_filters import tohtml

register = template.Library()


@register.simple_tag
def get_verbose_label(instance, field_name):
    """
    :param instance: an instance of a model
    :param field_name: string of a field name, property name etc.
    :return: a label for that field

    Returns verbose_name for a field. This function is used directly in some instances however it is often called by `verbose_field_display`
    or `verbose_td_display`.

    Custom labels can be provided as such: "first_name|The user's first name". If there is a custom label, this portion of the string is
    simply returned by the function

    To return a label from a foreign key, send in the field name as such: "user.first_name".

    If a model property is received without a custom label, this function will just return the property name being passed in"
    """

    def __special_capitalize__(raw_string):
        """ Little dance to make sure the first letter is capitalized.
        Do not want to use the capitalize() method since it makes the remaining portion of str lowercase. This is problematic in
         cases like: `DFO employee` since that would become `Dfo employee`"""
        first_letter = raw_string[0].upper()
        str_list = list(raw_string)
        str_list[0] = first_letter
        raw_string = "".join(str_list)
        return raw_string

    # 2019/04/03 - P. Upson
    # Added a test to see if the instance is 'null'. I was getting an issue on the diets/cruises page
    # during the get_verbose_label method due to the instance being passed in here being "None"
    # if the instance is null this method will return null.
    if instance is None:
        return None

    # at the end of the day, if the user is sending in a custom label, our work is done.
    elif len(field_name.split("|")) > 1:
        verbose_name = _(str(field_name.split("|")[1]))

    # check to see if there were any arguments passed in with the field name
    # this means the field is a foreign key so we will need to separate the first part preceding the "."
    elif len(field_name.split(".")) > 1:
        field_name = field_name.split(".")[0]
        field_instance = instance._meta.get_field(field_name)
        verbose_name = field_instance.verbose_name

    else:
        # try grabbing the instance of that field...
        try:
            field_instance = instance._meta.get_field(field_name)
        except FieldDoesNotExist:
            # if it does not exist, perhaps we are receiving a model prop (with no custom label)
            # in which case, the verbose name will in is the same as the field_name..
            verbose_name = field_name
        else:
            try:
                verbose_name = field_instance.verbose_name
            except AttributeError:
                # if there is no verbose_name attribute, just send back the field name
                verbose_name = field_name
    return mark_safe(__special_capitalize__(verbose_name))


@register.simple_tag
def get_field_value(instance, field_name, format=None, display_time=False, hyperlink=None, nullmark="---", date_format="%Y-%m-%d",
                    safe=False):
    """
    :param instance: an instance of a model
    :param field_name: string of a field name, property name etc.
    :param format: a string of formatting trigger words [currency, html]
    :param display_time: Should the time be displayed as well as the date? This arg is moot if a date_format string is provided
    :param hyperlink: True / False about whether the resulting value is a hyperlink
    :param nullmark: specify a string to return if value is null
    :param date_format: the formatting string of a DateTime object
    :param safe: should the resulting value be returned as a safestring?
    :return: field value

    Returns verbose_name for a field. This function is used directly in some instances however it is often called by `verbose_field_display`
    or `verbose_td_display`.

    To return a field value from a foreign key, send in the field name as such: "user.first_name".

    To return a value from a model prop, simply send in the field name as such: "my_model_prop". Effectively there is no different
    between entering a prop and a real field.
    """


    # first, if there is no instance, we cannot return anything intelligable
    if instance is None:
        return None

    #  next, let's see if it is field in another table that we are trying to access (e.g. user.first_name
    elif len(field_name.split(".")) > 1:
        arg = field_name.split(".")[1]
        field_name = field_name.split(".")[0]
        try:
            field_value = getattr(getattr(instance, field_name), arg)
        except AttributeError:
            # there is no value and therefore the getattr function fails..
            field_value = nullmark
    else:
        # if there is a custom label, we need to shed it.
        if len(field_name.split("|")) > 1:
            # overwrite the field_name arg with the first part of the string
            field_name = field_name.split("|")[0]

        try:
            field_instance = instance._meta.get_field(field_name)
        except FieldDoesNotExist:
            # perhaps it is a model property
            try:
                field_value = getattr(instance, field_name)
            except AttributeError:
                if settings.DB_MODE == "DEV":
                    print(f"Could not evaluate field value for '{field_name} for object {type(instance)}")
        else:

            # first check if there is a value :
            if getattr(instance, field_name) is not None and getattr(instance, field_name) != "":
                # check to see if it is a many to many field
                if field_instance.get_internal_type() == 'ManyToManyField' or field_instance.get_internal_type() == 'ManyToManyRel':
                    m2m = getattr(instance, field_name)
                    field_value = str([str(field) for field in m2m.all()]).replace("[", "").replace("]", "").replace("'",
                                                                                                                     "").replace(
                        '"', "")

                # check to see if there are choices
                elif len(field_instance.choices) > 0:
                    field_value = getattr(instance, "get_{}_display".format(field_name))()

                # check to see if it is a datefield
                elif field_instance.get_internal_type() == 'DateTimeField':
                    if not date_format:
                        date_format = "%Y-%m-%d"
                    datetime_obj = getattr(instance, field_name)
                    if display_time:
                        field_value = datetime_obj.strftime('{} %H:%M'.format(date_format))
                    else:
                        field_value = datetime_obj.strftime(date_format)

                # check to see if it is a url
                elif str(getattr(instance, field_name)).startswith("http"):
                    field_value = '<a href="{url}" target="_blank">{url}</a>'.format(url=getattr(instance, field_name))

                # check to see if it is a BooleanField
                elif field_instance.get_internal_type() == 'BooleanField' or field_instance.get_internal_type() == 'NullBooleanField':
                    field_value = yesno(getattr(instance, field_name), "Yes,No,Unknown")

                # check to see if hyperlink was provided
                elif hyperlink:
                    field_value = mark_safe('<a href="{}">{}</a>'.format(hyperlink, getattr(instance, field_name)))
                else:
                    field_value = getattr(instance, field_name)
            else:
                field_value = nullmark

    # handle some of the formatting
    if "currency" in str(format).lower():
        try:
            field_value = '${:,.2f}'.format(float(field_value))
        except:
            pass
    try:
        field_value = markdown.markdown(field_value) if "html" in str(format).lower() else field_value
        field_value = mark_safe(field_value) if safe else field_value
    except UnboundLocalError:
        field_value = nullmark
    return field_value


@register.simple_tag
def verbose_field_display(instance, field_name, format=None, display_time=False, hyperlink=None, date_format=None):
    """
    Returns a standard display block for a field based on the verbose fieldname
    """

    # call on the get_verbose_label func to handle label prep
    verbose_name = get_verbose_label(instance, field_name)

    # call on the get_field_value func to handle field value prep
    field_value = get_field_value(instance, field_name, format=format, display_time=display_time, date_format=date_format, hyperlink=hyperlink)

    # if url and field_value != "n/a":
    #     html_block = '<p><span class="label">{}:</span><br><a href="{}">{}</a></p>'.format(verbose_name, url, field_value)
    # else:
    html_block = '<p><span class="label">{}:</span><br>{}</p>'.format(verbose_name, field_value)

    return SafeString(html_block)


@register.simple_tag
def verbose_td_display(instance, field_name, format=None, display_time=False, url=None, date_format=None, nullmark="---", th_width=None,
                       td_width=None, to_html=False):
    """
    returns a table row <tr> with a <td> for the label and a <td> for the value. Call this from within a <table>
    """
    # call on the get_verbose_label func to handle label prep
    verbose_name = get_verbose_label(instance, field_name)

    # call on the get_field_value func to handle field value prep
    field_value = get_field_value(instance, field_name, format=format, display_time=display_time, date_format=date_format,
                                  nullmark=nullmark)

    if to_html:
        field_value = tohtml(field_value)

    th_tag_opener = '<th style="width: {};">'.format(th_width) if th_width else '<th>'
    td_tag_opener = '<td style="width: {};">'.format(td_width) if td_width else '<td>'

    if url and field_value != "n/a":
        html_block = f'<tr>{th_tag_opener}{verbose_name}</th>{td_tag_opener}<a href="{url}">{field_value}</a></td></tr>'
    else:
        html_block = '<tr>{}{}</th>{}{}</td></tr>'.format(th_tag_opener, verbose_name, td_tag_opener, field_value)
    return SafeString(html_block)



@register.filter
def model_verbose_name(instance):
    """send in a model object and it will send back out the verbose name of the model"""
    try:
        return type(instance)._meta.verbose_name
    except AttributeError:
        return "---"