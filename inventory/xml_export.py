import html

from django.db.models import Q
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree
from xml.dom import minidom
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from lib.functions.custom_functions import attr_error_2_none
from lib.templatetags.custom_filters import nz
from . import models
from django.urls import reverse


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ", encoding="utf-8")


def charstring(root, level_1_tag, text_eng, text_fre=None):
    """Takes in the root and creates a charstring tag in the root. If text_fre is missing it will be a unilingual element.
        """
    if text_fre is None:
        level_1 = SubElement(root, level_1_tag)
        CharacterString = SubElement(level_1, 'gco:CharacterString').text = text_eng
    else:
        level_1 = SubElement(root, level_1_tag, attrib={
            'xsi:type': "gmd:PT_FreeText_PropertyType",
        })
        SubElement(level_1, 'gco:CharacterString').text = text_eng
        PT_FreeText = SubElement(level_1, 'gmd:PT_FreeText')
        textGroup = SubElement(PT_FreeText, 'gmd:textGroup')
        LocalisedCharacterString = SubElement(textGroup, 'gmd:LocalisedCharacterString', attrib={
            'locale': "#fra"
        }).text = text_fre
    return None


def date_converter(year, month=None, day=None):
    if day != None:
        date_string = "{}-{}-{}".format(str(year).zfill(4), str(month).zfill(2), str(day).zfill(2))
    elif month != None:
        date_string = "{}-{}".format(str(year).zfill(4), str(month).zfill(2))
    else:
        date_string = "{}".format(str(year).zfill(4))
    return date_string


def datestamp(root, level_1_tag, year, month=None, day=None):
    date_string = date_converter(year, month, day)
    level_1 = SubElement(root, level_1_tag)
    datestamp = SubElement(level_1, 'gco:Date').text = date_string  # DJF modified this from DateTime to Date
    return None


def codelist(root, level_1_tag, level_2_tag, code_list, code_list_value, text):
    element = SubElement(SubElement(root, level_1_tag), level_2_tag, attrib={
        'codeList': code_list,
        'codeListValue': code_list_value,
    }).text = text
    return None


def ci_responsible_party(resource_person):
    root = Element('gmd:CI_ResponsibleParty')

    # individualName
    charstring(root, 'gmd:individualName', resource_person.person.full_name)

    # organisationName
    charstring(root, 'gmd:organisationName', attr_error_2_none(resource_person.person.organization, "name_eng"),
               attr_error_2_none(resource_person.person.organization, "name_fre"))

    # positionName
    charstring(root, 'gmd:positionName', resource_person.person.position_eng, resource_person.person.position_fre)

    contact_info = SubElement(root, "gmd:contactInfo")
    ci_contact = SubElement(contact_info, "gmd:CI_Contact")
    # telephone
    phone = SubElement(ci_contact, "gmd:phone")
    ci_telephone = SubElement(phone, "gmd:CI_Telephone")
    charstring(ci_telephone, 'gmd:voice', resource_person.person.phone, resource_person.person.phone)
    # address
    address = SubElement(ci_contact, "gmd:address")
    ci_address = SubElement(address, "gmd:CI_Address")
    # civic
    charstring(ci_address, 'gmd:deliveryPoint', attr_error_2_none(resource_person.person.organization, "address"),
               attr_error_2_none(resource_person.person.organization, "address"))
    # city
    charstring(ci_address, 'gmd:city', attr_error_2_none(resource_person.person.organization, "city"),
               attr_error_2_none(resource_person.person.organization, "city"))
    # province
    my_loc = attr_error_2_none(resource_person.person.organization, "location")
    charstring(ci_address, 'gmd:administrativeArea',
               attr_error_2_none(my_loc, "location_eng"),
               attr_error_2_none(my_loc, "location_fre"),
               )
    # postalcode
    charstring(ci_address, 'gmd:postalCode', attr_error_2_none(resource_person.person.organization, "postal_code"))
    # country
    my_loc = attr_error_2_none(resource_person.person.organization, "location")
    charstring(ci_address, 'gmd:country',
               attr_error_2_none(my_loc, "country"),
               attr_error_2_none(my_loc, "country"),
               )
    # email
    charstring(ci_address, 'gmd:electronicMailAddress', resource_person.person.user.email,
               resource_person.person.user.email)
    # role
    codelist(root, "gmd:role", "gmd:CI_RoleCode",
             "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_90", resource_person.role.code,
             resource_person.role.role)
    return root


def descriptive_keyword(keyword):
    """ returns an xml block for a single keyword
    """
    if keyword.text_value_fre is None:
        print("There is no french version of the keyword '{}'".format(keyword.text_value_eng))

    root = Element('gmd:keyword', attrib={
        'xmlns:gmd': "http://www.isotc211.org/2005/gmd",
        'xmlns:xsi': "http://www.w3.org/2001/XMLSchema-instance",
        'xsi:type': "gmd:PT_FreeText_PropertyType",
    })
    SubElement(root, 'gco:CharacterString', attrib={
        'xmlns:gco': "http://www.isotc211.org/2005/gco",
    }).text = keyword.non_hierarchical_name_en
    PT_FreeText = SubElement(root, 'gmd:PT_FreeText')
    textGroup = SubElement(PT_FreeText, 'gmd:textGroup')
    LocalisedCharacterString = SubElement(textGroup, 'gmd:LocalisedCharacterString', attrib={
        'locale': "#fra"
    }).text = keyword.non_hierarchical_name_fr
    return root


