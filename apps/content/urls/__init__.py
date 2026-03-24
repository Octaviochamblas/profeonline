from .resource_urls import urlpatterns as resource_urlpatterns
from .subject_urls import urlpatterns as subject_urlpatterns
from .topic_urls import urlpatterns as topic_urlpatterns
from .level_urls import urlpatterns as level_urlpatterns
from .module_urls import urlpatterns as module_urlpatterns

app_name = "content"

urlpatterns = [
    *resource_urlpatterns,
    *subject_urlpatterns,
    *topic_urlpatterns,
    *level_urlpatterns,
    *module_urlpatterns,
]