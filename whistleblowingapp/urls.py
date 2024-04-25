from django.urls import path

from . import views

app_name = "whistleblowingapp"
urlpatterns = [
    path("", views.index, name="whistleblowingapp"),
    path("signedin/logout", views.logoutview, name="logout"),
    path("signedin/", views.signedin, name="signedin"),
    path("submitreport/", views.report, name="submitreport"),
    path("allreports/", views.allreports, name="allreports"),
    path("submitted/", views.submitreport, name="submitted"),
    path("viewreport/<int:report_id>/", views.viewreport, name="viewreport"),
    path("viewUserReports/", views.viewUserReports, name="viewUserReports"),
    path('delete-report/<int:report_id>/', views.deleteReport, name='deleteReport'),
    path('view/<str:file_type>/<path:file_path>/', views.view_file, name='view_file'),

]