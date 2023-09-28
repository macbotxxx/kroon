# Create a middleware that will log the actions:
from kroon.users.models import User
from django.contrib.auth.models import Group
from .models import Action_logs

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            # getting the available group - Gov_Worker
            worker_group = Group.objects.get( name = "Gov_Worker" )
            # filtering the worker group from the user account
            gov_worker = User.objects.filter ( email = request.user.email , groups__id = worker_group.id )
            for g in gov_worker:
                # creating the worker action log
                Action_logs.objects.create(
                    action=f'{request.method} {request.path}',
                    user = request.user
                )

        return response


