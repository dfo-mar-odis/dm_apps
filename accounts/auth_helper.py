import yaml
from requests_oauthlib import OAuth2Session
import os
import time
from decouple import config, UndefinedValueError

# This is necessary for testing with non-HTTPS localhost
# Remove this if deploying to production
from dm_apps import utils

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# This is necessary because Azure does not guarantee
# to return scopes in the same case and order as requested
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
os.environ['OAUTHLIB_IGNORE_SCOPE_CHANGE'] = '1'

# Load the azure_oauth_settings.yml file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

aad_connection_dict = utils.get_azure_connection_dict()

if utils.azure_ad_values_exist(aad_connection_dict):
    authorize_url = '{0}{1}'.format(aad_connection_dict['AAD_AUTHORITY'], aad_connection_dict['AAD_AUTHORIZE_ENDPOINT'])
    token_url = '{0}{1}'.format(aad_connection_dict['AAD_AUTHORITY'], aad_connection_dict['AAD_TOKEN_ENDPOINT'])


# Method to generate a sign-in url
def get_sign_in_url():
    # Initialize the OAuth client
    aad_auth = OAuth2Session(aad_connection_dict['AAD_APP_ID'],
                             scope=aad_connection_dict['AAD_SCOPES'],
                             redirect_uri=aad_connection_dict['AAD_REDIRECT'])

    sign_in_url, state = aad_auth.authorization_url(authorize_url, prompt='login')

    return sign_in_url, state


# Method to exchange auth code for access token
def get_token_from_code(callback_url, expected_state):
    # Initialize the OAuth client
    aad_auth = OAuth2Session(aad_connection_dict['AAD_APP_ID'],
                             state=expected_state,
                             scope=aad_connection_dict['AAD_SCOPES'],
                             redirect_uri=aad_connection_dict['AAD_REDIRECT'])

    token = aad_auth.fetch_token(token_url,
                                 client_secret=aad_connection_dict['AAD_APP_SECRET'],
                                 authorization_response=callback_url)

    return token


def store_token(request, token):
    request.session['oauth_token'] = token


def store_user(request, user):
    request.session['user'] = {
        'is_authenticated': True,
        'name': user['displayName'],
        'email': user['mail'] if (user['mail'] != None) else user['userPrincipalName']
    }


def get_token(request):
    token = request.session['oauth_token']
    if token != None:
        # Check expiration
        now = time.time()
        # Subtract 5 minutes from expiration to account for clock skew
        expire_time = token['expires_at'] - 300
        if now >= expire_time:
            # Refresh the token
            aad_auth = OAuth2Session(aad_connection_dict['AAD_APP_ID'],
                                     token=token,
                                     scope=aad_connection_dict['AAD_SCOPES'],
                                     redirect_uri=aad_connection_dict['AAD_REDIRECT'])

            refresh_params = {
                'client_id': aad_connection_dict['AAD_APP_ID'],
                'client_secret': aad_connection_dict['AAD_APP_SECRET'],
            }
            new_token = aad_auth.refresh_token(token_url, **refresh_params)

            # Save new token
            store_token(request, new_token)

            # Return new access token
            return new_token

        else:
            # Token still valid, just return it
            return token


def remove_user_and_token(request):
    if 'oauth_token' in request.session:
        del request.session['oauth_token']

    if 'user' in request.session:
        del request.session['user']
