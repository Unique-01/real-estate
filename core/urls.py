from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('property-list', views.PropertyList.as_view(), name='property_list'),
    path('<slug:slug>/<int:id>/',
         views.PropertyDetail.as_view(), name='property_detail'),
    path('search/', views.search, name='search'),
    path('profile/<username>', views.profile, name='profile'),
    path('accounts/update-profile', views.profile_update, name='profile_update'),
    path('upload-property', views.property_upload, name='property_upload'),
    path('send-mail/', views.contact_email, name='contact_email'),
    path('delete-property/<slug>/<id>',
         views.PropertyDelete.as_view(), name='property_delete'),
]
