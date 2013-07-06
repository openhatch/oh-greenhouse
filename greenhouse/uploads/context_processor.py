from django.conf import settings


def user_context(request):
    allowed_groups = settings.ALLOWED_LAUNCHPAD_TEAMS
    if bool(request.user.groups.filter(name__in=allowed_groups)):
        in_group = True
    else:
        in_group = False 

    return {'in_allowed_group': in_group}
