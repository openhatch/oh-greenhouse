from django.contrib.auth.decorators import user_passes_test
from django.conf import settings


def group_perm_required():
    """
    An extension of the user_passes_test decorator that simplifies
    permissions handling for viewing a page.
    """
    def in_groups(u):
        allowed_groups = settings.ALLOWED_LAUNCHPAD_TEAMS
        if u.is_authenticated():
            if bool(u.groups.filter(name__in=allowed_groups)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups, login_url='/denied')
