from collections import OrderedDict

from django.conf import settings
from django.urls import reverse, NoReverseMatch
from django.views.generic import TemplateView
from django.utils.translation import gettext as _
from accounts.models import Announcement


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
        app_dict["inventory"] = {
            "title": _("Metadata Inventory"),
            "description": _("Tool for organizing and managing regional data resources."),
            "status": "production",
            "access": "open",
            "url": reverse('inventory:index'),
            "icon_path": 'img/icons/research.svg',
            "region": "all",

        }
    except NoReverseMatch:
        pass

    if settings.SHOW_TICKETING_APP:
        try:
            app_dict["tickets"] = {
                "title": _("Data Management Tickets"),
                "description": _("Submit and track data management service requests."),
                "status": "production",
                "access": "open",
                "url": reverse('tickets:router'),
                "icon_path": 'img/icons/flowchart.svg',
                "region": "all",
            }
        except NoReverseMatch:
            pass

    try:
        app_dict["travel"] = {
            "title": _("Travel Management System"),
            "description": _("Management tool to facilitate regional and national travel pre-approvals."),
            "status": "production",
            "access": "permission-required",
            "url": reverse('travel:index'),
            "icon_path": 'img/icons/paper-plane.svg',
            "region": "all",
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
        app_dict["grais"] = {
            "title": _("grAIS"),
            "description": _("Gulf Region Aquatic Invasive Species data entry and archiving tool."),
            "status": "production",
            "access": "permission-required",
            "url": reverse('grais:index'),
            "icon_path": 'img/icons/starfish.svg',
            "region": "regional",
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
            "region": "regional",
        }
    except NoReverseMatch:
        pass

    try:
        app_dict["ihub"] = {
            "title": _("iHub"),
            "description": _("Indigenous Hub entry management and reporting tool."),
            "status": "production",
            "access": "permission-required",
            "url": reverse('ihub:index'),
            "icon_path": 'img/icons/network.svg',
            "region": "regional",
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
            "icon_path": 'img/icons/seine.svg',
            "region": "regional",
        }
    except NoReverseMatch:
        pass

    try:
        app_dict["scifi"] = {
            "title": _("SciFi"),
            "description": _("Gulf Science finance tracking and reporting tool."),
            "status": "production",
            "access": "permission-required",
            "url": reverse('scifi:index'),
            "icon_path": 'img/icons/money1.svg',
            "region": "all",
        }
    except NoReverseMatch:
        pass

    try:
        app_dict["spring_cleanup"] = {
            "title": _("GFC Spring Cleanup!"),
            "description": _("App to coordinate a spring cleanup in the area around the GFC. Sign up today!!."),
            "status": "dev",
            "access": "permission-required",
            "url": reverse('spring_cleanup:index'),
            "icon_path": 'img/icons/earth.svg',
            "region": "regional",
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
            "region": "regional",
        }
    except NoReverseMatch:
        pass

    try:
        app_dict["diets"] = {
            "title": _("Marine Diets"),
            "description": _("Stomach contents analysis database / application."),
            "status": "production",
            "access": "permission-required",
            "url": reverse('diets:index'),
            "icon_path": 'img/icons/fork.svg',
            "region": "regional",
        }
    except NoReverseMatch:
        pass

    try:
        app_dict["shiny"] = {
            "title": _("R Shiny Apps"),
            "description": _("Collection of Shiny Apps hosted on the DM Apps server"),
            "status": "production",
            "access": "permission-required",
            "url": reverse('shiny:index'),
            "icon_path": 'img/icons/rproj.png',
            "region": "regional",
        }
    except NoReverseMatch:
        pass

    try:
        app_dict["trapnet"] = {
            "title": _("TrapNet"),
            "description": _("Diadromous Data Entry Tool."),
            "status": "beta",
            "access": "login-required",
            "url": reverse('trapnet:index'),
            "icon_path": 'img/icons/river.svg',
            "region": "regional",
        }
    except NoReverseMatch:
        pass

    try:
        app_dict["ios2"] = {
            "title": _("IOS Instrument Tracking"),
            "description": _("IOS Instrument Tracking Application."),
            "status": "dev",
            "access": "permission-required",
            "url": reverse('ios2:index'),
            "icon_path": 'img/icons/sailor.svg',
            "region": "regional",
        }
    except NoReverseMatch:
        pass

    try:
        app_dict["publications"] = {
            "title": _("Project Inventory"),
            "description": _("Tools for viewing information on completed projects"),
            "status": "dev",
            "access": "login-required",
            "url": reverse('publications:index'),
            "icon_path": 'img/icons/publications.svg',
            "region": "regional",
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
            "region": "regional",
        }
    except NoReverseMatch:
        pass

    try:
        app_dict["sar_search"] = {
            "title": _("SAR Search"),
            "description": _("Species at Risk Search Tool."),
            "status": "dev",
            "access": "login-required",
            "url": reverse('sar_search:index'),
            "icon_path": 'img/icons/beetle.svg',
            "region": "regional",
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
            "region": "regional",
        }
    except NoReverseMatch:
        pass

    try:
        app_dict["whalesdb"] = {
            "title": _("Whale Equipment Deployment Inventory"),
            "description": _("Tool for managing whale equipment, deployments and recordings."),
            "status": "dev",
            "access": "login-required",
            "url": reverse('whalesdb:index'),
            "icon_path": 'img/whalesdb/whales_dark.svg',
            "region": "regional",
        }
    except NoReverseMatch:
        pass

    try:
        app_dict["csas"] = {
            "title": _("Canadian Science Advisory Secretariat"),
            "description": _("Tool for tracking meetings, requests and publications."),
            "status": "dev",
            "access": "login-required",
            "url": reverse('csas:index'),
            "icon_path": 'img/csas/csas_image.svg',
            "region": "regional",
        }
    except NoReverseMatch:
        pass

    try:
        app_dict["vault"] = {
            "title": _("Megafauna media vault"),
            "description": _("Media vault for marine megafauna."),
            "status": "production",
            "access": "permission-required",
            "url": reverse('vault:index'),
            "icon_path": 'img/icons/vault.svg',
            "region": "regional",
        }
    except NoReverseMatch:
        pass

    try:
        app_dict["necropsy"] = {
            "title": _("Necropsy Tools and Marine Mammal Inventory"),
            "description": _("Tools for necropsies and inventory of marine mammal equipment"),
            "status": "production",
            "access": "permission-required",
            "url": reverse('necropsy:index'),
            "icon_path": 'img/icons/necropsy.svg',
            "region": "regional",
        }
    except NoReverseMatch:
        pass

    try:
        app_dict["spot"] = {
            "title": _("Grants & Contributions"),
            "description": _("Gulf Region application for the tracking of Gs & Cs."),
            "status": "beta",
            "access": "permission-required",
            "url": reverse('spot:index'),
            "icon_path": 'img/icons/agreement.svg',
            "region": "regional",
        }
    except NoReverseMatch:
        pass
    #
    # try:
    #     app_dict["masterlist"] = {
    #         "title": _("MasterList"),
    #         "description": _("Regional master list and consultation instructions."),
    #         "status": "dev",
    #         "access": "permission-required",
    #         "url": reverse('masterlist:index'),
    #         "icon_path": 'img/icons/connection.svg',
    #         "region": "regional",
    #     }
    # except NoReverseMatch:
    #     pass

    return OrderedDict(app_dict)


class IndexView(TemplateView):
    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        # messages.info(request,
        #               mark_safe(_("Please note that this site is only intended for the storage of <b>unclassified information</b>.")))
        # messages.warning(request,
        #               mark_safe(_("<b>On Friday January 10, 2020 at 12pm AST, the site will be down for a few hours for scheduled maintenance. Sorry for any inconvenience.</b>")))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        app_odict = get_app_dict(self.request)
        app_dict_shared = OrderedDict()
        app_dict_regional = OrderedDict()
        for key in app_odict:
            if app_odict[key]["region"] == "all":
                app_dict_shared[key] = app_odict[key]

            if app_odict[key]["region"] == "regional":
                app_dict_regional[key] = app_odict[key]

        context["app_dict_shared"] = app_dict_shared
        context["app_dict_regional"] = app_dict_regional
        context["app_dict"] = app_odict
        context["announcements"] = [a for a in Announcement.objects.all() if a.is_current]
        if settings.DEVOPS_BUILD_NUMBER and settings.DEVOPS_BUILD_NUMBER != "":
            context["build_number"] = settings.DEVOPS_BUILD_NUMBER
        return context

