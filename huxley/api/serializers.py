# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from rest_framework import serializers

from huxley.accounts.models import HuxleyUser
from huxley.core.models import Committee, Country, School

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = HuxleyUser
        fields = ('id', 'first_name', 'last_name', 'user_type', 'school',
                  'committee',)

class CommitteeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Committee
        fields = ('id', 'name', 'full_name', 'delegation_size', 'special',)

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'name', 'special',)

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        # TODO: country/committee preferences
        fields = ('id', 'registered', 'name', 'address', 'city', 'state',
                  'zip_code', 'country', 'primary_name', 'primary_email',
                  'primary_phone', 'secondary_name', 'secondary_email',
                  'secondary_phone', 'program_type', 'times_attended',
                  'min_delegation_size', 'max_delegation_size',
                  'international', 'waitlist')
