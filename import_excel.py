import pandas as pd

from restaurant.models import Item, Tag, Section


file = './Items.xlsx'
excel_data = pd.read_excel(file)

for num in range(len(excel_data)):
    try:
        item = Item.objects.get(name=excel_data.Name[num])
    except Item.DoesNotExist:
        item = Item()
        item.name = excel_data.Name[num]
    item.created_by_id = 1
    item.price = int(excel_data.price[num])
    item.category = excel_data.Category[num]
    item.image = 'https://officecafe.in/assets/images/logo_whiteback.png'
    if str(excel_data.Description[num]) == 'nan':
        item.desc = ''
    else:
        item.desc = str(excel_data.Description[num])
    tags = str(excel_data.Tags[num]).split(', ')
    item.save()
    for tg in tags:
        tag, created = Tag.objects.get_or_create(tag=tg)
        item.tags.add(tag)

    section, created = Section.objects.get_or_create(name=str(excel_data.Section[num]))
    item.sections.add(section)
