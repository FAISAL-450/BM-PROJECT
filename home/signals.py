from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group

@receiver(post_save, sender=User)
def assign_groups(sender, instance, created, **kwargs):
    if created and instance.username == 'admin':
        role_mapping = {
            "eb69dbcb-90a4-4f13-9059-d6494812fd8f": "ConstructionGroup",
            "2b36c9c9-5c74-435b-becd-d01df21e4cf4": "SalesGroup"
        }
        for group_name in role_mapping.values():
            group, _ = Group.objects.get_or_create(name=group_name)
            instance.groups.add(group)


