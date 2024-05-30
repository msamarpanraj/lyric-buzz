from django.contrib.auth.models import User
from lyrics.models import Profile

for user in User.objects.all():
    Profile.objects.get_or_create(user=user)
