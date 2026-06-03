from django.urls import path
from apps.core.views.analytics_views import AnalyticsEventPostView, AnalyticsDashboardView

urlpatterns = [
    path("eventos/", AnalyticsEventPostView.as_view(), name="analytics_post"),
    path("panel/analitica/", AnalyticsDashboardView.as_view(), name="analytics_dashboard"),
]
