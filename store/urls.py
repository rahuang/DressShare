from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt
from django.conf.urls import patterns, include, url

from store import views

urlpatterns = patterns('',
    url(
            r'^own-dress/$',
            views.OwnDress.as_view(),
            name='own-dress',
        ),
    url(
            r'^add-dress/$',
            views.AddDress.as_view(),
            name='add-dress',
        ),
    url(
            r'^process-dress/$',
            views.ProcessDress.as_view(),
            name='process-dress',
        ),
    url(
            r'^processfittingroom/$',
            views.ProcessFit.as_view(),
            name='process-fitting-room',
        ),
    url(
            r'^fittingroom/$',
            views.FittingRoomView.as_view(),
            name='fitting-room',
        ),
    url(
            r'^processrequest/$',
            views.ProcessRequest.as_view(),
            name='process-request',
        ),
    url(
            r'^requests/$',
            views.Requests.as_view(),
            name='requests',
        ),
    
)