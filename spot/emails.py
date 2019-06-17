from django.template import loader

from_email = 'test@dfo-mpo.gc.ca'
admin_email = 'test@dfo-mpo.gc.ca'
stacy_email = 'test@dfo-mpo.gc.ca'


class EOIAcknowledgement:
    def __init__(self, object):
        self.title = 'EOI Receipt Acknowledgement Email'
        if object.language_id == 2:
            self.subject = 'Accusé de réception de votre déclaration d’intérêt'
        else:
            self.subject = "Expressions of Interest Receipt Acknowledgement"
        self.message = self.load_html_template(object)
        self.from_email = from_email
        self.to_list = [stacy_email]

    def load_html_template(self, object):
        t = loader.get_template('spot/emails/acknowledgement_of_receipt.html')
        context = {'object': object}
        rendered = t.render(context)
        return rendered

    def __str__(self):
        return "FROM: {}\nTO: {}\nSUBJECT: {}\nMESSAGE:{}".format(self.from_email, self.to_list, self.subject, self.message)
