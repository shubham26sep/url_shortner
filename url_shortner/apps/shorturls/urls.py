from django.urls import path, re_path

from url_shortner.apps.shorturls import views

urlpatterns = [
    path('fetch/short-url/', views.FetchShortUrlView.as_view(), name='short-url'),
    path('fetch/short-urls/', views.FetchMultipleShortUrlsView.as_view(), name='short-urls'),
    path('fetch/long-url/', views.FetchLongUrlView.as_view(), name='long-url'),
    path('fetch/long-urls/', views.FetchMultipleLongUrlsView.as_view(), name='long-urls'),
    path('fetch/count/', views.FetchShortUrlAccessCount.as_view(), name='short-url-access-count'),
    path('clean-urls/', views.CleanUrlView.as_view(), name='clean-urls'),
    re_path('(?P<hashcode>[\w._-]+)/', views.ShortUrlServerView.as_view(), name='short-url-server'),
]
