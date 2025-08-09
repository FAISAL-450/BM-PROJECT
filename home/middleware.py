import base64
import json
from django.conf import settings
from django.contrib.auth.models import Group
from django.utils.deprecation import MiddlewareMixin

def get_claims(request):
    """
    Decode the X-MS-CLIENT-PRINCIPAL header from Azure Easy Auth.
    Returns a list of claims.
    """
    encoded = request.headers.get("X-MS-CLIENT-PRINCIPAL")
    if encoded:
        try:
            decoded = base64.b64decode(encoded).decode("utf-8")
            return json.loads(decoded)
        except Exception as e:
            # Optional: log decoding errors
            print(f"Error decoding Azure claims: {e}")
    return []

def extract_group_ids(claims):
    """
    Extract group GUIDs from the decoded claims.
    """
    return [c["val"] for c in claims if c["typ"] == "groups"]

def sync_django_groups(user, group_ids):
    """
    Map Azure group GUIDs to Django groups using AZURE_GROUP_MAP from settings.
    Clears existing groups and assigns new ones.
    """
    user.groups.clear()
    for gid in group_ids:
        group_name = settings.AZURE_GROUP_MAP.get(gid)
        if group_name:
            group, _ = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)

class AzureEasyAuthMiddleware(MiddlewareMixin):
    """
    Middleware to sync Azure AD group claims to Django groups on every request.
    Required because Azure Easy Auth handles login outside Django.
    """
    def process_request(self, request):
        if request.user.is_authenticated:
            claims = get_claims(request)
            group_ids = extract_group_ids(claims)
            sync_django_groups(request.user, group_ids)