class SupplemantInformation:
    def __init__(self, resource):
        self.resource = resource

    # list of fields to build #
    ##########################
    # parameters collected
    # QC process description
    # Physical sample description
    # citations

    def create_english_block(self):
        xml_block = ""
        # parameters collected
        if self.resource.parameters_collected_eng != None and self.resource.parameters_collected_eng != "":
            xml_temp = "PARAMETERS COLLECTED:\n{}".format(self.resource.parameters_collected_eng)
            if xml_block is None:
                xml_block = xml_temp
            else:
                xml_block = "{}\n\n{}".format(xml_block, xml_temp)

        # QC process description
        if self.resource.qc_process_descr_eng != None and self.resource.qc_process_descr_eng != "":
            xml_temp = "NOTES ON QUALITY CONTROL:\n{}".format(self.resource.qc_process_descr_eng)
            if xml_block is None:
                xml_block = xml_temp
            else:
                xml_block = "{}\n\n{}".format(xml_block, xml_temp)

        # Physical sample description
        if self.resource.physical_sample_descr_eng != None and self.resource.physical_sample_descr_eng != "":
            xml_temp = "PHYSICAL SAMPLE DETAILS:\n{}".format(self.resource.physical_sample_descr_eng)
            if xml_block is None:
                xml_block = xml_temp
            else:
                xml_block = "{}\n\n{}".format(xml_block, xml_temp)

        # Sampling Method
        if self.resource.sampling_method_eng != None and self.resource.sampling_method_eng != "":
            xml_temp = "SAMPLING METHODS:\n{}".format(self.resource.sampling_method_eng)
            if xml_block is None:
                xml_block = xml_temp
            else:
                xml_block = "{}\n\n{}".format(xml_block, xml_temp)

        # citations
        if self.resource.citations.count() > 0:
            citation_list = ""
            for citation in self.resource.citations.all():
                if citation_list == "":
                    citation_list = "{}".format(citation.short_citation)
                else:
                    citation_list = "{}\n\n{}".format(citation_list, citation.short_citation)

            xml_temp = "CITATION LIST:\n{}".format(citation_list)
            if xml_block is None:
                xml_block = xml_temp
            else:
                xml_block = "{}\n\n{}".format(xml_block, xml_temp)
        return xml_block

    def create_french_block(self):
        xml_block = ""
        # parameters collected
        if self.resource.parameters_collected_fre != None and self.resource.parameters_collected_fre != "":
            xml_temp = "PARAMÈTRES COLLECTÉS :\n{}".format(self.resource.parameters_collected_fre)
            if xml_block is None:
                xml_block = xml_temp
            else:
                xml_block = "{}\n\n{}".format(xml_block, xml_temp)

        # QC process description
        if self.resource.qc_process_descr_fre != None and self.resource.qc_process_descr_fre != "":
            xml_temp = "NOTES SUR LE CONTRÔLE DE QUALITÉ :\n{}".format(self.resource.qc_process_descr_fre)
            if xml_block is None:
                xml_block = xml_temp
            else:
                xml_block = "{}\n\n{}".format(xml_block, xml_temp)

        # Physical sample description
        if self.resource.physical_sample_descr_fre != None and self.resource.physical_sample_descr_fre != "":
            xml_temp = "DÉTAILS DE L'ÉCHANTILLON PHYSIQUE :\n{}".format(self.resource.physical_sample_descr_fre)
            if xml_block is None:
                xml_block = xml_temp
            else:
                xml_block = "{}\n\n{}".format(xml_block, xml_temp)

        # Sampling method
        if self.resource.sampling_method_fre != None and self.resource.sampling_method_fre != "":
            xml_temp = "MÉTHODES D'ÉCHANTILLONNAGE :\n{}".format(self.resource.sampling_method_fre)
            if xml_block is None:
                xml_block = xml_temp
            else:
                xml_block = "{}\n\n{}".format(xml_block, xml_temp)

        # citations
        if self.resource.citations.count() > 0:
            citation_list = ""
            for citation in self.resource.citations.all():
                if citation_list == "":
                    citation_list = "{}".format(citation.short_citation)
                else:
                    citation_list = "{}\n\n{}".format(citation_list, citation.short_citation)

            xml_temp = "LISTE DE RÉFÉRENCE :\n{}".format(citation_list)
            if xml_block is None:
                xml_block = xml_temp
            else:
                xml_block = "{}\n\n{}".format(xml_block, xml_temp)

        return xml_block


