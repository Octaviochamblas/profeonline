from .resource_urls import urlpatterns as resource_urlpatterns
from .subject_urls import urlpatterns as subject_urlpatterns
from .topic_urls import urlpatterns as topic_urlpatterns

app_name = "content"

urlpatterns = [
    *resource_urlpatterns,
    *subject_urlpatterns,
    *topic_urlpatterns,
]