# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

class ChangePasswordErrors:
    MISSING_FIELDS = 'One or more fields is blank.'
    MISMATCHED_PASSWORDS = 'New passwords must match.'
    PASSWORD_TOO_SHORT = 'New password must be at least 6 characters long.'
    INVALID_CHARACTERS = 'New password can only consist of alphanumeric characters and symbols (above numbers).'
    INCORRECT_PASSWORD = 'Incorrect password.'

class AuthenticationErrors:
    MISSING_FIELDS = "Whoops! One or more of the fields is blank."
    INVALID_LOGIN = "Sorry! The login you provided was invalid."
    INACTIVE_ACCOUNT = "We're sorry, but your account is inactive."