class KeywordGroup:
    def __init__(self, resource, domain):
        self.keywords = resource.keywords.filter(keyword_domain_id=domain)
        self.domain = domain
        self.keyword_count = len(self.keywords)

    def create_topic_category(self, root):
        """returns an xml element for the whole topicCategory domain
        """
        for keyword in self.keywords:
            topicCategory = SubElement(root, 'gmd:topicCategory')
            MD_TopicCategoryCode = SubElement(topicCategory, 'gmd:MD_TopicCategoryCode')
            MD_TopicCategoryCode.text = keyword.text_value_eng

    def create_group_element(self):
        """returns an xml element for the whole keyword domain
        """
        descriptiveKeywords = Element('gmd:descriptiveKeywords')
        MD_Keywords = SubElement(descriptiveKeywords, 'gmd:MD_Keywords')

        # for each keyword add a keyword block using nested function
        for keyword in self.keywords:
            MD_Keywords.append(descriptive_keyword(keyword))

        # annotation #
        ##############
        if self.domain == 1:  # NASA good
            codelist(MD_Keywords, "gmd:type", "gmd:MD_KeywordTypeCode",
                     "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_101", "RI_528",
                     "theme; thème")
            thesaurusName = SubElement(MD_Keywords, 'gmd:thesaurusName')
            CI_Citation = SubElement(thesaurusName, 'gmd:CI_Citation')
            charstring(CI_Citation, 'gmd:title',
                       "NASA/Global Change Master Directory (GCMD) Science Keywords Version 6.0.0.0.0",
                       "NASA/Global Change Master Directory (GCMD) Science Keywords Version 6.0.0.0.0")
            # revision date
            date = SubElement(CI_Citation, 'gmd:date')
            CI_Date = SubElement(date, 'gmd:CI_Date')
            datestamp(CI_Date, 'gmd:date', 2007)
            codelist(CI_Date, "gmd:dateType", "gmd:CI_DateTypeCode",
                     "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_87", "RI_368",
                     "revision; révision")
            # publication date
            date = SubElement(CI_Citation, 'gmd:date')
            CI_Date = SubElement(date, 'gmd:CI_Date')
            datestamp(CI_Date, 'gmd:date', 2007)
            codelist(CI_Date, "gmd:dateType", "gmd:CI_DateTypeCode",
                     "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_87", "RI_367",
                     "publication; publication")
            # creation date
            date = SubElement(CI_Citation, 'gmd:date')
            CI_Date = SubElement(date, 'gmd:CI_Date')
            datestamp(CI_Date, 'gmd:date', 2007)
            codelist(CI_Date, "gmd:dateType", "gmd:CI_DateTypeCode",
                     "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_87", "RI_366",
                     "creation;création")
            citedResponsibleParty = SubElement(CI_Citation, 'gmd:citedResponsibleParty')
            CI_ResponsibleParty = SubElement(citedResponsibleParty, 'gmd:CI_ResponsibleParty')
            charstring(CI_ResponsibleParty, 'gmd:individualName',
                       'LM Olsen, G Major, K Shein, J Scialdone, R Vogel, S Leicester, H Weir, S Ritz, T Stevens, M Meaux, C Solomon, R Bilodeau, M Holland, T Northcutt, RA Restrepo')
            charstring(CI_ResponsibleParty, 'gmd:organisationName', 'NASA', 'NASA')
            contactInfo = SubElement(CI_ResponsibleParty, 'gmd:contactInfo')
            CI_Contact = SubElement(contactInfo, 'gmd:CI_Contact')
            onlineResource = SubElement(CI_Contact, 'gmd:onlineResource')
            CI_OnlineResource = SubElement(onlineResource, 'gmd:CI_OnlineResource')
            linkage = SubElement(CI_OnlineResource, 'gmd:linkage')
            url = SubElement(linkage, 'gmd:URL')
            url.text = "http://gcmd.nasa.gov/index.html"
            charstring(CI_OnlineResource, 'gmd:protocol', 'WWW:LINK-1.0-http--link')
            codelist(CI_ResponsibleParty, "gmd:role", "gmd:CI_RoleCode",
                     "http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_RoleCode", 'owner', 'Owner')


        elif self.domain == 2:  # ITIS
            codelist(MD_Keywords, "gmd:type", "gmd:MD_KeywordTypeCode",
                     "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_101", "RI_528",
                     "theme; thème")
            thesaurusName = SubElement(MD_Keywords, 'gmd:thesaurusName')
            CI_Citation = SubElement(thesaurusName, 'gmd:CI_Citation')
            charstring(CI_Citation, 'gmd:title', "Integrated Taxonomic Information System (ITIS)",
                       "Système d'information taxonomique intégré (SITI)")
            # revision date
            date = SubElement(CI_Citation, 'gmd:date')
            CI_Date = SubElement(date, 'gmd:CI_Date')
            datestamp(CI_Date, 'gmd:date', 2017)
            codelist(CI_Date, "gmd:dateType", "gmd:CI_DateTypeCode",
                     "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_87", "RI_368",
                     "revision; révision")
            # publication date
            date = SubElement(CI_Citation, 'gmd:date')
            CI_Date = SubElement(date, 'gmd:CI_Date')
            datestamp(CI_Date, 'gmd:date', 2017)
            codelist(CI_Date, "gmd:dateType", "gmd:CI_DateTypeCode",
                     "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_87", "RI_367",
                     "publication; publication")
            # creation date
            date = SubElement(CI_Citation, 'gmd:date')
            CI_Date = SubElement(date, 'gmd:CI_Date')
            datestamp(CI_Date, 'gmd:date', 2017)
            codelist(CI_Date, "gmd:dateType", "gmd:CI_DateTypeCode",
                     "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_87", "RI_366",
                     "creation;création")
            citedResponsibleParty = SubElement(CI_Citation, 'gmd:citedResponsibleParty')
            CI_ResponsibleParty = SubElement(citedResponsibleParty, 'gmd:CI_ResponsibleParty')
            charstring(CI_ResponsibleParty, 'gmd:organisationName', 'Integrated Taxonomic Information System (ITIS)',
                       "Système d'information taxonomique intégré (SITI)")
            contactInfo = SubElement(CI_ResponsibleParty, 'gmd:contactInfo')
            CI_Contact = SubElement(contactInfo, 'gmd:CI_Contact')
            onlineResource = SubElement(CI_Contact, 'gmd:onlineResource')
            CI_OnlineResource = SubElement(onlineResource, 'gmd:CI_OnlineResource')
            linkage = SubElement(CI_OnlineResource, 'gmd:linkage')
            url = SubElement(linkage, 'gmd:URL')
            url.text = "https://www.itis.gov"
            charstring(CI_OnlineResource, 'gmd:protocol', 'WWW:LINK-1.0-http--link')
            codelist(CI_ResponsibleParty, "gmd:role", "gmd:CI_RoleCode",
                     "http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_RoleCode", 'owner', 'Owner')

        elif self.domain == 3:  # MeSH
            codelist(MD_Keywords, "gmd:type", "gmd:MD_KeywordTypeCode",
                     "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_101", "RI_528",
                     "theme; thème")
            thesaurusName = SubElement(MD_Keywords, 'gmd:thesaurusName')
            CI_Citation = SubElement(thesaurusName, 'gmd:CI_Citation')
            charstring(CI_Citation, 'gmd:title', "Medical Subject Headings (MeSH)", "Medical Subject Headings (MeSH)")
            # revision date
            date = SubElement(CI_Citation, 'gmd:date')
            CI_Date = SubElement(date, 'gmd:CI_Date')
            datestamp(CI_Date, 'gmd:date', 2018)
            codelist(CI_Date, "gmd:dateType", "gmd:CI_DateTypeCode",
                     "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_87", "RI_368",
                     "revision; révision")
            # publication date
            date = SubElement(CI_Citation, 'gmd:date')
            CI_Date = SubElement(date, 'gmd:CI_Date')
            datestamp(CI_Date, 'gmd:date', 2018)
            codelist(CI_Date, "gmd:dateType", "gmd:CI_DateTypeCode",
                     "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_87", "RI_367",
                     "publication; publication")
            # creation date
            date = SubElement(CI_Citation, 'gmd:date')
            CI_Date = SubElement(date, 'gmd:CI_Date')
            datestamp(CI_Date, 'gmd:date', 2018)
            codelist(CI_Date, "gmd:dateType", "gmd:CI_DateTypeCode",
                     "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_87", "RI_366",
                     "creation;création")
            citedResponsibleParty = SubElement(CI_Citation, 'gmd:citedResponsibleParty')
            CI_ResponsibleParty = SubElement(citedResponsibleParty, 'gmd:CI_ResponsibleParty')
            charstring(CI_ResponsibleParty, 'gmd:organisationName', 'U.S. National Library of Medicine',
                       'U.S. National Library of Medicine')
            contactInfo = SubElement(CI_ResponsibleParty, 'gmd:contactInfo')
            CI_Contact = SubElement(contactInfo, 'gmd:CI_Contact')
            onlineResource = SubElement(CI_Contact, 'gmd:onlineResource')
            CI_OnlineResource = SubElement(onlineResource, 'gmd:CI_OnlineResource')
            linkage = SubElement(CI_OnlineResource, 'gmd:linkage')
            url = SubElement(linkage, 'gmd:URL')
            url.text = "https://www.nlm.nih.gov/mesh/"
            charstring(CI_OnlineResource, 'gmd:protocol', 'WWW:LINK-1.0-http--link')
            codelist(CI_ResponsibleParty, "gmd:role", "gmd:CI_RoleCode",
                     "http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_RoleCode", 'owner', 'Owner')

        elif self.domain == 4:  # Uncontrolled
            codelist(MD_Keywords, "gmd:type", "gmd:MD_KeywordTypeCode",
                     "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_101", "RI_528",
                     "theme; thème")
            thesaurusName = SubElement(MD_Keywords, 'gmd:thesaurusName')
            CI_Citation = SubElement(thesaurusName, 'gmd:CI_Citation')
            charstring(CI_Citation, 'gmd:title', "uncontrolled vocabulary; user-specified",
                       "vocabulaire libre; spécifié par l'utilisateur")
            # revision date
            date = SubElement(CI_Citation, 'gmd:date')
            CI_Date = SubElement(date, 'gmd:CI_Date')
            datestamp(CI_Date, 'gmd:date', 2018)
            codelist(CI_Date, "gmd:dateType", "gmd:CI_DateTypeCode",
                     "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_87", "RI_368",
                     "revision; révision")
            # publication date
            date = SubElement(CI_Citation, 'gmd:date')
            CI_Date = SubElement(date, 'gmd:CI_Date')
            datestamp(CI_Date, 'gmd:date', 2018)
            codelist(CI_Date, "gmd:dateType", "gmd:CI_DateTypeCode",
                     "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_87", "RI_367",
                     "publication; publication")
            # creation date
            date = SubElement(CI_Citation, 'gmd:date')
            CI_Date = SubElement(date, 'gmd:CI_Date')
            datestamp(CI_Date, 'gmd:date', 2018)
            codelist(CI_Date, "gmd:dateType", "gmd:CI_DateTypeCode",
                     "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_87", "RI_366",
                     "creation;création")
            citedResponsibleParty = SubElement(CI_Citation, 'gmd:citedResponsibleParty')
            CI_ResponsibleParty = SubElement(citedResponsibleParty, 'gmd:CI_ResponsibleParty')
            charstring(CI_ResponsibleParty, 'gmd:organisationName', 'n/a', 'n/a')
            codelist(CI_ResponsibleParty, "gmd:role", "gmd:CI_RoleCode",
                     "http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_RoleCode", 'owner', 'Owner')


        elif self.domain == 5:  # WoRMS
            codelist(MD_Keywords, "gmd:type", "gmd:MD_KeywordTypeCode",
                     "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_101", "RI_528",
                     "theme; thème")
            thesaurusName = SubElement(MD_Keywords, 'gmd:thesaurusName')
            CI_Citation = SubElement(thesaurusName, 'gmd:CI_Citation')
            charstring(CI_Citation, 'gmd:title', "World Register of Marine Species (WoRMS)",
                       "World Register of Marine Species (WoRMS)")
            # revision date
            date = SubElement(CI_Citation, 'gmd:date')
            CI_Date = SubElement(date, 'gmd:CI_Date')
            datestamp(CI_Date, 'gmd:date', 2018)
            codelist(CI_Date, "gmd:dateType", "gmd:CI_DateTypeCode",
                     "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_87", "RI_368",
                     "revision; révision")
            # publication date
            date = SubElement(CI_Citation, 'gmd:date')
            CI_Date = SubElement(date, 'gmd:CI_Date')
            datestamp(CI_Date, 'gmd:date', 2018)
            codelist(CI_Date, "gmd:dateType", "gmd:CI_DateTypeCode",
                     "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_87", "RI_367",
                     "publication; publication")
            # creation date
            date = SubElement(CI_Citation, 'gmd:date')
            CI_Date = SubElement(date, 'gmd:CI_Date')
            datestamp(CI_Date, 'gmd:date', 2018)
            codelist(CI_Date, "gmd:dateType", "gmd:CI_DateTypeCode",
                     "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_87", "RI_366",
                     "creation;création")
            citedResponsibleParty = SubElement(CI_Citation, 'gmd:citedResponsibleParty')
            CI_ResponsibleParty = SubElement(citedResponsibleParty, 'gmd:CI_ResponsibleParty')
            charstring(CI_ResponsibleParty, 'gmd:organisationName', 'World Register of Marine Species',
                       'World Register of Marine Species')
            contactInfo = SubElement(CI_ResponsibleParty, 'gmd:contactInfo')
            CI_Contact = SubElement(contactInfo, 'gmd:CI_Contact')
            onlineResource = SubElement(CI_Contact, 'gmd:onlineResource')
            CI_OnlineResource = SubElement(onlineResource, 'gmd:CI_OnlineResource')
            linkage = SubElement(CI_OnlineResource, 'gmd:linkage')
            url = SubElement(linkage, 'gmd:URL')
            url.text = "http://www.marinespecies.org/"
            charstring(CI_OnlineResource, 'gmd:protocol', 'WWW:LINK-1.0-http--link')
            codelist(CI_ResponsibleParty, "gmd:role", "gmd:CI_RoleCode",
                     "http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#CI_RoleCode", 'owner', 'Owner')

        elif self.domain == 6:  # core subject
            codelist(MD_Keywords, "gmd:type", "gmd:MD_KeywordTypeCode",
                     "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_101", "RI_528",
                     "theme; thème")
            thesaurusName = SubElement(MD_Keywords, 'gmd:thesaurusName')
            CI_Citation = SubElement(thesaurusName, 'gmd:CI_Citation')
            charstring(CI_Citation, 'gmd:title', "Government of Canada Core Subject Thesaurus",
                       "Thésaurus des sujets de base du gouvernement du Canada")
            # creation date
            date = SubElement(CI_Citation, 'gmd:date')
            CI_Date = SubElement(date, 'gmd:CI_Date')
            datestamp(CI_Date, 'gmd:date', 2004)
            codelist(CI_Date, "gmd:dateType", "gmd:CI_DateTypeCode",
                     "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_87", "RI_366",
                     "creation; création")
            date = SubElement(CI_Citation, 'gmd:date')
            CI_Date = SubElement(date, 'gmd:CI_Date')
            datestamp(CI_Date, 'gmd:date', 2016, 7, 4)
            codelist(CI_Date, "gmd:dateType", "gmd:CI_DateTypeCode",
                     "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_87", "RI_368",
                     "revision; révision")
            # publication date
            date = SubElement(CI_Citation, 'gmd:date')
            CI_Date = SubElement(date, 'gmd:CI_Date')
            datestamp(CI_Date, 'gmd:date', 2007, 7, 23)
            codelist(CI_Date, "gmd:dateType", "gmd:CI_DateTypeCode",
                     "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_87", "RI_367",
                     "publication; publication")
            citedResponsibleParty = SubElement(CI_Citation, 'gmd:citedResponsibleParty')
            CI_ResponsibleParty = SubElement(citedResponsibleParty, 'gmd:CI_ResponsibleParty')
            charstring(CI_ResponsibleParty, 'gmd:organisationName', 'Government of Canada; Library and Archives Canada',
                       'Gouvernement du Canada; Bibliothèque et Archives Canada')
            contactInfo = SubElement(CI_ResponsibleParty, 'gmd:contactInfo')
            CI_Contact = SubElement(contactInfo, 'gmd:CI_Contact')
            onlineResource = SubElement(CI_Contact, 'gmd:onlineResource')
            CI_OnlineResource = SubElement(onlineResource, 'gmd:CI_OnlineResource')
            linkage = SubElement(CI_OnlineResource, 'gmd:linkage')
            url = SubElement(linkage, 'gmd:URL')
            url.text = "http://canada.multites.net"
            charstring(CI_OnlineResource, 'gmd:protocol', 'WWW:LINK-1.0-http--link')
            codelist(CI_ResponsibleParty, "gmd:role", "gmd:CI_RoleCode",
                     "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_90", 'RI_409',
                     'custodian; conservateur')

        elif self.domain == 7:  # DFO areas
            codelist(MD_Keywords, "gmd:type", "gmd:MD_KeywordTypeCode",
                     "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_101", "RI_525", "place")
            thesaurusName = SubElement(MD_Keywords, 'gmd:thesaurusName')
            CI_Citation = SubElement(thesaurusName, 'gmd:CI_Citation')
            charstring(CI_Citation, 'gmd:title', "DFO Areas", "Zones du MPO")
            # revision date
            date = SubElement(CI_Citation, 'gmd:date')
            CI_Date = SubElement(date, 'gmd:CI_Date')
            datestamp(CI_Date, 'gmd:date', 2009, 1, 6)
            codelist(CI_Date, "gmd:dateType", "gmd:CI_DateTypeCode",
                     "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_87", "RI_368",
                     "revision; révision")
            # publication date
            date = SubElement(CI_Citation, 'gmd:date')
            CI_Date = SubElement(date, 'gmd:CI_Date')
            datestamp(CI_Date, 'gmd:date', 2009)
            codelist(CI_Date, "gmd:dateType", "gmd:CI_DateTypeCode",
                     "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_87", "RI_367",
                     "publication; publication")
            # creation date
            date = SubElement(CI_Citation, 'gmd:date')
            CI_Date = SubElement(date, 'gmd:CI_Date')
            datestamp(CI_Date, 'gmd:date', 2009)
            codelist(CI_Date, "gmd:dateType", "gmd:CI_DateTypeCode",
                     "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_87", "RI_366",
                     "creation;création")
            citedResponsibleParty = SubElement(CI_Citation, 'gmd:citedResponsibleParty')
            CI_ResponsibleParty = SubElement(citedResponsibleParty, 'gmd:CI_ResponsibleParty')
            charstring(CI_ResponsibleParty, 'gmd:individualName', 'Doug Gregory')
            charstring(CI_ResponsibleParty, 'gmd:organisationName', 'Government of Canada; Fisheries and Oceans Canada',
                       'Gouvernement du Canada; Pêches et Océans Canada')
            contactInfo = SubElement(CI_ResponsibleParty, 'gmd:contactInfo')
            CI_Contact = SubElement(contactInfo, 'gmd:CI_Contact')
            onlineResource = SubElement(CI_Contact, 'gmd:onlineResource')
            CI_OnlineResource = SubElement(onlineResource, 'gmd:CI_OnlineResource')
            linkage = SubElement(CI_OnlineResource, 'gmd:linkage')
            url = SubElement(linkage, 'gmd:URL')
            url.text = "http://gcmd.nasa.gov/index.html"
            charstring(CI_OnlineResource, 'gmd:protocol', 'WWW:LINK-1.0-http--link')
            codelist(CI_ResponsibleParty, "gmd:role", "gmd:CI_RoleCode",
                     "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_90", 'RI_413',
                     'originator; créateur')

        return descriptiveKeywords


