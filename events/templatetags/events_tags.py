from django import template

from projects2 import utils

register = template.Library()


@register.simple_tag
def get_project_year_field_list(project_year):
    try:
        return utils.get_project_year_field_list(project_year)
    except Exception as e:
        return []


@register.simple_tag
def get_staff_field_list():
    try:
        return utils.get_staff_field_list()
    except Exception as e:
        print(e)
        return []


@register.simple_tag
def get_om_field_list():
    try:
        return utils.get_om_field_list()
    except Exception as e:
        print(e)
        return []


@register.simple_tag
def get_capital_field_list():
    try:
        return utils.get_capital_field_list()
    except Exception as e:
        print(e)
        return []


@register.simple_tag
def get_activity_field_list():
    try:
        return utils.get_activity_field_list()
    except Exception as e:
        print(e)
        return []


@register.simple_tag
def get_collaboration_field_list():
    try:
        return utils.get_collaboration_field_list()
    except Exception as e:
        print(e)
        return []


@register.simple_tag
def get_status_report_field_list():
    try:
        return utils.get_status_report_field_list()
    except Exception as e:
        print(e)
        return []


@register.simple_tag
def get_activity_update_field_list():
    try:
        return utils.get_activity_update_field_list()
    except Exception as e:
        print(e)
        return []


@register.simple_tag
def get_file_field_list():
    try:
        return utils.get_file_field_list()
    except Exception as e:
        print(e)
        return []


@register.simple_tag
def get_citations_field_list():
    try:
        return utils.get_citation_field_list()
    except Exception as e:
        print(e)
        return []
