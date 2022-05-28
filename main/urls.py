from pipes import Template
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

urlpatterns = [

    path('', TemplateView.as_view(template_name = 'index.html'), name='index'),
    path('about',TemplateView.as_view(template_name = 'about.html'), name='about'),
     path('aboutsite', TemplateView.as_view(template_name = 'aboutsite.html'), name='aboutsite'),
     path('team', TemplateView.as_view(template_name = 'team.html'), name='team'),

    path('dashboard',views.dashboard, name='dashboard'),
    path('communityprint/<communityID>', views.communityPDFView, name='communityPDFView'),
    path('groupprint/<groupID>', views.groupPDFView, name='groupPDFView'),

    path('additem', views.addCommunityItem, name='additem'),
    path('edititem/<str:communityItemID>',views.editCommunityItem, name='edititem'),
    path('deletecommunityitem/<str:communityItemID>',views.deleteitem, name='deletecommunityitem'),
    path('viewitem/<str:communityItemID>', views.itemDetail, name='itemdetail'),

    path('addgroup', views.addGroup, name='addgroup'),
    path('editgroup/<str:groupID>', views.editGroup, name='editgroup'),
    path('deletegroup/<str:groupID>', views.deleteGroup, name='deletegroup'),
    path('viewgroup/<str:groupID>', views.groupDetail, name='groupdetail'),

    path('viewcommunity/<str:communityNameID>', views.communityDetail, name='communityDetail'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
