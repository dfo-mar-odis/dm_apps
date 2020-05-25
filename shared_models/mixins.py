from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _


class CommonMixin():
    '''
    This is a mixin for all the variables and tools that we expect to have in view
    This should be called after a View class, if possible
    '''

    # key is used to construct commonly formatted strings, such as used in the get_success_url
    key = None

    # title to display on the CreateView page either this var or the h1 var is required
    title = None

    # an extending class can override this similarly to how the template_name attribute can be overriden
    # Except in this case the value will be used to include a java_script file at the bottom of the
    # 'shared_models/shared_entry_form.html' template
    java_script = None

    # an extending class can override this similarly to how the template_name attribute can be overriden
    # Except in this case the value will be used to include a nav_menu file at the top of the
    # 'shared_models/shared_entry_form.html' template
    nav_menu = None

    # an extending class can override this similarly to how the template_name attribute can be overriden
    # Except in this case the value will be used to include a site_css file at the top of the
    # 'shared_models/shared_entry_form.html' template
    site_css = None

    # an extending class can override this similarly to how the template_name attribute can be overriden
    # Except in this case the value will be used to include a field_list in the context var

    # These are for testing purposes only
    auth = True

    # this should be overriden in an extending class to determine if a user is authorized to do certain actions
    def test_func(self):
        return self.auth

    # this is a list of fields used for describing the context variable called 'object'
    field_list = None

    # This is a subtitle that will be appended to the title of the webpage tab in the browser. e.g., Title - subtitle
    subtitle = None

    # title h1
    h1 = None
    # title h2
    h2 = None
    # title h3
    h3 = None

    # stuff for breadcrumbs
    #########################
    # should be a simple string
    active_page_name_crumb = None
    # should be a dictionary in the following format {"title": my_title, "url": my_url }
    parent_crumb = None
    # should be a dictionary in the following format {"title": my_title, "url": my_url }
    grandparent_crumb = None
    # should be a dictionary in the following format {"title": my_title, "url": my_url }
    greatgrandparent_crumb = None
    # should be a dictionary in the following format {"title": my_title, "url": my_url }
    root_crumb = None
    # this can be used in the case of simple breadcrumbs where we are just going from index > active page; this will override anything provided in the root_crumb var
    home_url_name = None

    container_class = "container"

    def get_title(self):
        return self.title

    # Can be overriden in the extending class to do things based on the kwargs passed in from get_context_data
    def get_java_script(self):
        return self.java_script

    # Can be overriden in the extending class to do things based on the kwargs passed in from get_context_data
    def get_nav_menu(self):
        return self.nav_menu

    # Can be overriden in the extending class to do things based on the kwargs passed in from get_context_data
    def get_site_css(self):
        return self.site_css

    def get_auth(self):
        return self.auth

    # Can be overriden in the extending class to do things based on the kwargs passed in from get_context_data
    def get_field_list(self):
        return self.field_list

    def get_subtitle(self):
        return self.subtitle

    def get_h1(self):
        return self.h1

    def get_h2(self):
        return self.h2

    def get_h3(self):
        return self.h3

    def get_active_page_name_crumb(self):
        return self.active_page_name_crumb

    def get_parent_crumb(self):
        return self.parent_crumb

    def get_grandparent_crumb(self):
        return self.grandparent_crumb

    def get_greatgrandparent_crumb(self):
        return self.greatgrandparent_crumb

    def get_root_crumb(self):
        return self.root_crumb

    def get_crumbs(self):
        """
        Certain templates expect a context variable called crumbs the structure of this var is a list of dicts.
        Each dict has a title and url except the active crumb which only needs a title'''
        """

        root = self.get_root_crumb()
        greatgrandparent = self.get_greatgrandparent_crumb()
        grandparent = self.get_grandparent_crumb()
        parent = self.get_parent_crumb()
        active_page_name = self.get_active_page_name_crumb()

        # if there is not an active page, we will take either the h1 or title or subtitle if available
        if not active_page_name:
            if self.get_h1():
                active_page_name = self.get_h1()
            elif self.get_title():
                active_page_name = self.get_title()
            elif self.get_subtitle():
                active_page_name = self.get_subtitle()

        # if there is still no active page name, we are out of business: no crumbs
        if active_page_name:
            crumbs = list()

            # first see if there is a home_url_name
            if self.home_url_name:
                crumbs.append({"title": _("Home"), "url": reverse(self.home_url_name)})

            elif root:
                crumbs.append(root)

            if greatgrandparent:
                crumbs.append(greatgrandparent)

            if grandparent:
                crumbs.append(grandparent)

            if parent:
                crumbs.append(parent)

            crumbs.append({"title": active_page_name})
            return crumbs

    def get_container_class(self):
        return self.container_class

    def get_common_context(self) -> dict:
        context = dict()

        title = self.get_title()
        h1 = self.get_h1()

        if not title and not h1:
            raise AttributeError("No title or h1 attribute set in the class extending CommonMixin")

        if title:
            context['title'] = title

        if h1:
            context['h1'] = h1

        java_script = self.get_java_script()
        nav_menu = self.get_nav_menu()
        site_css = self.get_site_css()
        context["auth"] = self.get_auth()

        field_list = self.get_field_list()
        h2 = self.get_h2()
        h3 = self.get_h3()
        subtitle = self.get_subtitle()
        crumbs = self.get_crumbs()
        container_class = self.get_container_class()

        if java_script:
            context['java_script'] = java_script

        if nav_menu:
            context['nav_menu'] = nav_menu

        if site_css:
            context['site_css'] = site_css

        if field_list:
            context['field_list'] = field_list

        if subtitle:
            context['subtitle'] = subtitle
        # if there is no subtitle, use the h1 as a default
        elif self.get_crumbs():
            context['subtitle'] = self.get_crumbs()[-1].get("title")
        elif h1:
            context['subtitle'] = h1
        elif title:
            context['subtitle'] = title

        if h1:
            context['h1'] = h1

        if h2:
            context['h2'] = h2

        if h3:
            context['h3'] = h3

        if crumbs:
            context['crumbs'] = crumbs

        context['container_class'] = container_class

        return context


