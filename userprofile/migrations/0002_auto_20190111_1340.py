# Generated by Django 2.1.4 on 2019-01-11 08:10

from django.db import migrations


def create_profile(apps, schema_editor):
    from django.contrib.auth import get_user_model

    User = get_user_model()

    UserProfile = apps.get_model('userprofile', 'UserProfile')
    CategoryModel = apps.get_model('userprofile', 'CategoryMaster')

    users = User.objects.all()

    if users.count() > 0:
        admin_user = users.filter(is_superuser=True).first()

        if not admin_user:
            admin_user = users.first()

        try:
            category = CategoryModel.objects.get(is_default=True)
        except CategoryModel.DoesNotExist:
            category = CategoryModel.objects.create(
                is_default=True, point=3, is_percentage=True,
                name="Default - Auto Created", created_by_id=admin_user.id)

        for user in users:
            try:
                UserProfile.objects.get(created_by_id=user.id)
            except UserProfile.DoesNotExist:
                UserProfile.objects.create(created_by_id=user.id,
                                           category=category)


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_profile),
    ]
