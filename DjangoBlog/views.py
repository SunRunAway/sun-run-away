from django.http import HttpResponse


def displayMeta(request):
    html = []
    for k, v in request.META.items():
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))
