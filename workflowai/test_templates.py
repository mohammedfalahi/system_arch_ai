from templates import get_all_templates, get_template_descriptions

templates = get_all_templates()
print('Available Templates:')
print('='*60)
for name in templates.keys():
    print(f'- {name}')
    print(f'  Code length: {len(templates[name])} characters')

print('\nDescriptions:')
print('='*60)
descs = get_template_descriptions()
for name, desc in descs.items():
    print(f'\n{name}:')
    print(f'  {desc}')

print('\n' + '='*60)
print(f'Total templates available: {len(templates)}')