def construct(my_resource, pretty=True):
    # ElementTree.register_namespace("gmd","http://www.isotc211.org/2005/gmd")
    # ElementTree.register_namespace("xsi","http://www.w3.org/2001/XMLSchema-instance")

    root = Element("gmd:MD_Metadata", attrib={
        "xmlns:gmd": "http://www.isotc211.org/2005/gmd",
        'xmlns:srv': "http://www.isotc211.org/2005/srv",
        'xmlns:gss': "http://www.isotc211.org/2005/gss",
        'xmlns:gco': "http://www.isotc211.org/2005/gco",
        'xmlns:xlink': "http://www.w3.org/1999/xlink",
        'xmlns:gts': "http://www.isotc211.org/2005/gts",
        'xmlns:gfc': "http://www.isotc211.org/2005/gfc",
        'xmlns:gmi': "http://www.isotc211.org/2005/gmi",
        'xmlns:gml': "http://www.opengis.net/gml/3.2",
        'xmlns:gmx': "http://www.isotc211.org/2005/gmx",
        'xmlns:gsr': "http://www.isotc211.org/2005/gsr",
        'xmlns': "http://www.isotc211.org/2005/gmd",
        'xmlns:geonet': "http://www.fao.org/geonetwork",
        'xmlns:xsi': "http://www.w3.org/2001/XMLSchema-instance",
        'xsi:schemaLocation': "http://www.isotc211.org/2005/gmd http://nap.geogratis.gc.ca/metadata/tools/schemas/metadata/can-cgsb-171.100-2009-a/gmd/gmd.xsd http://www.isotc211.org/2005/srv http://nap.geogratis.gc.ca/metadata/tools/schemas/metadata/can-cgsb-171.100-2009-a/srv/srv.xsd http://www.geconnections.org/nap/napMetadataTools/napXsd/napm http://nap.geogratis.gc.ca/metadata/tools/schemas/metadata/can-cgsb-171.100-2009-a/napm/napm.xsd",

    })

    # uuid
    charstring(root, 'gmd:fileIdentifier', str(my_resource.uuid))

    # language
    charstring(root, 'gmd:language', "eng; CAN")

    # characterSet for metadata
    codelist(root, "gmd:characterSet", "gmd:MD_CharacterSetCode",
             "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_95", "RI_458", "utf8; utf8")

    # parentIdentifier
    if my_resource.parent != None:
        charstring(root, 'gmd:parentIdentifier', str(my_resource.parent.uuid))

    # ResourceType
    try:
        codelist(root, "gmd:hierarchyLevel", "gmd:MD_ScopeCode",
                 "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_108",
                 my_resource.resource_type.code, my_resource.resource_type.label)
    except AttributeError:
        print("no resource_type")

    # responsible parties for metadata information
    gmd_contact = SubElement(root, 'gmd:contact')

    # for each point of contact
    for person in my_resource.resource_people.filter(role__id=4):
        gmd_contact.append(ci_responsible_party(person))

    # timestamp
    datestamp(root, 'gmd:dateStamp', timezone.now().year, timezone.now().month, timezone.now().day)

    # metadata standard name - STATIC
    charstring(root, 'gmd:metadataStandardName',
               "North American Profile of ISO 19115:2003 - Geographic information - Metadata",
               "Profil nord-américain de la norme ISO 19115:2003 - Information géographique - Métadonnées")

    # metadata standards version - STATIC
    charstring(root, 'gmd:metadataStandardVersion', "CAN/CGSB-171.100-2009")

    # locale - STATIC
    PT_Locale = SubElement(SubElement(root, 'gmd:locale'), "gmd:PT_Locale", attrib={'id': "fra"})
    codelist(PT_Locale, "gmd:languageCode", "gmd:LanguageCode",
             "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_116", "fra", "French; Français")
    codelist(PT_Locale, "gmd:Country", "gmd:Country",
             "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_117", "CAN", "Canada; Canada")
    codelist(PT_Locale, "gmd:characterEncoding", "gmd:MD_CharacterSetCode",
             "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_458", "RI_458", "utf8; utf8")

    # Reference system info
    referenceSystemInfo = SubElement(root, 'gmd:referenceSystemInfo')
    MD_ReferenceSystem = SubElement(referenceSystemInfo, 'gmd:MD_ReferenceSystem')
    referenceSystemIdentifier = SubElement(MD_ReferenceSystem, 'gmd:referenceSystemIdentifier')
    RS_Identifier = SubElement(referenceSystemIdentifier, 'gmd:RS_Identifier')

    try:
        charstring(RS_Identifier, 'gmd:code', my_resource.spat_ref_system.code)
        charstring(RS_Identifier, 'gmd:codeSpace', my_resource.spat_ref_system.codespace)
    except AttributeError:
        print("no spat_ref_system")

    # Data identification Info #
    ############################

    identificationInfo = SubElement(root, 'gmd:identificationInfo')
    MD_DataIdentification = SubElement(identificationInfo, 'gmd:MD_DataIdentification')
    citation = SubElement(MD_DataIdentification, 'gmd:citation')
    CI_Citation = SubElement(citation, 'gmd:CI_Citation')

    # Title
    charstring(CI_Citation, 'gmd:title', my_resource.title_eng, my_resource.title_fre)

    # creation date
    CI_Date = SubElement(SubElement(CI_Citation, 'gmd:date'), 'gmd:CI_Date')
    datestamp(CI_Date, 'gmd:date', my_resource.time_start_year, my_resource.time_start_month,
              my_resource.time_start_day)
    codelist(CI_Date, "gmd:dateType", "gmd:CI_DateTypeCode",
             "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_87", "RI_366",
             "creation; création")

    if my_resource.fgp_publication_date is None:  # only pass in a publication date, which would be the current time

        # publication date
        CI_Date = SubElement(SubElement(CI_Citation, 'gmd:date'), 'gmd:CI_Date')
        datestamp(CI_Date, 'gmd:date', timezone.now().year, timezone.now().month, timezone.now().day)
        codelist(CI_Date, "gmd:dateType", "gmd:CI_DateTypeCode",
                 "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_87", "RI_367",
                 "publication; publication")

    else:  # publication AND revision dates are added (if available)

        # publication date
        CI_Date = SubElement(SubElement(CI_Citation, 'gmd:date'), 'gmd:CI_Date')
        datestamp(CI_Date, 'gmd:date', my_resource.fgp_publication_date.year, my_resource.fgp_publication_date.month,
                  my_resource.fgp_publication_date.day)
        codelist(CI_Date, "gmd:dateType", "gmd:CI_DateTypeCode",
                 "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_87", "RI_367",
                 "publication; publication")

        if my_resource.last_revision_date:
            # revision date
            CI_Date = SubElement(SubElement(CI_Citation, 'gmd:date'), 'gmd:CI_Date')
            datestamp(CI_Date, 'gmd:date', my_resource.last_revision_date.year, my_resource.last_revision_date.month,
                      my_resource.last_revision_date.day)
            codelist(CI_Date, "gmd:dateType", "gmd:CI_DateTypeCode",
                     "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_87", "RI_368",
                     "revision; révision")

    # Custodians and other roles (not point of contact)
    # for each point of contact
    for person in my_resource.resource_people.filter(~Q(role__id=4)).filter(role__code__isnull=False):
        # if person.role.id == 1:
        citedResponsibleParty = SubElement(CI_Citation, 'gmd:citedResponsibleParty')
        citedResponsibleParty.append(ci_responsible_party(person))

    # abstract
    charstring(MD_DataIdentification, 'gmd:abstract', my_resource.descr_eng, my_resource.descr_fre)

    # purpose
    charstring(MD_DataIdentification, 'gmd:purpose', my_resource.purpose_eng, my_resource.purpose_fre)

    # status
    try:
        codelist(MD_DataIdentification, "gmd:status", "gmd:MD_ProgressCode",
                 "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_106", my_resource.status.code,
                 my_resource.status.label)
    except AttributeError:
        print("no 'status'")

    # resource Maintenance
    MD_MaintenanceInformation = SubElement(SubElement(MD_DataIdentification, 'gmd:resourceMaintenance'),
                                           'gmd:MD_MaintenanceInformation')
    try:
        codelist(MD_MaintenanceInformation, "gmd:maintenanceAndUpdateFrequency", "gmd:MD_MaintenanceFrequencyCode",
                 "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_102",
                 my_resource.maintenance.code, my_resource.maintenance.code)
    except AttributeError:
        print("no 'maintenance'")

    # uncontrolled
    uncontrolled = KeywordGroup(my_resource, 4)
    if uncontrolled.keyword_count > 0:
        MD_DataIdentification.append(uncontrolled.create_group_element())

    # GCMD
    gcmd = KeywordGroup(my_resource, 1)
    if gcmd.keyword_count > 0:
        MD_DataIdentification.append(gcmd.create_group_element())

    # DFO areas
    dfo_area = KeywordGroup(my_resource, 7)
    if dfo_area.keyword_count > 0:
        MD_DataIdentification.append(dfo_area.create_group_element())

    # gc core subject
    gc_core = KeywordGroup(my_resource, 6)
    if gc_core.keyword_count > 0:
        MD_DataIdentification.append(gc_core.create_group_element())

    # ITIS
    itis = KeywordGroup(my_resource, 2)
    if itis.keyword_count > 0:
        MD_DataIdentification.append(itis.create_group_element())

    # MeSH
    mesh = KeywordGroup(my_resource, 3)
    if mesh.keyword_count > 0:
        MD_DataIdentification.append(mesh.create_group_element())

    # WoRMS
    worms = KeywordGroup(my_resource, 5)
    if worms.keyword_count > 0:
        MD_DataIdentification.append(worms.create_group_element())

    # LegalConstraints - STATIC
    MD_LegalConstraints = SubElement(SubElement(MD_DataIdentification, 'gmd:resourceConstraints'),
                                     'gmd:MD_LegalConstraints')
    charstring(MD_LegalConstraints, 'gmd:useLimitation',
               "Open Government Licence - Canada (http://open.canada.ca/en/open-government-licence-canada)",
               "Licence du gouvernement ouvert - Canada (http://ouvert.canada.ca/fr/licence-du-gouvernement-ouvert-canada)")
    codelist(MD_LegalConstraints, "gmd:accessConstraints", "gmd:MD_RestrictionCode",
             "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_107", "RI_606",
             "license; licence")
    codelist(MD_LegalConstraints, "gmd:useConstraints", "gmd:MD_RestrictionCode",
             "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_107", "RI_606",
             "license; licence")

    # General Constraints
    MD_Constraints = SubElement(SubElement(MD_DataIdentification, 'gmd:resourceConstraints'), 'gmd:MD_Constraints')
    charstring(MD_Constraints, 'gmd:useLimitation', my_resource.resource_constraint_eng,
               my_resource.resource_constraint_fre)

    # Security Constraints
    MD_SecurityConstraints = SubElement(SubElement(MD_DataIdentification, 'gmd:resourceConstraints'),
                                        'gmd:MD_SecurityConstraints')
    charstring(MD_SecurityConstraints, 'gmd:useLimitation', my_resource.security_use_limitation_eng,
               my_resource.security_use_limitation_fre)
    codelist(MD_SecurityConstraints, "gmd:classification", "gmd:MD_ClassificationCode",
             "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_96", "RI_484",
             "Unclassified; non-classifié")

    # spatialRepresentationType
    try:
        codelist(MD_DataIdentification, "gmd:spatialRepresentationType", "gmd:MD_SpatialRepresentationTypeCode",
                 "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_109",
                 my_resource.spat_representation.code, my_resource.spat_representation.label)
    except AttributeError:
        print("No 'spat_representation'")

        # language
    charstring(MD_DataIdentification, 'gmd:language', 'eng; CAN')

    # characterSet
    try:
        codelist(MD_DataIdentification, "gmd:characterSet", "gmd:MD_CharacterSetCode",
                 "http://nap.geogratis.gc.ca/metadata/register/napMetadataRegister.xml#IC_195",
                 my_resource.data_char_set.code, my_resource.data_char_set.label)
    except AttributeError:
        print("No 'data_char_set")

    # topic category
    topic_category = KeywordGroup(my_resource, 8)
    if topic_category.keyword_count > 0:
        topic_category.create_topic_category(MD_DataIdentification)

    # temporal extent
    extent = SubElement(MD_DataIdentification, 'gmd:extent')
    EX_Extent = SubElement(extent, 'gmd:EX_Extent')
    temporalElement = SubElement(EX_Extent, 'gmd:temporalElement')
    EX_TemporalExtent = SubElement(temporalElement, 'gmd:EX_TemporalExtent')
    extent = SubElement(EX_TemporalExtent, 'gmd:extent')
    TimePeriod = SubElement(extent, 'gml:TimePeriod', attrib={'gml:id': "timeperiod1"})
    beginPosition = SubElement(TimePeriod, 'gml:beginPosition')
    endPosition = SubElement(TimePeriod, 'gml:endPosition')
    beginPosition.text = date_converter(my_resource.time_start_year, my_resource.time_start_month,
                                        my_resource.time_start_day)
    if my_resource.time_end_year != None:
        endPosition.text = date_converter(my_resource.time_end_year, my_resource.time_end_month,
                                          my_resource.time_end_day)

    # geographic extent
    extent = SubElement(MD_DataIdentification, 'gmd:extent')
    EX_Extent = SubElement(extent, 'gmd:EX_Extent')
    charstring(EX_Extent, 'gmd:description', my_resource.geo_descr_eng, my_resource.geo_descr_fre)

    geographicElement = SubElement(EX_Extent, 'gmd:geographicElement')
    EX_GeographicBoundingBox = SubElement(geographicElement, 'gmd:EX_GeographicBoundingBox')
    westBoundLongitude = SubElement(EX_GeographicBoundingBox, 'gmd:westBoundLongitude')
    SubElement(westBoundLongitude, 'gco:Decimal').text = str(nz(my_resource.west_bounding, ""))
    eastBoundLongitude = SubElement(EX_GeographicBoundingBox, 'gmd:eastBoundLongitude')
    SubElement(eastBoundLongitude, 'gco:Decimal').text = str(nz(my_resource.east_bounding, ""))
    southBoundLatitude = SubElement(EX_GeographicBoundingBox, 'gmd:southBoundLatitude')
    SubElement(southBoundLatitude, 'gco:Decimal').text = str(nz(my_resource.south_bounding, ""))
    northBoundLatitude = SubElement(EX_GeographicBoundingBox, 'gmd:northBoundLatitude')
    SubElement(northBoundLatitude, 'gco:Decimal').text = str(nz(my_resource.north_bounding, ""))

    # supplemental information
    suppl_info = SupplemantInformation(my_resource)
    charstring(MD_DataIdentification, 'gmd:supplementalInformation', suppl_info.create_english_block(),
               suppl_info.create_french_block())

    distributionInfo = SubElement(root, 'gmd:distributionInfo')
    MD_Distribution = SubElement(distributionInfo, 'gmd:MD_Distribution')

    # distribution Format
    for df in my_resource.distribution_formats.all():
        MD_Format = SubElement(SubElement(MD_Distribution, 'gmd:distributionFormat '), "gmd:MD_Format")
        charstring(MD_Format, 'gmd:name', df.name)
        charstring(MD_Format, 'gmd:version', "n/a")

    # distributor
    distributor = SubElement(MD_Distribution, 'gmd:distributor')
    MD_Distributor = SubElement(distributor, 'gmd:MD_Distributor')
    distributorContact = SubElement(MD_Distributor, 'gmd:distributorContact')

    # for each point of contact
    for person in my_resource.resource_people.all():
        if person.role.id == 4:
            distributorContact.append(ci_responsible_party(person))

    # for each data resource
    for data_resource in my_resource.data_resources.all():
        transferOptions = SubElement(MD_Distribution, 'gmd:transferOptions')
        MD_DigitalTransferOptions = SubElement(transferOptions, 'gmd:MD_DigitalTransferOptions')
        onLine = SubElement(MD_DigitalTransferOptions, 'gmd:onLine')
        CI_OnlineResource = SubElement(onLine, 'gmd:CI_OnlineResource')
        linkage = SubElement(CI_OnlineResource, 'gmd:linkage')
        URL = SubElement(linkage, 'gmd:URL').text = data_resource.url
        charstring(CI_OnlineResource, 'gmd:protocol', data_resource.protocol)
        charstring(CI_OnlineResource, 'gmd:name', data_resource.name_eng, data_resource.name_fre)
        charstring(CI_OnlineResource, 'gmd:description', data_resource.content_type.english_value, data_resource.content_type.french_value)

    # for each web service
    for web_service in my_resource.web_services.all():
        transferOptions = SubElement(MD_Distribution, 'gmd:transferOptions')
        MD_DigitalTransferOptions = SubElement(transferOptions, 'gmd:MD_DigitalTransferOptions')
        onLine = SubElement(MD_DigitalTransferOptions, 'gmd:onLine', attrib={
            'xlink:role': web_service.service_language,
        })
        CI_OnlineResource = SubElement(onLine, 'gmd:CI_OnlineResource')
        linkage = SubElement(CI_OnlineResource, 'gmd:linkage')
        URL = SubElement(linkage, 'gmd:URL').text = web_service.url
        charstring(CI_OnlineResource, 'gmd:protocol', web_service.protocol)
        charstring(CI_OnlineResource, 'gmd:name', web_service.name_eng, web_service.name_fre)
        charstring(CI_OnlineResource, 'gmd:description', web_service.content_type.english_value,
                   web_service.content_type.french_value)
    if pretty:
        return prettify(root)
    else:
        return ElementTree(root)


