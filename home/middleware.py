import json, base64
from django.contrib.auth.models import User, Group

class AzureEasyAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        header = request.META.get('HTTP_X_MS_CLIENT_PRINCIPAL')
        if header:
            try:
                decoded = base64.b64decode(header)
                user_info = json.loads(decoded)
                email = user_info.get('userDetails')
                roles = user_info.get('userRoles', [])

                if email:
                    username = email.split('@')[0]
                    user, _ = User.objects.get_or_create(username=username, defaults={'email': email})
                    request.user = user

                    role_map = {
                        "Construction Dept": "ConstructionGroup",
                        "Sales Dept": "SalesGroup"
                    }

                    user.groups.clear()
                    for role in roles:
                        group_name = role_map.get(role)
                        if group_name:
                            group, _ = Group.objects.get_or_create(name=group_name)
                            user.groups.add(group)
            except Exception as e:
                pass  # Optional: log the error

        return self.get_response(request)



