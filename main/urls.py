from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    path('', views.home, name='home'),
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
    path('about',
         views.aboutPage, name='about'),
    path('sentry-test/', trigger_error)

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