class CommonFormMixin(CommonMixin):
    auth = True
    cancel_url = None
    cancel_text = _("Back")
    submit_text = _("Submit")
    editable = True

    def get_cancel_url(self):
        if self.cancel_url:
            return self.cancel_url
        elif self.parent_crumb:
            return self.parent_crumb.get("url")
        elif self.home_url_name:
            return reverse(self.home_url_name)
        else:
            return self.request.META.get('HTTP_REFERER')

    def get_cancel_text(self):
        return self.cancel_text

    def get_submit_text(self):
        return self.submit_text

    def get_editable(self):
        return self.editable

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        # if there is no success url provided, a reasonable guess would be to go back to the parent url
        elif self.parent_crumb:
            return self.parent_crumb.get("url")

    def get_common_context(self):
        context = super().get_common_context()
        context['cancel_url'] = self.get_cancel_url()
        context['cancel_text'] = self.get_cancel_text()
        context['submit_text'] = self.get_submit_text()
        context['editable'] = self.get_editable()
        return context


class CommonPopoutFormMixin(CommonFormMixin):
    '''
    This can be added to a FormView (+Update, Create, Delete etc...) if you want to make it a popout
    NOTE: This should come before the View class in order to work properly
    '''
    width = 900
    height = 650
    success_url = None
    template_name = 'shared_models/generic_popout_form.html'

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        else:
            return reverse_lazy("shared_models:close_me")

    def get_common_context(self):
        context = super().get_common_context()
        # set the width and the height of the popout form
        context['width'] = self.width
        context['height'] = self.height
        return context


class CommonListMixin(CommonMixin):
    # the url to the corresponding CreateView for the same model object
    new_object_url = None
    # the url name to the corresponding CreateView for the same model object. This can be used in the simple scenario where there are no kwargs
    new_object_url_name = None
    # the url name to the corresponding DetailView for the same model object. The assuption is that there will be a kwarg called "pk"
    row_object_url_name = None
    # an optional random object used to populate the table header of the list view
    random_object = None

    def get_row_object_url_name(self):
        return self.row_object_url_name

    def get_new_object_url_name(self):
        return self.new_object_url_name

    def get_new_object_url(self):
        """
        This function is utlimately was provisions the context with the new object url.
        It will prioritize a new object url name over a new object url.
        """
        new_object_url_name = self.get_new_object_url_name()
        if new_object_url_name:
            return reverse_lazy(new_object_url_name)
        else:
            return self.new_object_url

    def get_random_object(self):
        if self.random_object:
            return self.random_object
        else:
            return self.get_queryset().model.objects.first()

    def get_common_context(self):
        context = super().get_common_context()
        context["paginate_by"] = self.paginate_by # this is coming from ListView but we are putting it into context variable
        context["random_object"] = self.get_random_object()
        context["row_object_url_name"] = self.get_row_object_url_name()
        context["new_object_url"] = self.get_new_object_url()
        context["random_object"] = self.get_random_object()
        return context
