from django.http import JsonResponse
from django.views import View
from .models import Movie
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import json
# Create your views here.

class Movies(View):
    # @method_decorator(ensure_csrf_cookie)
    def get(self, request):

        if(request.user.is_authenticated):

            user = User.objects.get(id=request.user.id)
            movie_list = list(user.movies.all().values())

            return JsonResponse({
                'Content-Type': 'application/json',
                'status': 200,
                'data': movie_list
            }, safe=False)
        else:
            return JsonResponse({
                'Content-Type': 'application/json',
                'status': 200,
                'message': 'Must be logged in to see this data'
            }, safe=False)
    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        data = request.body.decode('utf-8')
        data = json.loads(data)
        try:
            new_movie = Movie(title=data["title"], description=data["description"])
            new_movie.created_by = request.user
            new_movie.save()
            data["id"] = new_movie.id
            print(data, "this happens on line 38 from :", request.user)
            return JsonResponse({ 
                "data": data
            }, safe=False)
        
        except:
            return JsonResponse({"error": "something has gone terriblly wrong"},safe=False)

class Movie_Detail(View):
    def get(self, request, pk):
        movie_list = list(Movie.objects.filter(pk=pk).values())
        return JsonResponse({'data': movie_list},safe=False)
    def put(self, request, pk):
       
        data = request.body.decode('utf-8')
        data = json.loads(data)

        try:
            edited_movie = Movie.objects.get(pk=pk)
            data_key = list(data.keys())
            for key in data_key:
                if key == "title":
                    edited_movie.title = data[key]
                    print('one')
                if key == "description":
                    edited_movie.description = data[key]
                    print('and done')
            edited_movie.save()
            data["id"] = edited_movie.id
            return JsonResponse({"data": data}, safe=False)
        except:
            return JsonResponse({"error": "Something Went Wrong"}, safe=False)

    def delete(self, request, pk):
        try:
            movie_to_delete = Movie.objects.get(pk=pk)
            movie_to_delete.delete()
            return JsonResponse({"data": "deleted"}, safe=False)
        except:
            return JsonResponse({"error": "Something Went Wrong"}, safe=False)

                                                                                                                                                                