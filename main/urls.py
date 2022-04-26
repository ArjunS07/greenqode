from pipes import Template
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

from django.views.generic import TemplateView



urlpatterns = [

    path('', TemplateView.as_view(template_name = 'index.html'), name='index'),
    path('about',
         TemplateView.as_view(template_name = 'about.html'), name='about'),
     path('aboutsite', TemplateView.as_view(template_name = 'aboutsite.html'), name='aboutsite'),
     path('team', TemplateView.as_view(template_name = 'team.html'), name='team'),

    path('communitycollection',
         views.communityCollection, name='communitycollection'),
    path('pdf/<pk>', views.render_pdf_view, name='render_pdf_view'),
    path('additem', views.addCommunityItem, name='additem'),
    path('edititem/<str:communityItemID>',
         views.editCommunityItem, name='edititem'),
    path('deletecommunityitem/<str:communityItemID>',

         views.deleteitem, name='deletecommunityitem'),
    path('viewcommunity/<str:communityNameID>',
         views.viewCommunityAsGuest, name='viewcommunityasguest'),
    path('viewitem/<str:communityNameID>/<str:communityItemID>',
         views.viewCommunityItemAsGuest, name='viewitemasguest'),


]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
