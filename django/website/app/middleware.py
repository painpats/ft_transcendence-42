from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

Member = get_user_model()

class UpdateMembersStatusMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            request.user.last_request = timezone.now()
            request.user.is_online = True
            request.user.save(update_fields=['last_request', 'is_online'])
            self.update_all_status()

        response = self.get_response(request)
        return response

    def update_all_status(self):
        inactivity = timezone.now() - timedelta(minutes=5)

        inactive_members = Member.objects.filter(last_request__lt=inactivity, is_online=True)

        for member in inactive_members:
            member.is_online = False
            member.save(update_fields=['is_online'])
