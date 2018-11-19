from django.http import JsonResponse
from django.views import View
from django.contrib.auth.models import User
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from movies_api.models import Movie
from django.contrib import auth
import json


@ensure_csrf_cookie
def getToken(request):
  return JsonResponse({'data': 'token successful'}, safe = False)

def logout(request):
  print(request.user, ' this is request.user in logout')
  auth.logout(request)
  print(request.user, request.user.is_authenticated)
  return JsonResponse({"data": "logout successful"},safe = False)

## VIEWS

class CreateUser(View):
  def post(self, request):
    data = request.body.decode('utf-8')
    data = json.loads(data)
    try:
        new_user = User(username = data["username"], password = data["password"], email=data["email"])
        ##hashing the password 
        new_user.set_password(new_user.password)
        new_user.save()
        print(new_user.backend, ' this is happening new user backend')
        auth.login(request, new_user)
        return JsonResponse({"data":  "registration successful"}, safe = False)
    except:
        return JsonResponse({"error": "registration unsuccessful"},safe = False)



class Authentication(View):
    def post(self, request):
        data = request.body.decode('utf-8')
        data = json.loads(data)
        # Will return a user, and do the hashing algorithm be checked if the user
        # is in the database and then return that user
        user = auth.authenticate(username = data["username"], password = data["password"])
        if user is not None:
            auth.login(request, user)
            return JsonResponse({"data": "You are logged in"},safe = False)
        else:
            return JsonResponse({"data": "Login unsuccessful"},safe = False)


class User_Detail(View):
    def get(self, request, pk):
        user = list(User.objects.filter(pk = pk).values())
        movies = list(Movie.objects.filter(created_by_id = pk).values())
        return JsonResponse({"data": {"user": user, "movies": movies}}, safe = False)
