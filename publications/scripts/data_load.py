import csv
import logging

from django.db.utils import IntegrityError, DataError

from publications import models
from shared_models import models as shared_models

logging.basicConfig(level=logging.WARNING, filename="data_load.log", filemode="w")

def process_lookup(file_name, mod, delim=",", complex_parse=False, uppercase=True):
    # This method is intended to work with a file that is ONLY themes
    data_file = open(file_name, encoding='utf-8')
    reader = csv.reader(data_file, delimiter=delim)

    # skip the header row
    next(reader, None)

    val_list = []
    for line in reader:
        if line and line[0].strip():

            if not complex_parse:
                vals = [t.strip() for t in line[0].split(' | ')]
            else:
                vals = [t.strip() for t in line[0].replace(' and ', ' | ').replace(', ', ' | ').split(' | ')]

            for val in vals:
                if val and val not in val_list:
                    val_list.append(val.upper() if uppercase else val)

    for val in val_list:
        try:
            mod(name=val).save()
        except IntegrityError:
            pass
        except DataError:
            logging.error("String too long:\n'" + str(val) + "'\n")


def add_text(model, val_array):

    for val in val_array:
        try:
            if val and not model.objects.filter(project=project, value=val).exists():
                logging.debug("Adding " + model._meta.verbose_name + " to project: " + str(project))
                mod = model(project=project, value=val)
                mod.save()
        except DataError:
            logging.error("Error adding " + model._meta.verbose_name + ": ")
            logging.error(val)


def add_lookup(model, val_array, var):
    dirty = False

    for val in val_array:
        if not val:
            continue

        try:
            obj = model.objects.get(name__exact=val)
            try:
                var.get(id=obj.id)
            except model.DoesNotExist:
                logging.debug("Adding " + model._meta.verbose_name + " to project: " + str(project))
                var.add(obj)
                dirty = True
        except model.DoesNotExist:
            logging.error("=========================== Err " + model._meta.verbose_name + ": Could not find value matching: " + str(val))
            logging.error("Attempting to add")
            try:
                model(name=val).save()
                add_lookup(model, val_array, var)
                logging.error("Success")
            except:
                logging.error("Fail")
            # exit()

    if dirty:
        project.save()


data_theme_file_name = r'E:\Projects\Python\publications-inventory\Themes.csv'
process_lookup(data_theme_file_name, models.Theme)

data_human_file_name = r'E:\Projects\Python\publications-inventory\HumanComponents.csv'
process_lookup(data_human_file_name, models.HumanComponent)

data_pillars_file_name = r'E:\Projects\Python\publications-inventory\pillars.csv'
process_lookup(data_pillars_file_name, models.Pillar)

data_linkage_file_name = r'E:\Projects\Python\publications-inventory\Linkage.csv'
process_lookup(data_linkage_file_name, models.ProgramLinkage)

data_ecosystem_file_name = r'E:\Projects\Python\publications-inventory\Ecosystem.csv'
process_lookup(data_ecosystem_file_name, models.EcosystemComponent)

data_geoscope_file_name = r'E:\Projects\Python\publications-inventory\Geo-Scope.csv'
process_lookup(data_geoscope_file_name, models.GeographicScope)

data_internal_contact_file_name = r'E:\Projects\Python\publications-inventory\dfo-contacts.txt'
process_lookup(data_internal_contact_file_name, models.InternalContact, delim="|", complex_parse=False, uppercase=False)

data_organization_file_name = r'E:\Projects\Python\publications-inventory\organizations.txt'
process_lookup(data_organization_file_name, models.Organization, delim="|", complex_parse=False, uppercase=False)

data_spatial_scale_file_name = r'E:\Projects\Python\publications-inventory\spatial-scale.txt'
process_lookup(data_spatial_scale_file_name, models.SpatialScale)

data_tp_file_name = r'E:\Projects\Python\publications-inventory\pub_data4.csv'

tp_reader = csv.reader(open(data_tp_file_name, encoding='utf-8'), delimiter=',')

# skip the header line
next(tp_reader, None)

