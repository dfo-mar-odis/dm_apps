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

# Load the notification (communication) preferences model
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

# Load the status model in Contact
status_con = [['Active ', ' Active(fr)'], ['Inactive ', ' Inactive(fr)']]
load_lookup(models.CotStatus, status_con)

# Load the expertise model in Contact
expertise = [['Expertise A', 'Expertise A(fr)'], ['Expertise B', 'Expertise B(fr)'],
             ['Expertise C', 'Expertise C(fr)'], ['Expertise D', 'Expertise D(fr)'],
             ['Expertise E', 'Expertise E(fr)']]
load_lookup(models.CotExpertise, expertise)

# Load the Scope Model
scopes = [['Regional ', ' Regional(fr)'], ['Zonal ', ' Zonal(fr)'], ['National ', ' National(fr)']]
load_lookup(models.ScpScope, scopes)

# Load the Status Model
status = [['On ', ' On(fr)'], ['In Planning ', ' In Planning(fr)'], ['Internal ', ' Internal(fr)'],
          ['Off ', ' Off(fr)'], ['Cancelled ', ' Cancelled(fr)'], ]
load_lookup(models.SttStatus, status)

# Load the Quarter Model
quarter = [['Spring (Apr-June) ', ' Spring (Apr-June)(fr)'], ['Summer (July-Sept) ', ' Summer (July-Sept)(fr)'],
           ['Fall (Oct-Dec) ', ' Fall (Oct-Dec)(fr)'], ['Winter (Jan-Mar) ', ' Winter (Jan-Mar)(fr)']]
load_lookup(models.MeqQuarter, quarter)

# Load the Month Model
months = [['January ', ' January(fr)'], ['February ', ' February(fr)'], ['March ', ' March(fr)'],
          ['April ', ' April(fr)'], ['May ', ' May(fr)'], ['June ', ' June(fr)'],
          ['July ', ' July(fr)'], ['August ', ' August(fr)'], ['September ', ' September(fr)'],
          ['October ', ' October(fr)'], ['November ', ' November(fr)'], ['December ', ' December(fr)']]
load_lookup(models.MemMeetingMonth, months)

# Load Location Province
locations = [['Alberta ', ' Alberta(fr)'], ['British Columbia ', ' British Columbia(fr)'],
             ['Manitoba ', ' Manitoba(fr)'], ['New Brunswick ', ' New Brunswick(fr)'],
             ['Newfoundland and Labrador ', ' Newfoundland and Labrador(fr)'],
             ['Northwest Territories ', ' Northwest Territories(fr)'], ['Nova Scotia ', ' Nova Scotia(fr)'],
             ['Nunavut ', ' Nunavut(fr)'], ['Ontario ', ' Ontario(fr)'],
             ['Prince Edward Island ', ' Prince Edward Island(fr)'],
             ['Quebec ', ' Quebec(fr)'], ['Saskatchewan ', ' Saskatchewan(fr)'], ['Yukon ', ' Yukon(fr)']]
load_lookup(models.LocLocationProv, locations)

# Load Location City
locations = [['Edmonton ', ' Edmonton(fr)'], ['Victoria ', ' Victoria(fr)'], ['Winnipeg ', ' Winnipeg(fr)'],
             ['Fredericton ', ' Fredericton(fr)'], ['St. Johns ', ' St. Johns(fr)'],
             ['Yellowknife ', ' Yellowknife(fr)'], ['Halifax ', ' Halifax(fr)'],
             ['Iqaluit ', ' Iqaluit(fr)'], ['Toronto ', ' Toronto(fr)'],
             ['Charlottetown ', ' Charlottetown(fr)'], ['Quebec City ', ' Quebec City(fr)'],
             ['Whitehorse ', ' Whitehorse(fr)']]

load_lookup(models.LocLocationCity, locations)

# Load Process Types
process = [['Advisory Meeting ', ' Advisory Meeting(fr)'], ['Science Response ', ' Science Response(fr)'],
           ['Frameworks ', ' Frameworks(fr)']]
load_lookup(models.AptAdvisoryProcessType, process)

# Load Expected Publication(s)
exp_publication = [['SAR/SSR ', ' SAR/SSR(fr)'], ['Research Document ', ' Research Document(fr)'],
                   ['Proceedings ', ' Proceedings(fr)']]

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

# load Publication O&M Costs Category
category = [['Translation ', ' Translation(fr)']]
load_lookup(models.PccPublicationCostCategory, category)

# load Publication Communication of Results Category
category = [['Media Lines ', ' Media Lines(fr)'], ['Briefing Material ', ' Briefing Material(fr)'],
            ['Other Communication Material ', ' Other Communication Material(fr)']]
load_lookup(models.PccPublicationComResultsCategory, category)

# load Meeting O&M Costs Category
category = [['Hospitality ', ' Hospitality(fr)'], ['Travel ', ' Travel(fr)'], ['Venue ', ' Venue(fr)'],
            ['Interpretation ', ' Interpretation(fr)'], ['Office ', ' Office(fr)'], ['Rentals ', ' Rentals(fr)'],
            ['Contractors/Consultants ', ' Contractors/Consultants(fr)'], ['Planning ', ' Planning(fr)']]
load_lookup(models.MccMeetingCostCategory, category)

# ----------------------------------------------------------------------------------------------------
# Yongcun: This part will be removed, we will use shared_models.Region in "models.py", it's just for
#          the temporarily usage on my desktop.
#
# Load Regions
# region = [['Pacific ', ' Pacific(fr)'],
#           ['Ontario & Prairie ', ' Ontario & Prairie'],
#           ['Arctic ', ' Arctic(fr)'],
#           ['Quebec ', ' Quebec(fr)'],
#           ['Gulf ', ' Gulf(fr)'],
#           ['Maritimes ', ' Maritimes(fr)'],
#           ['Newfoundland ', ' Newfoundland(fr)'],
#           ['National Capital ', ' National Capital(fr)']]

# load_lookup(models.MyRegion, region)
#
# ----------------------------------------------------------------------------------------------------

print("Data Load complete")