def verify(resource):
    fields_to_check = [
        'uuid',
        'time_start_year',
        'west_bounding',
        'south_bounding',
        'east_bounding',
        'north_bounding',

        # bilingual fields
        '?title_',
        '?descr_',
        '?purpose_',
        '?geo_descr_',
        '?security_use_limitation_',

        # must check for fk and attribute
        '.resource_type.code',  # both fk and code attr
        '.status.code',  # both fk and code attr
        '.spat_ref_system.code',  # both fk and code and codespace attr
        '.spat_ref_system.codespace',  # both fk and code and codespace attr
        '.spat_representation.code',  # both fk and code attr
        '.data_char_set.code',
        '.maintenance.code',
        '.security_classification.code',

        # filters and counters; must have at least one of these
        'keywords|6',  # CST
        'keywords|7',  # dfo area
        'keywords|8',  # Topic category
        'resource_people|4',  # point of contact
        'resource_people|1',  # custodian
        'certification_history|',
        'data_resources|',
        'web_services|',
        'distribution_formats|',


        # will check all keywords associated with resource
        '*keyword.text_value_',  # special keywords function will be called

        # will check all people associated with resource
        '*person.organization',
        '*person.organization.name_',
        '*person.organization.location',
        '*person.organization.location.location_',
        '*person.position_',
        '*person.user.email',

        # optional fields; denoted by dollar sign $
        # these fields are optional but must be bilingual
        '$qc_process_descr_',  # QC process
        '$physical_sample_descr_',  # Physical Sample Description
        '$parameters_collected_',  # Parameters Collected
        '$sampling_method_',  # sampling method
        '$resource_constraint_',  # resource constraint
    ]

    # this is where we will store the feedback
    checklist = []
    # figure out the max possible score for completedness: number of fields, minus fields species to people and keywords,
    # plus number of keywords times number of fields for keywords (excluding ISO topic category, which are populated by FGP)
    # plus number of people times number of fields for people
    # note: any field ending in '_' represents two fields and thus should be counted twice

    simple_fields = len([f for f in fields_to_check if "$" not in f and "|" not in f and "." not in f and "__" not in f and "?" not in f])
    special_keyword_fields = len([f for f in fields_to_check if f.startswith("*keyword")])
    special_bilingual_keyword_fields = len([f for f in fields_to_check if f.startswith("*keyword") and f.endswith("_")])
    true_count_of_special_keyword_fields = special_keyword_fields - special_bilingual_keyword_fields + (
            special_bilingual_keyword_fields * 2)

    special_person_fields = len([f for f in fields_to_check if f.startswith("*person")])
    special_bilingual_person_fields = len([f for f in fields_to_check if f.startswith("*person") and f.endswith("_")])
    true_count_of_special_person_fields = special_person_fields - special_bilingual_person_fields + (special_bilingual_person_fields * 2)

    bilinugal_fields = len([f for f in fields_to_check if f.startswith("?") or f.startswith("$")])  # will include the optional fields
    true_count_of_bilinugal_fields = bilinugal_fields * 2

    fk_fields = len([f for f in fields_to_check if f.startswith(".")])
    true_count_of_fk_fields = fk_fields * 2  # because will be essentially checking for two fields.. the fk and the attr

    max_rating = len(fields_to_check) - \
                 (special_keyword_fields + special_person_fields + bilinugal_fields + fk_fields) + \
                 (resource.people.count() * true_count_of_special_person_fields) + \
                 (resource.keywords.filter(~Q(keyword_domain_id=8)).count() * true_count_of_special_keyword_fields) + \
                 true_count_of_bilinugal_fields + \
                 true_count_of_fk_fields + 1  # the +1 at the end is for the eng and fre web-service

    # start optimistic: full rating and translation is not needed
    rating = max_rating
    translation_needed = False

    for field in fields_to_check:
        # starting with the most simple case: unilingual fields of resource
        if "$" not in field and "|" not in field and "." not in field and "__" not in field and "?" not in field:
            field_value = nz(getattr(resource, field), None)
            verbose_name = resource._meta.get_field(field).verbose_name
            if field_value is None:
                checklist.append("A value for {} is missing.".format(verbose_name))
                rating = rating - 1
        # next lets deal with the simple bilingual fields
        elif field.startswith("?"):
            # for check to see if there is a value
            clean_field = field.replace("?", "")
            field_eng = "{}eng".format(clean_field)
            field_fre = "{}fre".format(clean_field)
            field_value_eng = nz(getattr(resource, field_eng), None)
            field_value_fre = nz(getattr(resource, field_fre), None)
            verbose_name_eng = resource._meta.get_field(field_eng).verbose_name
            verbose_name_fre = resource._meta.get_field(field_fre).verbose_name

            # check english field
            if field_value_eng is None:
                checklist.append("A value for {} is missing.".format(verbose_name_eng))
                rating = rating - 1

            # check french field
            if field_value_fre is None:
                checklist.append("A value for {} is missing.".format(verbose_name_fre))
                rating = rating - 1

            # now do a special bilingual field check to see if translation is needed
            if (field_value_eng is not None and field_value_fre is None) or (field_value_eng is None and field_value_fre is not None):
                translation_needed = True


        # next lets deal with optional fields
        elif field.startswith("$"):
            # for check to see if there is a value
            clean_field = field.replace("$", "")
            field_eng = "{}eng".format(clean_field)
            field_fre = "{}fre".format(clean_field)
            field_value_eng = nz(getattr(resource, field_eng), None)
            field_value_fre = nz(getattr(resource, field_fre), None)
            verbose_name_eng = resource._meta.get_field(field_eng).verbose_name
            verbose_name_fre = resource._meta.get_field(field_fre).verbose_name

            # now do a special bilingual field check to see if translation is needed
            if (field_value_eng is not None and field_value_fre is None) or (field_value_eng is None and field_value_fre is not None):
                checklist.append(
                    "'{}' and '{}' are optional fields, but if entered, they must be present in both languages".format(verbose_name_eng,
                                                                                                                       verbose_name_fre))
                rating = rating - 1
                translation_needed = True

        # next lets deal with foreign keys
        elif field.startswith("."):
            field_split = field.split(".")[1:]  # discard the first item
            fk_field = field_split[0]
            attr_field = field_split[1]

            # first check for fk value
            if nz(getattr(resource, fk_field), None) is None:
                checklist.append("A selection for {} is missing.".format(resource._meta.get_field(fk_field).verbose_name))
                rating = rating - 1
            #   otherwise check for attr value
            elif nz(getattr(getattr(resource, fk_field), attr_field), None) is None:
                verbose_name_fk = resource._meta.get_field(fk_field).verbose_name
                verbose_name_attr = getattr(resource, fk_field)._meta.get_field(attr_field).verbose_name
                checklist.append(
                    "The {} for {} is missing. Please contact your system administrator to have this fixed".format(verbose_name_attr,
                                                                                                                   verbose_name_fk))
                rating = rating - 1

        # deal with filters and counts
        elif "|" in field:
            field_list = field.split("|")
            field = field_list[0]
            my_filter = field_list[1]

            if field == 'certification_history':
                cert_now_html = mark_safe(
                    f'<a href={reverse("inventory:resource_certify", kwargs={"pk": resource.id})}>{_("certify now")}</a>')
                if resource.certification_history.count() == 0:
                    checklist.append(f'This record has not been certified ({cert_now_html})')
                    rating = rating - 1
                elif abs((resource.certification_history.first().certification_date - timezone.now()).days) > 30:
                    checklist.append(f'This record has not been certified within the past 30 days ({cert_now_html})')
                    rating = rating - 1

            elif field == 'keywords':
                keyword_domain = models.KeywordDomain.objects.get(pk=my_filter)
                if resource.keywords.filter(keyword_domain=keyword_domain).count() == 0:
                    checklist.append("At least one {} keyword is needed.".format(keyword_domain))
                    rating = rating - 1
            elif field == 'resource_people':
                role = models.PersonRole.objects.get(pk=my_filter)
                if resource.resource_people.filter(role=role) == 0:
                    checklist.append("At least one {} is needed.".format(role))
                    rating = rating - 1
            elif field == 'data_resources':
                if resource.data_resources.count() == 0:
                    checklist.append('There has to be at least one data resource attached to the record')
                    rating = rating - 1
            elif field == 'web_services':
                if resource.web_services.filter(service_language="urn:xml:lang:eng-CAN").count() == 0:
                    checklist.append('There has to be an English web service')
                    rating = rating - 1
                if resource.web_services.filter(service_language="urn:xml:lang:fra-CAN").count() == 0:
                    checklist.append('There has to be a French web service')
                    rating = rating - 1
            elif field == 'distribution_formats':
                if resource.distribution_formats.count() == 0:
                    checklist.append('There has to be at least one distribution format')
                    rating = rating - 1

        # next lets deal with special cases. This is the messiest one
        elif field.startswith("*"):
            field_split = field.replace("*", "").split(".")

            # the easier of the two is keywords. we must check to see if they are all bilingual
            if field_split[0] == "keyword":
                # I am taking the "easy" road and am hardcoding the test

                # examine all keywords, excluding ISO topic category which will be handled by FGP
                for keyword in resource.keywords.filter(~Q(keyword_domain_id=8)):
                    if keyword.text_value_fre is None or keyword.text_value_fre == "":
                        checklist.append('French value for keyword is needed for <a href="{}">{}</a>'.format(
                            reverse('inventory:keyword_detail', kwargs={'resource': resource.id, 'pk': keyword.id, }),
                            keyword.text_value_eng
                        ))
                        rating = rating - 1
                        translation_needed = True

                    elif keyword.text_value_eng is None or keyword.text_value_eng == "":
                        checklist.append("English value for keyword is needed for '{}'".format(
                            keyword.text_value_fre))
                        rating = rating - 1
                        translation_needed = True
            elif field_split[0] == "person":
                for person in resource.people.all():
                    if field_split[1] == "organization":
                        if len(field_split) == 2:  # means we are looking at the fk
                            if person.organization is None:
                                checklist.append("An organization for {} is missing.".format(person))
                                rating = rating - 1
                        elif field_split[2].startswith("name"):  # means we are looking at the org name
                            # if there is no organization, this will produce an error
                            try:
                                if person.organization.name_eng is None or person.organization.name_eng == "":
                                    checklist.append("An English organization name is needed for {}".format(person))
                                    rating = rating - 1
                                    translation_needed = True
                                if person.organization.name_fre is None or person.organization.name_fre == "":
                                    checklist.append("A French organization name is needed for {}".format(person))
                                    rating = rating - 1
                                    translation_needed = True
                            except AttributeError:
                                # two points are lost
                                rating = rating - 2
                        elif field_split[2].startswith("loc") and len(field_split) == 3:  # means we are looking at the fk
                            try:
                                if person.organization.location is None:
                                    checklist.append("A location is needed for '{}' which is the organization belonging to {}".format(
                                        person.organization, person))
                                    rating = rating - 1
                            except AttributeError:
                                # one point is lost
                                rating = rating - 1

                        elif field_split[2].startswith("loc") and field_split[3].startswith(
                                "loc"):  # means we are looking at the location name
                            # if there is no organization location, this will produce an error
                            try:
                                if person.organization.location.location_eng is None:
                                    checklist.append("An English organization location is needed for {}".format(person))
                                    rating = rating - 1
                                    translation_needed = True
                                if person.organization.location.location_fre is None:
                                    checklist.append("A French organization location is needed for {}".format(person))
                                    rating = rating - 1
                                    translation_needed = True
                            except AttributeError:
                                # two points are lost
                                rating = rating - 2

                    elif field_split[1].startswith("position"):
                        if person.position_eng is None or person.position_eng == "":
                            checklist.append("An English position name is needed for {}".format(person))
                            rating = rating - 1
                        if person.position_fre is None or person.position_fre == "":
                            checklist.append("A French position name is needed for {}".format(person))
                            rating = rating - 1

                        # now do a special bilingual field check to see if translation is needed
                        if (person.position_eng is not None and person.position_fre is None) or (
                                person.position_eng is None and person.position_fre is not None):
                            translation_needed = True

                    elif field_split[1].startswith("user"):
                        if person.user.email is None:
                            checklist.append("An email address is needed for {}".format(person))
                            rating = rating - 1

    html_list = ""
    for item in checklist:
        html_list += "<li>{}</li>".format(item)
    html_list = "<ul>{}</ul>".format(html_list)
    resource.completedness_report = html_list
    resource.completedness_rating = rating / max_rating
    resource.translation_needed = translation_needed
    resource.save()

    return html_list
