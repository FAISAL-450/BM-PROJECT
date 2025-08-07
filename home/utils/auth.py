from django.contrib.auth.models import Group
def assign_group_by_email(user):
    email = user.email.lower()
    if email.endswith('@constructioncorp.com'):
        group, _ = Group.objects.get_or_create(name='ConstructionGroup')
        user.groups.add(group)
    elif email.endswith('@salescorp.com'):
        group, _ = Group.objects.get_or_create(name='SalesGroup')
        user.groups.add(group)
