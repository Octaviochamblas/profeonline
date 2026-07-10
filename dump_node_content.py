import os
import sys
import json
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
django.setup()

from apps.content.models import KnowledgeNode

def dump_content(semantic_id, output_path):
    try:
        node = KnowledgeNode.objects.select_related('content').get(semantic_id=semantic_id)
        if not hasattr(node, 'content') or node.content is None:
            print(f"Node {semantic_id} has no content.")
            sys.exit(1)

        c = node.content
        data = {
            'semantic_id': semantic_id,
            'objetivo': c.objetivo,
            'introduccion': c.introduccion,
            'resumen': c.resumen,
            'explicacion': c.explicacion,
            'procedimiento': c.procedimiento,
            'ejemplos': c.ejemplos
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"Content dumped to {output_path}")

    except KnowledgeNode.DoesNotExist:
        print(f"Node {semantic_id} not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error dumping content: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python dump_node_content.py <semantic_id> <output_path>")
        sys.exit(1)

    semantic_id = sys.argv[1]
    output_path = sys.argv[2]
    dump_content(semantic_id, output_path)
