from django.test import TestCase, tag

from whalesdb import forms


class TestMorForm(TestCase):
    valid_data = {
        "mor_name": "MOR_001",
        "mor_max_depth": "10",
        "mor_link_setup_image": "https://somelink.com/images/img001.png",
        "mor_additional_equipment": "None",
        "mor_general_moor_description": "This is a mooring description",
        "more_notes": "Notes",
    }

    @tag('mor_form', 'valid_data')
    def test_mor_valid_data(self):
        form = forms.MorForm(data=self.valid_data)
        form.is_valid()
        self.assertFalse(form.errors)


class TestStnForm(TestCase):
    valid_data = {
            "stn_name": "STN_001",
            "stn_code": "STN",
            "stn_revision": "1",
            "stn_planned_lat": "25",
            "stn_planned_lon": "50",
            "stn_planned_depth": "10",
            "stn_notes": "Some Notes"
        }

    @tag('stn_form', 'valid_data')
    def test_stn_valid_data(self):
        form = forms.StnForm(data=self.valid_data)
        form.is_valid()
        self.assertFalse(form.errors)


class TestPrjForm(TestCase):
    valid_data = {
        "prj_name": 'PRJ_001',
        "prj_description": "Some project description here",
        "prj_url": "https//noneOfYourBusiness.com"
    }

    @tag('prj_form', 'valid_data')
    def test_prj_valid_data(self):
        form = forms.PrjForm(data=self.valid_data)
        form.is_valid()
        self.assertFalse(form.errors)
