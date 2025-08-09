import base64, json
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.conf import settings

AZURE_GROUP_MAP = {
    "eb69dbcb-90a4-4f13-9059-d6494812fd8f": "ConstructionGroup",
    "2b36c9c9-5c74-435b-becd-d01df21e4cf4": "SalesGroup"
}

def get_claims(request):
    encoded = request.headers.get("X-MS-CLIENT-PRINCIPAL")
    if encoded:
        decoded = base64.b64decode(encoded).decode("utf-8")
        return json.loads(decoded)
    return []

def extract_group_ids(claims):
    return [c["val"] for c in claims if c["typ"] == "groups"]

def sync_django_groups(user, group_ids):
    user.groups.clear()
    for gid in group_ids:
        group_name = AZURE_GROUP_MAP.get(gid)
        if group_name:
            group, _ = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)

@receiver(user_logged_in)
def assign_groups_on_login(sender, request, user, **kwargs):
    claims = get_claims(request)
    group_ids = extract_group_ids(claims)
    sync_django_groups(user, group_ids)

