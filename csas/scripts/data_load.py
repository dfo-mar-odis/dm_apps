from typing import List

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
        if not model.objects.filter(name=opt[0]):
            model(name=opt[0], nom=opt[1]).save()


# Load the (Request) priority model
priorities = [['High ', ' High(fr)'], ['Medium ', ' Medium(fr)'], ['Low ', ' Low(fr)'], ]
load_lookup(models.RepPriority, priorities)


# Load the (Request) proposed timing model
timings = [['By quarter ', ' By quarter(fr)'], ['By month ', ' By month(fr)'], ]
load_lookup(models.RetTiming, timings)


# Load the (Request) status model
req_status = [['Withdrawn ', ' Withdrawn(fr)'], ['CSAS Office Reviewing ', ' CSAS Office Reviewing(fr)'],
              ['RDS Reviewing ', ' RDS Reviewing(fr)'], ['Decision Made ', ' Decision Made(fr)'], ]
load_lookup(models.ResStatus, req_status)


# Load the (Request) decision model
decision = [['On ', ' On(fr)'], ['Off ', ' Off(fr)'], ['Tentative ', ' Tentative(fr)'], ]
load_lookup(models.RedDecision, decision)


# Load the (Request) decision explanation model
decision_exp = [['Planned Deferred (lower priority) ', ' Planned Deferred (lower priority)(fr)'],
                ['Client Withdrawal ', ' Client Withdrawal(fr)'],
                ['Capacity Issues (e.g., no science staff) ', 'Capacity Issues (e.g., no science staff)(fr)'],
                ['Unexpected Delays/Unforeseen Circumstances )', ' Unexpected Delays/Unforeseen Circumstances(fr)'], ]
load_lookup(models.RdeDecisionExplanation, decision_exp)


# Load the honorific model
honorifics = [['Mr. ', ' Mr.(fr)'], ['Mrs. ', ' Mrs.(fr)'], ['Ms. ', ' Ms.(fr)'], ['Dr. ', ' Dr.(fr)'],
              ['Chief ', ' Chief(fr)'], ['Capt. ', ' Capt.(fr)'], ]
load_lookup(CohHonorific, honorifics)

# --> Ask Tana if languages can be represented with one letter. I know there is some indigenous languages to add as well
# --> Till then language population is commented out
# Load the language model
languages = [['English ', ' Anglaise'], ['French ', ' Françis'], ]
load_lookup(LanLanguage, languages)

# Load the contact type model
types = [['Government ', ' Government(fr)'], ['Industry ', ' Industry(fr)'], ['NGO ', ' NGO(fr)'],
         ['Indigenous ', ' Indigenous(fr)'], ['Consultant ', ' Consultant(fr)'], ['Contractor ', ' Contractor(fr)'], ]
load_lookup(CotType, types)

# Load the notification preferences model
preferences = [['Phone ', ' Phone(fr)'], ['E-mail ', ' E-mail(fr)'], ['Fax ', ' Fax(fr)'], ]
load_lookup(NotNotificationPreference, preferences)

# Load Sector model
sectors = [['Science ', ' Science(fr)'], ['Oceans ', ' Oceans(fr)'], ['FFHPP ', ' FFHPP(fr)'], ['SARA ', ' SARA(fr)'],
           ['RM ', ' RM(fr)'], ['AMD ', ' AMD(fr)'], ]
load_lookup(SecSector, sectors)

# Load the role model
roles = [['Regional Coordinator ', ' Regional Coordinator(fr)'],
         ['Regional Science Advisor ', ' Regional Science Advisor(fr)'],
         ['Regional Admin ', ' Regional Admin(fr)'], ['Director ', ' Director(fr)'], ]
load_lookup(RolRole, roles)

# Load the Scope Model
scopes = [['Regional ', ' Regional(fr)'], ['Zonal ', ' Zonal(fr)'], ['National ', ' National(fr)']]
load_lookup(models.ScpScope, scopes)

# Load the Status Model
status = [['On ', ' On(fr)'], ['In Planning ', ' In Planning(fr)'], ['Internal ', ' Internal(fr)'],
          ['Off ', ' Off(fr)'], ['Cancelled ', ' Cancelled(fr)'], ]
