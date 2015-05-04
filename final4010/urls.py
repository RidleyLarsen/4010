from django.conf.urls import include, url
from django.contrib import admin

from core.views import HomepageView, QuizCreateView, QuizView

urlpatterns = [
    # Examples:
    # url(r'^$', 'final4010.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', HomepageView.as_view(), name="homepage"),
    url(r'^accounts/', include('accounts.urls', namespace="accounts")),
    url(r'^quiz/(?P<pk>\d+)/$', QuizView.as_view(), name="quiz_detail"),
    url(r'^account/', include(admin.site.urls)),
]
