# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models

from huxley.accounts.constants import *
from huxley.core.models import *

import re

class HuxleyUser(AbstractUser):

    TYPE_ADVISOR = 1
    TYPE_CHAIR = 2
    TYPE_CRISIS = 3
    TYPE_FINANCE = 4
    TYPE_SECRETARIAT = 5
    USER_TYPE_CHOICES = ((TYPE_ADVISOR, 'Advisor'),
                         (TYPE_CHAIR, 'Chair'),
                         (TYPE_CRISIS, 'Crisis'),
                         (TYPE_FINANCE, 'Finance'),
                         (TYPE_SECRETARIAT, 'Secretariat'))

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=TYPE_ADVISOR)
    school = models.OneToOneField(School, related_name='advisor', null=True)  # Advisors only.
    committee = models.ForeignKey(Committee, related_name='chair', null=True) # Chairs only.
    

    def is_advisor(self):
        return self.user_type == self.TYPE_ADVISOR

    def is_chair(self):
        return self.user_type == self.TYPE_CHAIR

    def is_crisis(self):
        return self.user_type == self.TYPE_CRISIS

    def is_finance(self):
        return self.user_type == self.TYPE_FINANCE

    def is_secretariat(self):
        return self.user_type == self.TYPE_SECRETARIAT

    def default_path(self):
        if self.is_advisor():
            return reverse('advisors:welcome')
        elif self.is_chair():
            return reverse('chairs:attendance')

    @staticmethod
    def authenticate(username, password):
        '''Attempt to authenticate a user, given a username (or email) and
        password. Return a 2-tuple of (User) user, (str) error.'''
        if not (username and password):
            return None, AuthenticationErrors.MISSING_FIELDS

        user = authenticate(username=username, password=password)
        if user is None:
            try:
                u = HuxleyUser.objects.get(email=username)
                user = authenticate(username=u.username, password=password)
            except HuxleyUser.DoesNotExist:
                pass

        if user is None:
            return None, AuthenticationErrors.INVALID_LOGIN
        if not user.is_active:
            return None, AuthenticationErrors.INACTIVE_ACCOUNT

        return user, None

    @staticmethod
    def login(request, user):
        '''Log in a user and return a redirect url based on whether they're
        an advisor or chair.'''
        login(request, user)
        return user.default_path()

    @classmethod
    def reset_password(cls, username):
        '''Reset and return a user's password, or return False if the user
        doesn't exist.'''
        if not username:
            return False
        try:
            user = cls.objects.get(models.Q(username=username) |
                                   models.Q(email=username))
            new_password = cls.objects.make_random_password(length=10)
            user.set_password(new_password)
            user.save()
            return new_password
        except cls.DoesNotExist:
            return False

    def change_password(self, old, new1, new2):
        '''Attempt to change the given user's password. Return a 2-tuple
        of (bool) success, (str) error.'''
        if not (old and new1 and new2):
            return False, ChangePasswordErrors.MISSING_FIELDS
        if new1 != new2:
            return False, ChangePasswordErrors.MISMATCHED_PASSWORDS
        if len(new1) < 6:
            return False, ChangePasswordErrors.PASSWORD_TOO_SHORT
        if not re.match("^[A-Za-z0-9\_\.!@#\$%\^&\*\(\)~\-=\+`\?]+$", new1):
            return False, ChangePasswordErrors.INVALID_CHARACTERS
        if not self.check_password(old):
            return False, ChangePasswordErrors.INCORRECT_PASSWORD

        self.set_password(new1)
        self.save();
        return True, None

    class Meta:
        db_table = 'huxley_user'
        verbose_name = 'user'
