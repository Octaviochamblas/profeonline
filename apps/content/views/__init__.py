from .area_list import AreaListView
from .area_detail import AreaDetailView
from .area_create import AreaCreateView
from .area_update import AreaUpdateView
from .area_delete import AreaDeleteView
from .resource_list import ResourceListView
from .resource_detail import ResourceDetailView
from .resource_create import ResourceCreateView
from .resource_update import ResourceUpdateView
from .resource_delete import ResourceDeleteView
from .subject_list import SubjectListView
from .subject_detail import SubjectDetailView
from .subject_create import SubjectCreateView
from .subject_update import SubjectUpdateView
from .subject_delete import SubjectDeleteView
from .topic_list import TopicListView
from .topic_detail import TopicDetailView
from .topic_create import TopicCreateView
from .topic_update import TopicUpdateView
from .topic_delete import TopicDeleteView
from .topic_options import topic_options_by_subject
from .level_list import LevelListView
from .level_detail import LevelDetailView
from .level_create import LevelCreateView
from .level_update import LevelUpdateView
from .level_delete import LevelDeleteView
from .module_list import ModuleListView
from .module_create import ModuleCreateView
from .module_update import ModuleUpdateView
from .module_delete import ModuleDeleteView
from .resource_options import resource_options
from .module_resource_add import module_resource_add
from .module_resource_remove import module_resource_remove
from .module_resource_list import module_resource_list
from .api_video import create_resource_from_video
from .resource_completion import toggle_resource_completion
from .evaluation_views import (
    quiz_start,
    quiz_submit,
    quiz_status,
    quiz_recover,
    report_error,
    topic_exam_start,
    topic_exam_submit,
)
