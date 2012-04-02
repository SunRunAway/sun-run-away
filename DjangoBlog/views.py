from django.http import HttpResponse
from django.contrib.sites.models import Site

current_site = Site.objects.get_current()
current_site.domain


def displayMeta(request):
    # html = ['<tr><td>current_site.domain</td><td>%s</td></tr>' % (current_site.domain)]
    # for k, v in request.META.items():
    #     html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    # return HttpResponse('<table>%s</table>' % '\n'.join(html))
    return None
