from django.shortcuts import render
from auth_app.forms import RegistrationForm
from django.http import JsonResponse #JSON response

#Authentication requirements
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.
def register(request):
    registered = False

    if request.method == "POST":
        user_form = RegistrationForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            registered = True

        else:
            print(user_form.errors)
    else:
        user_form = RegistrationForm()

    return render(request, 'auth_app/register.html',
                  {'user_form': user_form,
                   'registered': registered})


@login_required  # You need to be logged in to be able to logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('auth_app:user_login'))


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built in authentication
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                # Redirect user once logged in
                responseData = {
                    'results': 'success',
                }
                return JsonResponse(responseData)
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            responseData = {
                'message': 'Username or Password is not correct. Try again.',
                'results': 'failed',
            }
            return JsonResponse(responseData)

    else:
        return render(request, 'auth_app/login.html', {})
