from csas.models import CohHonorific, LanLanguage, CotType, NotNotificationPreference, SecSector, RolRole
from csas import models
###################################################################################################
# To run this script start the django shell:
#   >python manage.py shell
#
# Import the script:
#   >from csas.scripts import data_load
###################################################################################################


# load_lookup loads options into a model. Presumably the model is a simple lookup table with an auto generated ID field
# and a name field. The method will check to see if a name already exists in the lookup and will not add an options
# if it already exists
def load_lookup(model, options):

    for opt in options:
        # filter the model looking for this option. The option is only added if the filter returns a NoneType object
        if not model.objects.filter(name_en=opt[0]):
            model(name_en=opt[0], name_fr=opt[1]).save()
			
# Load the (Request) priority model
priorities = [['High ', ' High(fr)'], ['Medium ', ' Medium(fr)'], ['Low ', ' Low(fr)'],]
load_lookup(models.RepPriority, priorities)


# Load the (Request) proposed timing model
timings = [['By quarter ', ' By quarter(fr)'], ['By month ', ' By month(fr)'],]
load_lookup(models.RetTiming, timings)


# Load the honorific model
honorifics = [['Mr.', 'Mr. (fr)'], ['Mrs.', 'Mrs. (fr)'], ['Ms.', 'Ms. (fr)'], ['Dr.', 'Dr. (fr)'], ['Chief', 'Chief (fr)'], ['Capt.', 'Capt. (fr)'],]
load_lookup(CohHonorific, honorifics)

# --> Ask Tana if languages can be represented with one letter. I know there is some indigenous languages to add as well
# --> Till then language population is commented out
# Load the language model
languages = [['English', 'anglaise'], ['French', 'françis'],]
load_lookup(LanLanguage, languages)

# Load the contact type model
types = [['Government', 'Government (fr)'], ['Industry', 'Industry (fr)'], ['NGO', 'NGO (fr)'], ['Indigenous', 'Indigenous (fr)'], ['Consultant', 'Consultant (fr)'], ['Contractor', 'Contractor (fr)'],]
load_lookup(CotType, types)

# Load the notification preferences model
preferences = [['Phone', 'Phone (fr)'], ['Email', 'Email (fr)'], ['Fax', 'Fax (fr)'],]
load_lookup(NotNotificationPreference, preferences)

# Load Sector model
sectors = [['Science', 'Science (fr)'], ['Oceans', 'Oceans (fr)'], ['FFHPP', 'FFHPP (fr)'], ['SARA', 'SARA (fr)'], ['RM', 'RM (fr)'], ['AMD', 'AMD (fr)'],]
load_lookup(SecSector, sectors)

# Load the role model
roles = [['Regional Coordinator', 'Regional Coordinator (fr)'], ['Regional Science Advisor', 'Regional Science Advisor (fr)'], ['Regional Admin', 'Regional Admin (fr)'], ['Director', 'Director (fr)'],]
load_lookup(RolRole, roles)

# Load the Scope Model
scopes = [['Regional', 'Regional (fr)'], ['Zonal', 'Zonal (fr)'], ['National', 'National (fr)']]
load_lookup(models.ScpScope, scopes)

# Load the Status Model
status = [['On', 'On'], ['In Planning', 'In Planning'], ['Internal', 'Internal'], ['Off', 'Off'], ['Cancelled', 'Cancelled'], ]
load_lookup(models.SttStatus, status)

# Load the Quarter Model
quarter = [['Spring', 'Spring (fr)'], ['Summer', 'Summar (fr)'], ['Fall', 'Fall (fr)'], ['Winter', 'Winter (fr)'], ]
load_lookup(models.MeqQuarter, quarter)

# Load Locations
locations = [['test', 'test (fr)']]
load_lookup(models.LocLocation, locations)

# Load Process Types
process = [['test process', 'test process (fr)']]
load_lookup(models.AptAdvisoryProcessType, process)