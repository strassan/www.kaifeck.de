from django.contrib.auth.models import Group
from .settings import MAILCOW_USER_GROUP


def make_user_staff(strategy, details, backend, user=None, *args, **kwargs):
    if not user.is_staff:
        user.is_staff = True
        user.save()
    else:
        pass


def add_user_to_group(strategy, details, backend, user=None, *args, **kwargs):
    user_groups_qs = user.groups.filter(name=MAILCOW_USER_GROUP)
    group_qs = Group.objects.filter(name=MAILCOW_USER_GROUP)
    if group_qs:
        group = group_qs.first()
        if not group == user_groups_qs.first():
            group.user_set.add(user)
    else:
        pass
