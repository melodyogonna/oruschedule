from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

from .models import Project, Section, Tasks

# project_content = ContentType.objects.get_for_model(Project)
# section_content = ContentType.objects.get_for_model(Section)
# task_content = ContentType.objects.get_for_model(Tasks)


# @receiver(post_migrate)
# def create_groups(sender, **kwargs):
#     try:
#         Group.objects.get(name='admins')
#     except Group.DoesNotExist:
#         admins = Group(name='admins')
#         admins.save()
#         full_permission = Permission.objects.get(codename='full_permission')
#         admins.add(full_permission)



class InvitationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp)
        )

account_activation_token = InvitationTokenGenerator()