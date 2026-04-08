with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

with open('backend/disease_info.py', 'w', encoding='utf-8') as f:
    started = False
    for line in lines:
        if line.startswith('disease_info = {'):
            started = True
            f.write(line)
            continue
        if started:
            f.write(line)
            if line.startswith('}'):
                break