load_lookup(models.SttStatus, status)

# Load the Quarter Model
quarter = [['Spring ', ' Spring(fr)'], ['Summer ', ' Summar(fr)'], ['Fall ', ' Fall(fr)'], ['Winter ', ' Winter(fr)'], ]
load_lookup(models.MeqQuarter, quarter)

# Load Locations
locations = [['Victoria ', ' Victoria(fr)'], ['Edmonton ', 'Edmonton(fr)'], ['Winnipeg ', ' Winnipeg(fr)'],
             ['Toronto ', ' Toronto(fr)'], ['Quebec City ', ' Quebec City(fr)'], ['Halifax ', ' Halifax(fr)'],
             ['Charlottetown ', ' Charlottetown(fr)']]
load_lookup(models.LocLocation, locations)

# Load Process Types
process = [['Process Type A ', ' Process Type A(fr)'], ['Process Type B ', ' Process Type B(fr)'],
           ['Process Type C ', ' Process Type C(fr)'], ['Process Type D ', ' Process Type D(fr)']]
load_lookup(models.AptAdvisoryProcessType, process)

# Load Expected Publication(s)
exp_publication = [['SAR/SSR ', ' SAR/SSR(fr)'], ['Research Document ', ' Research Document(fr)'],
                   ['Proceedings ', ' Proceedings(fr)'], ['Attendance List ', ' Attendance List(fr)'],
                   ['Briefing Note(s) ', ' Briefing Notes(s)(fr)']]
load_lookup(models.MepMeetingExpectedPublication, exp_publication)

# Load Terms of Reference
reference = [['SAR/SSR ', ' SAR/SSR(fr)'], ['Research Document ', ' Research Document(fr)'],
             ['Proceedings ', ' Proceedings(fr)'], ['Attendance List ', ' Attendance List(fr)'],
             ['Briefing Note(s) ', ' Briefing Notes(s)(fr)']]
load_lookup(models.MdfMeetingDocsRef, reference)

# load Series
series = [['SAR ', ' SAR(fr)'], ['SR ', ' SR(fr)'], ['RES ', ' RES(fr)'], ['PRO ', ' PRO(fr)']]
load_lookup(models.PsePublicationSeries, series)

# load Publication Status
pub_status = [['In Approvals ', ' In Approvals(fr)'], ['Submitted for Posting ', ' Submitted for Posting(fr)']]
load_lookup(models.PusPublicationStatus, pub_status)

# load Publication Translation Status
trans_status = [['Not Translation ', ' Not Translation(fr)'],
                ['Submitted for Translation ', ' Submitted for Translation(fr)'],
                ['Back from Translation ', ' Back from Translation(fr)'], ['Complete ', ' Complete(fr)']]
load_lookup(models.PtsPublicationTransStatus, trans_status)

# load Publication Target Language
target_lang = [['English ', ' English(fr)'], ['French ', ' French(fr)'],
               ['Inuktitut (& dialects) ', ' Inuktitut (& dialects) (fr)']]
load_lookup(models.PtlPublicationTargetLanguage, target_lang)

# load Publication Translation Urgent Request
urgent_req = [['Yes ', ' Yes(fr)'], ['No ', ' No(fr)']]
load_lookup(models.PurPublicationUrgentRequest, urgent_req)

# ----------------------------------------------------------------------------------------------------
# Yongcun: This part will be removed, we will use shared_models.Region in "models.py", it's just for
#          the temporarily usage on my desktop.
#
# Load Regions
region = [['Pacific ', ' Pacific(fr)'], ['Central & Arctic ', ' Central & Arctic(fr)'], ['Quebec ', ' Quebec(fr)'],
          ['Gulf ', ' Gulf(fr)'], ['Maritimes ', ' Maritimes(fr)'], ['Newfoundland ', ' Newfoundland(fr)'],
          ['National ', ' National(fr)']]
load_lookup(models.MyRegion, region)
#
# ----------------------------------------------------------------------------------------------------

print("Data Load complete")
