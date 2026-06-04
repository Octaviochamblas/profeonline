from .area_urls import urlpatterns as area_urlpatterns
from .resource_urls import urlpatterns as resource_urlpatterns
from .subject_urls import urlpatterns as subject_urlpatterns
from .topic_urls import urlpatterns as topic_urlpatterns
from .level_urls import urlpatterns as level_urlpatterns
from .module_urls import urlpatterns as module_urlpatterns
from .publish_urls import urlpatterns as publish_urlpatterns

app_name = "content"

urlpatterns = [
    *area_urlpatterns,
    *resource_urlpatterns,
    *subject_urlpatterns,
    *topic_urlpatterns,
    *level_urlpatterns,
    *module_urlpatterns,
    *publish_urlpatterns,
]
