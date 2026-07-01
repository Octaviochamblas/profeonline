import os, sys, importlib.util

for p in range(1, 14):
    file_path = f'C:/Users/PC/Documents/Proyectos/Web/profeonline/scratch/b0309_pair_{p}.py'
    if os.path.exists(file_path):
        spec = importlib.util.spec_from_file_location(f'mod_{p}', file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for k, v in module.topics.items():
            print(f'{k}: keys = {list(v.keys())}, type(v)={type(v)}')
            if 'yaml' in v:
                print(f"  type(v['yaml']) = {type(v['yaml'])}")
