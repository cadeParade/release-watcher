from xml.dom import minidom
import requests

# from social.backends.oauth import ConsumerBasedOAuth


def make_user_superuser(strategy, details, user=None, *args, **kwargs):
    print "Callin on the superuser"
    print user.__dict__
    url = 'https://api.github.com/user/memberships/orgs?access_token=%s' % user.social_auth.filter(provider='github')[0].access_token
    r = requests.get(url)
    if(r.ok):
      orgs = r.json()
      org_names = [org['organization']['login'] for org in orgs]
      if 'AltSchool' in org_names:
        if user and not user.is_superuser:
          user.is_superuser = True
          user.is_staff = True
          user.save()


    # if user:
    #     return {'is_new': False}

    # fields = dict((name, kwargs.get(name) or details.get(name))
    #               for name in strategy.setting('USER_FIELDS',
    #                                            USER_FIELDS))
    # if not fields:
    #     return

    # return {
    #     'is_new': True,
    #     'user': strategy.create_user(**fields)
    # }


# class JiraOAuth(ConsumerBasedOAuth):
#     """TripIt OAuth authentication backend"""
#     name = 'tripit'
#     AUTHORIZATION_URL = 'https://altschool.atlassian.net/plugins/servlet/oauth/authorize'
#     REQUEST_TOKEN_URL = 'https://altschool.atlassian.net/plugins/servlet/oauth/request-token'
#     ACCESS_TOKEN_URL = 'https://altschool.atlassian.net/plugins/servlet/oauth/access-token'
#     # EXTRA_DATA = [('screen_name', 'screen_name')]

#     def get_user_details(self, response):
#         """Return user details from TripIt account"""
#         try:
#             first_name, last_name = response['name'].split(' ', 1)
#         except ValueError:
#             first_name = response['name']
#             last_name = ''
#         return {'username': response['screen_name'],
#                 'email': response['email'],
#                 'fullname': response['name'],
#                 'first_name': first_name,
#                 'last_name': last_name}

#     def user_data(self, access_token, *args, **kwargs):
#         """Return user data provided"""
#         url = 'https://api.tripit.com/v1/get/profile'
#         request = self.oauth_request(access_token, url)
#         content = self.fetch_response(request)
#         try:
#             dom = minidom.parseString(content)
#         except ValueError:
#             return None

#         return {
#             'id': dom.getElementsByTagName('Profile')[0].getAttribute('ref'),
#             'name': dom.getElementsByTagName(
#                 'public_display_name')[0].childNodes[0].data,
#             'screen_name': dom.getElementsByTagName(
#                 'screen_name')[0].childNodes[0].data,
#             'email': dom.getElementsByTagName(
#                 'is_primary')[0].parentNode.getElementsByTagName(
#                 'address')[0].childNodes[0].data,
#         }