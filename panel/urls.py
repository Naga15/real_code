from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('export-to-csv/<str:token>/<str:x_axis>/<str:y_axis>', views.export_to_csv, name='export-to-csv'),
    path('export-to-pdf/<str:token>/<str:x_axis>/<str:y_axis>', views.export_to_pdf_new, name='export-to-pdf'),
    path('service/<str:chassisid>/<str:eventid/<str:enginenum>>', views.service, name='service-data'),
]