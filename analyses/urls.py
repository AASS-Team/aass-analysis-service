from django.urls import path

from . import views

urlpatterns = [
    path("", views.AnalysesList.as_view()),
    path("<uuid:id>", views.AnalysisDetail.as_view()),
]
