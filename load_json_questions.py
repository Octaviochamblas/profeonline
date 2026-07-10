import os
import sys
import json
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
django.setup()

from apps.content.models import KnowledgeNode, NodeAssessmentQuestion, NodeAssessmentChoice

def load_questions(semantic_id, json_path):
    print(f"Loading {semantic_id} from {json_path}")
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading {json_path}: {e}")
        return

    try:
        node = KnowledgeNode.objects.get(semantic_id=semantic_id)
    except KnowledgeNode.DoesNotExist:
        print(f"Node {semantic_id} not found.")
        return

    # Delete existing questions if replacing
    # NodeAssessmentQuestion.objects.filter(node=node).delete()

    created_count = 0
    for q_data in data:
        q = NodeAssessmentQuestion.objects.create(
            node=node,
            level=q_data.get('level', 1),
            text=q_data.get('text', ''),
            explanation=q_data.get('explanation', ''),
            status='publicada'
        )
        for choice_data in q_data.get('choices', []):
            NodeAssessmentChoice.objects.create(
                question=q,
                text=choice_data.get('text', ''),
                is_correct=choice_data.get('is_correct', False)
            )
        created_count += 1

    print(f"Loaded {created_count} questions for {semantic_id}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python load_json_questions.py <semantic_id> <json_path>")
        sys.exit(1)

    semantic_id = sys.argv[1]
    json_path = sys.argv[2]
    load_questions(semantic_id, json_path)
