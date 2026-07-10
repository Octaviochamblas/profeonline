import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
django.setup()

from apps.content.models import KnowledgeNode, NodeAssessmentQuestion
from django.core.management import call_command

def get_nodes_needing_questions(limit=5):
    nodes = KnowledgeNode.objects.filter(node_type=KnowledgeNode.NODE_RECURSO, is_published=True)
    needing = []
    for node in nodes:
        for level in (1, 2, 3):
            count = NodeAssessmentQuestion.objects.filter(node=node, level=level, status='publicada').count()
            if count < 7:
                needing.append(node)
                break # Needs processing
        if len(needing) >= limit:
            break
    return needing

nodes = get_nodes_needing_questions(limit=5)
if not nodes:
    print("No more nodes need processing.")
    sys.exit(0)

for node in nodes:
    print(f"Processing node: {node.semantic_id}")
    call_command("generate_node_assessment_questions", node=node.semantic_id, publish=True)
