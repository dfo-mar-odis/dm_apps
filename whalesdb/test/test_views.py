from django.test import tag
from django.urls import reverse_lazy
from django.utils.translation import activate

from whalesdb.test.common_views import CommonTest


###########################################################################################
# Index View is a bit different from most views as it is basically just a landing page
###########################################################################################
class TestIndexView(CommonTest):

    def setUp(self):
        super().setUp()

        self.test_url = reverse_lazy('whalesdb:index')
        self.test_expected_template = 'whalesdb/index.html'

    # Users should be able to view the whalesdb index page which corresponds to the whalesdb/index.html template
    @tag('index_view', 'response', 'access')
    def test_index_view_en(self):
        super().assert_view()

    # Users should be able to view the whalesdb index page corresponding to the whalesdb/index.html template, in French
    @tag('index_view', 'response', 'access')
    def test_index_view_fr(self):
        super().assert_view(lang='fr')

    # The index view should return a context to be used on the index.html template
    # this should consist of a "Sections" dictionary containing sub-sections
    @tag('index_view', 'context')
    def test_index_view_context(self):
        activate('en')

        response = self.client.get(self.test_url)

        # expected to determine if the user is authorized to add content
        self.assertIn("auth", response.context)