# 0 Projects_id - not used
# *1 Themes
# *2 Project title
# *3 Human Component
# *4 Ecosystem Component
# *5 Spatial Management
# *6 Pillar of sustainability
# *7 Linkage to Program
# *8 Description
# *9 Source data (external)
# 10 Source data year (external) - ignore for now
# *11 Source data (internal)
# 12 Source data year (internal) - ignore for now
# *13 Spatial data product
# *14 Spatial data product year
# *15 Computer environment
# *16 Software Libraries
# *17 Method of approach
# *18 FGP Link
# *19 code or data site
# *20 contact (keep as free text)
# *21 DFO Contact (create code list)
# *22 Geographic scope
# *23 Geographic coordinates
# *24 Spatial Scale
# *25 Pub year
# *26 Organization
# 27 DFO Region
# 28 DFO Division
# *29 Sites
# *30 Publications
for line in tp_reader:

    project_title = line[2].replace("\"", "")

    themes = [t.strip().upper() for t in line[1].split(' | ')]

    humans = [h.strip().upper() for h in line[3].split(' | ')]

    ecosystems = [e.strip().upper() for e in line[4].split(' | ')]

    spatial_management = [sm.strip() for sm in line[5].split(' | ')]

    pillars = [p.strip().upper() for p in line[6].split(' | ')]

    linkages = [l.strip().upper() for l in line[7].split(' | ')]

    description = line[8].replace("\"", "").replace('\\n', '\n')

    source_internal = [sm.strip() for sm in line[9].split(' | ')]

    source_external = [sm.strip() for sm in line[11].split(' | ')]

    spatial_data_product = [sm.strip() for sm in line[13].split(' | ')]

    spatial_data_product_year = [sm.strip() for sm in line[14].split(',')]

    computer_environment = [sm.strip() for sm in line[15].split(' | ')]

    computer_libraries = [sm.strip() for sm in line[16].split(' | ')]

    method = line[17].replace("\"", "").replace('\\n', '\n')

    fgp_linkages = [l.strip() for l in line[18].split(' | ')]

    code_site = [l.strip() for l in line[19].split(' | ')]

    external_contact = [l.strip() for l in line[20].split(' | ')]

    internal_contact = [l.strip() for l in line[21].split(' | ')]

    geographic_scope = [l.strip().upper() for l in line[22].replace(' and ', ' | ').replace(', ', ' | ').split(' | ')]

    coordinates = [l.strip() for l in line[23].strip().replace("°E", "").replace("°N", "").split(" ")] if line[23].strip() else None

    spatial_scale = [l.strip().upper() for l in line[24].split(' | ')]

    year = line[25]
    if '-' in year:
        sp_year = year.split('-')
        if sp_year[1]:
            year = sp_year[1]
        else:
            year = sp_year[0]

    organizations = [s.strip() for s in line[26].split(' | ')]

    divisions = [s.strip() for s in line[28].strip().split(' | ')] if line[28].strip() else None

    sites = [s.strip() for s in line[29].split(' | ')]

    publications = [p.strip() for p in line[30].split(' | ')]

    try:
        project = models.Project.objects.get(title=project_title)
    except models.Project.MultipleObjectsReturned:
        logging.error("found multiple projects matching:\n\n'" + project_title + "'\n\n")
        exit()
    except models.Project.DoesNotExist:
        logging.error("Creating new publication: " + project_title)
        project = models.Project(title=project_title, abstract=description)
        project.save()

    if year:
        logging.debug("Setting year")
        project.year = year
        project.save()

    if coordinates:
        logging.debug("coordinates" + str(coordinates))
        coord = models.GeoCoordinate(north_south=coordinates[0], east_west=coordinates[1])
        coord.save()
        project.coordinates = coord
        project.save()

    if not project.method and method:
        logging.debug("Setting Method")
        project.method = method
        project.save()

    if project:
        add_lookup(models.Theme, themes, project.theme)
        add_lookup(models.HumanComponent, humans, project.human_component)
        add_lookup(models.Pillar, pillars, project.sustainability_pillar)
        add_lookup(models.ProgramLinkage, linkages, project.program_linkage)
        add_lookup(models.EcosystemComponent, ecosystems, project.ecosystem_component)
        add_lookup(models.GeographicScope, geographic_scope, project.geographic_scope)
        add_lookup(models.InternalContact, internal_contact, project.dfo_contact)
        add_lookup(models.Organization, organizations, project.organization)
        add_lookup(models.SpatialScale, spatial_scale, project.spatial_scale)

        add_text(models.ComputerEnvironment, computer_environment)
        add_text(models.SourceDataInternal, source_internal)
        add_text(models.SourceDataExternal, source_external)
        add_text(models.SpatialDataProduct, spatial_data_product)
        add_text(models.SpatialDataProductYear, spatial_data_product_year)
        add_text(models.ComputerLibraries, computer_libraries)
        add_text(models.SpatialManagementDesignation, spatial_management)
        add_text(models.FgpLinkage, fgp_linkages)
        add_text(models.Site, sites)
        add_text(models.CodeSite, code_site)
        add_text(models.ExternalContact, external_contact)
        add_text(models.Publication, publications)

        if divisions:
            proj_div = [div for div in project.division.values_list()]
            dirty = False
            for division in divisions:
                logging.debug("division: " + str(division))
                try:
                    div = shared_models.Division.objects.get(abbrev=division)
                    if not div in proj_div:
                        project.division.add(div)
                        dirty = True
                except shared_models.Division.DoesNotExist:
                    logging.error("============ Division " + division + " doesn't exist")

            if dirty:
                project.save()