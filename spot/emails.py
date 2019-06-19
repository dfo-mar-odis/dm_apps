from django.template import loader

from_email = 'test@dfo-mpo.gc.ca'
admin_email = 'test@dfo-mpo.gc.ca'
stacy_email = 'test@dfo-mpo.gc.ca'


class MasterEmail:
    def __init__(self, object, email_name):
        self.object = object
        self.email_name = email_name
        self.title = self.__get_title__()
        self.subject = self.__get_subject__()
        self.message = self.__load_template__()
        self.from_email = self.__get_from_email__()
        self.to_list = self.__get_to_list__()
        self.something_missing = self.__check_if_something_is_missing__()

    def __get_title__(self):
        if self.email_name == "eoi_acknowledgement":
            return 'EOI receipt acknowledgement email'
        if self.email_name == "negotiations":
            return 'Negotiations email'

    def __get_subject__(self):
        if self.email_name == "eoi_acknowledgement":
            return 'Accusé de réception de votre déclaration d’intérêt' if self.object.language_id == 2 else "Expressions of Interest Receipt Acknowledgement"
        elif self.email_name == "negotiations":
            return 'MISSING' if self.object.language_id == 2 else "MISSING"

    def __load_template__(self):
        if self.email_name == "eoi_acknowledgement":
            t = loader.get_template('spot/emails/acknowledgement_of_receipt.html')
        elif self.email_name == "negotiations":
            t = loader.get_template('spot/emails/negotiations.html')
        else:
            t = loader.get_template('spot/emails/email_template.html')
        context = {
            'object': self.object,
        }
        rendered = t.render(context)
        return rendered

    def __get_from_email__(self):
        return None

    def __get_to_list__(self):
        return None

    def __str__(self):
        # should make it so that MISSING is printed if an email is missing...
        my_from = self.from_email if self.from_email else "MISSING"
        my_to = self.to_list if self.to_list else "MISSING"
        return "FROM: {}\nTO: {}\nSUBJECT: {}\nMESSAGE:{}".format(my_from, my_to, self.subject, self.message)

    def __check_if_something_is_missing__(self):
        return True if "MISSING" in str(self) else False
