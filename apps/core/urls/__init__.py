from .home_urls import urlpatterns as home_patterns
from .analytics_urls import urlpatterns as analytics_patterns

app_name = "core"

urlpatterns = home_patterns + analytics_patterns
