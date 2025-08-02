from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import Group
from django.conf import settings

@receiver(user_logged_in)
def assign_group(sender, request, user, **kwargs):
    azure_group_ids = request.session.get("azure_groups", [])
    roles_mapping = settings.AZURE_AUTH.get("ROLES", {})

    for azure_id in azure_group_ids:
        group_name = roles_mapping.get(azure_id)
        if group_name:
            group, _ = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)
