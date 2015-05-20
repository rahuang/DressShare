from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt
from django.conf.urls import patterns, include, url

from store import views

urlpatterns = patterns('',
    url(
            r'^test1/$',
            views.TestPage.as_view(),
            name='test1',
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
)