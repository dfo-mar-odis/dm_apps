import argparse
import os

def nz(value, arg):
    """if a value is equal to None, this function will return arg instead"""
    if value is None or value == "":
        return arg
    else:
        return value

parser = argparse.ArgumentParser()
# parser.add_argument('--app-id', help='application id issued by AAD')
# parser.add_argument('--secret-key', help='django secret key')
# parser.add_argument('--google-api-key', help='google api key')
# parser.add_argument('--sendgrid-api-key', help='sendgrid api key')
parser.add_argument('--azure-storage-account-name', help='name of azure storage blob account')
parser.add_argument('--azure-storage-secret-key', help='secret key for azure storage blob account')
parser.add_argument('--db-host', help='')
parser.add_argument('--db-port', help='')
parser.add_argument('--db-name', help='')
parser.add_argument('--db-user', help='')
parser.add_argument('--deployment-stage', help='select one of the following: DEV, TEST, PROD')
parser.add_argument('--db-password', help='')
parser.add_argument('--in-pipeline', help='')
#
# parser.add_argument('--email-host', help='')
# parser.add_argument('--email-user', help='')
# parser.add_argument('--email-password', help='')
# parser.add_argument('--email-port', help='')
# parser.add_argument('--email-use-tls', help='')
#
# parser.add_argument('--oauth-app-id', help='')
# parser.add_argument('--oauth-app-secret', help='')
# parser.add_argument('--oauth-redirect', help='')
# parser.add_argument('--oauth-scopes', help='')
# parser.add_argument('--oauth-authority', help='')
# parser.add_argument('--oauth-authorize-endpoint', help='')
# parser.add_argument('--oauth-token-endpoint', help='')
#
# parser.add_argument('--azure-storage-account-name', help='azure blob storage account name')
parser.add_argument('--devops-build-number', help='Devops artifact build number')




args = parser.parse_args()

new_file = os.path.join(".env")
with open(new_file, 'w') as write_file:
    # write_file.write("# General\n")
    # write_file.write("SECRET_KEY = {}\n".format(nz(args.secret_key, "")))
    # write_file.write("GOOGLE_API_KEY = {}\n".format(nz(args.google_api_key, "")))
    # write_file.write("SENDGRID_API_KEY = {}\n".format(nz(args.sendgrid_api_key, "")))
    #
    # write_file.write("\n# Credentials for Database\n")
    write_file.write("DEPLOYMENT_STAGE = {}\n".format(nz(args.deployment_stage, "")))
    write_file.write("DB_HOST = {}\n".format(nz(args.db_host, "")))
    write_file.write("DB_PORT = {}\n".format(nz(args.db_port, "")))
    write_file.write("DB_NAME = {}\n".format(nz(args.db_name, "")))
    write_file.write("DB_USER = {}\n".format(nz(args.db_user, "")))
    write_file.write("DB_PASSWORD = {}\n".format(nz(args.db_password, "")))
    write_file.write("AZURE_STORAGE_ACCOUNT_NAME = {}\n".format(nz(args.azure_storage_account_name, "")))
    write_file.write("AZURE_STORAGE_SECRET_KEY = {}\n".format(nz(args.azure_storage_secret_key, "")))
    write_file.write("IN_PIPELINE = {}\n".format(nz(args.in_pipeline, False)))
    #
    # write_file.write("\n# Credentials for Email Service\n")
    # write_file.write("EMAIL_HOST = {}\n".format(nz(args.email_host, "")))
    # write_file.write("EMAIL_HOST_USER = {}\n".format(nz(args.email_user, "")))
    # write_file.write("EMAIL_HOST_PASSWORD = {}\n".format(nz(args.email_password, "")))
    # write_file.write("EMAIL_PORT = {}\n".format(nz(args.email_port, "")))
    # write_file.write("EMAIL_USE_TLS = {}\n".format(nz(args.email_use_tls, "")))
    #
    # write_file.write("\n# Oauth Credentials for AAD\n")
    # write_file.write("app_id = {}\n".format(nz(args.oauth_app_id, "")))
    # write_file.write("app_secret = {}\n".format(nz(args.oauth_app_secret, "")))
    # write_file.write("redirect = {}\n".format(nz(args.oauth_redirect, "")))
    # write_file.write("scopes = {}\n".format(nz(args.oauth_scopes, "")))
    # write_file.write("authority = {}\n".format(nz(args.oauth_authority, "")))
    # write_file.write("authorize_endpoint = {}\n".format(nz(args.oauth_authorize_endpoint, "")))
    # write_file.write("token_endpoint = {}\n".format(nz(args.oauth_token_endpoint, "")))
    #
    # write_file.write("\n# Oauth Credentials for AAD\n")
    # write_file.write("AZURE_STORAGE_ACCOUNT_NAME = {}\n".format(nz(args.azure_storage_account_name, "")))
    write_file.write("DEVOPS_BUILD_NUMBER = {}\n".format(nz(args.devops_build_number, "")))


