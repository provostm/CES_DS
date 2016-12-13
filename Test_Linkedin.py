# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 11:38:31 2016

@author: martin.provost
"""

from linkedin import linkedin
#from linkedin import server

API_KEY = "7724vt213ze2mj"
API_SECRET = "GVd9MjBigin3yQhv"
RETURN_URL = "http://localhost:3000/auth/linkedin/callback"
authentication = linkedin.LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL, linkedin.PERMISSIONS.enums.values())
print authentication.authorization_url
application = linkedin.LinkedInApplication(authentication)
#
#authentication.authorization_code = 'AQTXrv3Pe1iWS0EQvLg0NJA8ju_XuiadXACqHennhWih7iRyDSzAm5jaf3R7I8'
#authentication.get_access_token()

#
#application = server.quick_api(API_KEY, API_SECRET)
#
#application.get_profile()

#print profil



#recherche de profil avec mot clé
#application.search_profile(selectors=[{'people': ['first-name', 'last-name']}], params={'keywords': 'apple microsoft'})

# recherche de société avec mot clé
#application.search_company(selectors=[{'companies': ['name', 'universal-name', 'website-url']}], params={'keywords': 'apple microsoft'})
#application.get_companies(company_ids=[1035], universal_names=['apple'], selectors=['name'], params={'is-company-admin': 'true'})


#recherche de job avec mot clé
#application.search_job(selectors=[{'jobs': ['id', 'customer-job-code', 'posting-date']}], params={'title': 'python', 'count': 2})

