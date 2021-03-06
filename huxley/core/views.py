# Copyright (c) 2011-2014 Berkeley Model United Nations. All rights reserved.
# Use of this source code is governed by a BSD License (see LICENSE).

from django.shortcuts import render_to_response
from django.template import RequestContext

from huxley.core.models import *

def index(request):
    '''Render the appropriate base tempate.'''
    context = RequestContext(request)
    if not request.user.is_authenticated():
        return render_to_response('login.html', context)
    else:
        return render_to_response('base-inner.html', context)
