from collections import OrderedDict

from django.urls import reverse, NoReverseMatch
from django.views.generic import TemplateView
from django.utils.translation import gettext as _

# check to see if there is a user-defined local configuration file
# if there is, we we use this as our local configuration, otherwise we use the default
try:
    from . import my_conf as local_conf
except ModuleNotFoundError and ImportError:
    from . import default_conf as local_conf

try:
    SHOW_TICKETS_APP = local_conf.SHOW_TICKETS_APP
except AttributeError:
    SHOW_TICKETS_APP = True


# Create your views here.
def get_app_dict(request):
    """
    This function will go through and try to connect to all apps in the project. If an app is not available
    (i.e., raising a NoReverseMatch exception it will not be included in the OrderedDict
    each object in the OrderedDict will result in a card on the website's splash page

    :param request:
    :return: ordered dictionary containing all connected apps
    """

    app_dict = {}

    try:
        if request.user.is_authenticated:
            inventory_url = reverse('inventory:my_resource_list')
        else:
            inventory_url = reverse('inventory:resource_list')
        app_dict["inventory"] = {
            "title": _("Metadata Inventory"),
            "description": _("Tool for organizing and managing regional data resources."),
            "status": "production",
            "access": "open",
            "url": inventory_url,
            "icon_path": 'img/icons/research.svg',
            "region": "all",

        }
    except NoReverseMatch:
        pass

    if SHOW_TICKETS_APP:
        try:
            app_dict["tickets"] = {
                "title": _("Data Management Tickets"),
                "description": _("Submit and track data management service requests."),
                "status": "production",
                "access": "open",
                "url": reverse('tickets:router'),
                "icon_path": 'img/icons/tickets.svg',
                "region": "all",
            }
        except NoReverseMatch:
            pass

    try:
        app_dict["grais"] = {
            "title": _("grAIS"),
            "description": _("Gulf Region Aquatic Invasive Species data entry and archiving tool."),
            "status": "production",
            "access": "permission-required",
            "url": reverse('grais:index'),
            "icon_path": 'img/icons/starfish.svg',
            "region": "gulf",
        }
    except NoReverseMatch:
        pass

    try:
        app_dict["herring"] = {
            "title": _("HERmorrhage"),
            "description": _("The herring sampling and ageing application."),
            "status": "production",
            "access": "permission-required",
            "url": reverse('herring:index'),
            "icon_path": 'img/icons/fish.svg',
            "region": "gulf",
        }
    except NoReverseMatch:
        pass

    try:
        app_dict["ihub"] = {
            "title": _("iHub"),
            "description": _("Indigenous Hub entry management and reporting tool."),
            "status": "beta",
            "access": "permission-required",
            "url": reverse('ihub:index'),
            "icon_path": 'img/icons/network.svg',
            "region": "gulf",
        }
    except NoReverseMatch:
        pass

    try:
        app_dict["camp"] = {
            "title": _("CAMP db"),
            "description": _("Community Aquatic Monitoring Program (CAMP) data entry and archiving tool."),
            "status": "production",
            "access": "login-required",
            "url": reverse('camp:index'),
            "icon_path": 'img/icons/coral.svg',
            "region": "gulf",
        }
    except NoReverseMatch:
        pass

    try:
        app_dict["projects"] = {
            "title": _("Project Planning"),
            "description": _("Tool for the tracking, development and coordination of science project workplans."),
            "status": "production",
            "access": "login-required",
            "url": reverse('projects:index'),
            "icon_path": 'img/icons/scope.svg',
            "region": "all",
        }
    except NoReverseMatch:
        pass

    try:
        app_dict["scifi"] = {
            "title": _("SciFi"),
            "description": _("Gulf Science finance tracking and reporting tool."),
            "status": "beta",
            "access": "permission-required",
            "url": reverse('scifi:index'),
            "icon_path": 'img/icons/stats.svg',
            "region": "gulf",
        }
    except NoReverseMatch:
        pass

    try:
        app_dict["masterlist"] = {
            "title": _("MasterList"),
            "description": _("Regional master list and consultation instructions."),
            "status": "dev",
            "access": "permission-required",
            "url": reverse('masterlist:index'),
            "icon_path": 'img/icons/connection.svg',
            "region": "gulf",
        }
    except NoReverseMatch:
        pass

    try:
        app_dict["snowcrab"] = {
            "title": _("Snow Crab"),
            "description": _("front-end application for the Gulf snow crab monitoring dataset"),
            "status": "dev",
            "access": "open",
            "url": reverse('crab:index'),
            "icon_path": 'img/icons/crab.svg',
            "region": "gulf",
        }
    except NoReverseMatch:
        pass

    try:
        app_dict["oceanography"] = {
            "title": _("Oceanography"),
            "description": _("Collection, processing and storage of regional oceanographic data."),
            "status": "dev",
            "access": "open",
            "url": reverse('oceanography:index'),
            "icon_path": 'img/icons/boat.svg',
            "region": "gulf",
        }
    except NoReverseMatch:
        pass

    try:
        app_dict["diets"] = {
            "title": _("Marine Diets"),
            "description": _("Stomach contents analysis database / application."),
            "status": "beta",
            "access": "permission-required",
            "url": reverse('diets:index'),
            "icon_path": 'img/icons/fork.svg',
            "region": "gulf",
        }
    except NoReverseMatch:
        pass

    try:
        app_dict["shares"] = {
            "title": _("Gulf Shares"),
            "description": _("Administrative tool for managing gulf region shares."),
            "status": "production",
            "access": "permission-required",
            "url": reverse('shares:index'),
            "icon_path": 'img/icons/database.svg',
            "region": "gulf",
        }
    except NoReverseMatch:
        pass

    try:
        app_dict["travel"] = {
            "title": _("Travel Management System"),
            "description": _("Gulf region travel management tool."),
            "status": "beta",
            "access": "permission-required",
            "url": reverse('travel:index'),
            "icon_path": 'img/icons/paper-plane.svg',
            "region": "gulf",
        }
    except NoReverseMatch:
        pass

    try:
        app_dict["spot"] = {
            "title": _("Grants & Contributions"),
            "description": _("Gulf Region application for the tracking of Gs & Cs."),
            "status": "dev",
            "access": "permission-required",
            "url": reverse('spot:index'),
            "icon_path": 'img/icons/agreement.svg',
            "region": "gulf",
        }
    except NoReverseMatch:
        pass

    try:
        app_dict["publications"] = {
            "title": _("Project Publications Inventory"),
            "description": _("Tool for publishing and viewing publications related to completed projects."),
            "status": "dev",
            "access": "login-required",
            "url": reverse('publications:index'),
            "icon_path": 'img/icons/publications.svg',
            "region": "gulf",
        }
    except NoReverseMatch:
        pass

    try:
        app_dict["staff"] = {
            "title": _("Staff Planning Tool"),
            "description": _("Tool for staff planning."),
            "status": "dev",
            "access": "login-required",
            "url": reverse('staff:index'),
            "icon_path": 'img/icons/staff.svg',
            "region": "gulf",
        }
    except NoReverseMatch:
        pass

    return OrderedDict(app_dict)


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        app_odict = get_app_dict(self.request)
        app_dict_shared = OrderedDict()
        app_dict_gulf = OrderedDict()
        for key in app_odict:
            if app_odict[key]["region"] == "all":
                app_dict_shared[key] = app_odict[key]

            if app_odict[key]["region"] == "gulf":
                app_dict_gulf[key] = app_odict[key]


        context["app_dict_shared"] = app_dict_shared
        context["app_dict_gulf"] = app_dict_gulf
        return context
