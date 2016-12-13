# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 14:04:40 2016

@author: martin.provost
"""

from linkedin.linkedin import (LinkedInAuthentication, LinkedInApplication,
                               PERMISSIONS)


if __name__ == '__main__':
    API_KEY = "7724vt213ze2m"
    API_SECRET = "GVd9MjBigin3yQh"
    RETURN_URL = 'http://localhost:8000/'
    authentication = LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL,
                                            PERMISSIONS.enums.values())
    print authentication.authorization_url
    application = LinkedInApplication(authentication)
