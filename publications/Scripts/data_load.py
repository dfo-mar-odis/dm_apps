import csv
from django.db.utils import IntegrityError, DataError
import datetime
from publications import models


def process_lookup(file_name, mod):
    # This method is intended to work with a file that is ONLY themes
    data_file = open(file_name, encoding='utf-8')
    reader = csv.reader(data_file, delimiter=',')

    # skip the header row
    next(reader, None)

    val_list = []
    for line in reader:
        if line and line[0].strip():
            vals = [t.strip().upper() for t in line[0].split(' | ')]
            for val in vals:
                if val and val not in val_list:
                    val_list.append(val)

    for val in val_list:
        try:
            mod(name=val).save()
        except IntegrityError:
            pass
        except DataError:
            print("String too long:\n'" + str(val) + "'\n")


def add_text(model, val_array, mod_name):
    print("Adding " + mod_name + " to project: " + str(project))
    for val in val_array:
        try:
            if val and not model.objects.filter(project=project, value=val).exists():
                mod = model(project=project, value=val)
                mod.save()
        except DataError:
            print("Error adding " + mod_name + ": " )
            print(val)


def add_lookup(model, val_array, var):
    dirty = False
    for val in val_array:
        if not val:
            continue

        obj = model.objects.get(name__exact=val)
        try:
            var.get(id=obj.id)
        except model.DoesNotExist:
            var.add(obj)
            dirty = True

    return dirty


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

data_tp_file_name = r'E:\Projects\Python\publications-inventory\pub_data2.csv'

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
# 14 Spatial data product year
# *15 Computer environment
# 16 Software Libraries
# 17 Method of approach
# 18 FGP Link
# 19 code or data site
# 20 contact (keep as free text)
# 21 DFO Contact (create code list)
# 22 Geographic scope
# 23 Geographic coordinates
# 24 Spatial Scale
# *25 Pub year
# 26 Organization
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

    computer_environment = [sm.strip() for sm in line[15].split(' | ')]

    year = line[25]
    if '-' in year:
        year = year.split('-')[1]

    sites = [s.strip() for s in line[29].split(' | ')]

    publications = [p.strip() for p in line[30].split(' | ')]

    try:
        project = models.Project.objects.get(title=project_title)
    except models.Project.MultipleObjectsReturned:
        print("found multiple projects matching:\n\n'" + project_title + "'\n\n")
        exit()
    except models.Project.DoesNotExist:
        print("Creating new publication: " + project_title)
        project = models.Project(title=project_title, abstract=description)
        project.save()

    print("Adding Themes")
    if add_lookup(models.Theme, themes, project.theme):
        project.save()

    print("Adding Human Components")
    if add_lookup(models.HumanComponent, humans, project.human_component):
        project.save()

    print("Adding Pillars")
    if add_lookup(models.Pillar, pillars, project.sustainability_pillar):
        project.save()

    print("Adding Linkages")
    if add_lookup(models.ProgramLinkage, linkages, project.program_linkage):
        project.save()

    print("Adding Ecosystems")
    if add_lookup(models.EcosystemComponent, ecosystems, project.ecosystem_component):
        project.save()

    if project:
        add_text(models.ComputerEnvironment, computer_environment, "computer environment")
        add_text(models.SourceDataInternal, source_internal, "source data (internal)")
        add_text(models.SourceDataExternal, source_external, "source data (external)")
        add_text(models.SpatialDataProduct, spatial_data_product, "spatial data product")
        add_text(models.SpatialManagementDesignation, spatial_management, "spatial management")
        add_text(models.Site, sites, "sites")
        add_text(models.Publication, publications, "publications")
