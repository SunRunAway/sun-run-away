from django.shortcuts import render_to_response
from django.template import RequestContext


def aboutme(request):
    return render_to_response('aboutme.html', context_instance=RequestContext(request))
