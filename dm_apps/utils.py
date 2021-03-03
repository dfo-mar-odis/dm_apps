import boto3
from Levenshtein._levenshtein import distance
from botocore.config import Config
from botocore.exceptions import ClientError
from decouple import config
from django.conf import settings
from django.core.mail import send_mail as django_send_mail
from python_http_client import BadRequestsError
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, Personalization

from lib.templatetags.custom_filters import nz


def get_azure_connection_dict():
    key_list = [
        'AAD_APP_ID',  # needed
        'AAD_APP_SECRET',  # needed
        'AAD_REDIRECT',  # needed?
        'AAD_SCOPES',
        'AAD_AUTHORITY',
        'AAD_AUTHORIZE_ENDPOINT',
        'AAD_TOKEN_ENDPOINT',
    ]
    my_dict = dict()
    for key in key_list:
        if key == 'AAD_SCOPES':
            my_dict[key] = "openid user.read"
        elif key == 'AAD_AUTHORITY':
            my_dict[key] = "https://login.microsoftonline.com/1594fdae-a1d9-4405-915d-011467234338"
        elif key == 'AAD_AUTHORIZE_ENDPOINT':
            my_dict[key] = "/oauth2/v2.0/authorize"
        elif key == 'AAD_TOKEN_ENDPOINT':
            my_dict[key] = "/oauth2/v2.0/token"
        else:
            casting = str
            my_dict[key] = config(key, cast=casting, default="")
    return my_dict


def azure_ad_values_exist(connection_dict):
    key_list = [
        'AAD_APP_ID',
        'AAD_APP_SECRET',
        'AAD_REDIRECT',
        # 'AAD_SCOPES',
        # 'AAD_AUTHORITY',
        # 'AAD_AUTHORIZE_ENDPOINT',
        # 'AAD_TOKEN_ENDPOINT',
    ]
    # if all values are present, below expression should be evaluated as False
    there_is_something_missing = False in [connection_dict[key] != "" for key in key_list]
    return there_is_something_missing is False


def db_connection_values_exist(connection_dict):
    key_list = [
        # 'DB_MODE',
        'DB_HOST',
        'DB_PORT',
        'DB_NAME',
        'DB_USER',
        'DB_PASSWORD',
    ]
    # if all values are present, below expression should be evaluated as False
    there_is_something_missing = False in [connection_dict[key] != "" for key in key_list]
    return there_is_something_missing is False


def get_db_connection_dict():
    key_list = [
        'DB_MODE',
        'DB_HOST',
        'DB_PORT',
        'DB_NAME',
        'DB_USER',
        'DB_PASSWORD',
    ]
    my_dict = dict()
    for key in key_list:
        casting = int if "port" in key.lower() else str
        default_value = 3306 if "port" in key.lower() else ""
        try:
            my_dict[key] = config(key, cast=casting, default=default_value)
        except ValueError:
            my_dict[key] = ""

    return my_dict


def custom_send_mail(subject=None, html_message=None, from_email=None, recipient_list=None, text_message=None, email_instance=None):
    """
    The role of this function is to handle the sending of an email message based on the configuration of the project setting.py file.
    - If settings.USE_SENDGRID = True, the mail will be sent with the python sendgrid package using the sendgrid REST api
    - If settings.USE_SMTP_EMAIL = True, the email will be send with django's send_mail function.
    - If settings.USE_SMTP_EMAIL and settings.USE_SENDGRID are both false, no email will be sent.

    :param subject:
    :param html_message:
    :param from_email:
    :param recipient_list:
    :return:
    """
    if email_instance:
        subject = email_instance.get_subject()
        text_message = email_instance.get_text_message()
        html_message = email_instance.get_html_message()
        from_email = email_instance.get_from_email()
        recipient_list = email_instance.get_recipient_list()

    if settings.USE_SENDGRID:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        from_email = Email(from_email)
        to_list = Personalization()
        for email in set(recipient_list):
            to_list.add_to(Email(email))
        mail = Mail(
            from_email=from_email,
            to_emails=None,
            subject=subject,
            html_content=html_message,
            plain_text_content=text_message
        )
        mail.add_personalization(to_list)
        try:
            sg.send(mail)
        except BadRequestsError:
            print("bad request. email not sent")

    elif settings.USE_AWS_SES:
        my_config = Config(
            region_name='ca-central-1',
            signature_version='v4',
            retries={
                'max_attempts': 10,
                'mode': 'standard'
            }
        )
        # from https://docs.aws.amazon.com/ses/latest/DeveloperGuide/send-using-sdk-python.html
        # The character encoding for the email.
        CHARSET = "UTF-8"
        # Create a new SES resource and specify a region.
        client = boto3.client('ses', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY, config=my_config)
        # Try to send the email.
        try:
            # Provide the contents of the email.
            response = client.send_email(
                Destination={
                    'ToAddresses': recipient_list
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': CHARSET,
                            'Data': nz(html_message, ''),
                        },
                        'Text': {
                            'Charset': CHARSET,
                            'Data': nz(text_message, ''),
                        },
                    },
                    'Subject': {
                        'Charset': CHARSET,
                        'Data': subject,
                    },
                },
                Source=from_email,
            )
        # Display an error if something goes wrong.
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])

    elif settings.USE_SMTP_EMAIL:
        django_send_mail(
            subject=subject,
            message=nz(text_message, ''),
            html_message=html_message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False
        )

    else:
        print('No email configuration present in application...')
        if email_instance:
            print(email_instance)
        else:
            print("FROM: {}\nTO: {}\nSUBJECT: {}\nMESSAGE:{}".format(from_email, recipient_list, subject, html_message))


def compare_strings(str1, str2):
    def __strip_string__(string):
        return str(string.lower().replace(" ", "").split(",")[0])

    try:
        return distance(__strip_string__(str1), __strip_string__(str2))
    except AttributeError:
        return 9999
