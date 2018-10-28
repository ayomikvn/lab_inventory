from django.shortcuts import render
from auth_app.forms import RegistrationForm
from auth_app.forms import PasswordChangeCustomForm
from django.http import JsonResponse #JSON response
# This function takes the current request and the updated user object from which the new session hash will be derived and updates the session hash appropriately. (Changes password hash)
from django.contrib.auth import update_session_auth_hash

#Authentication requirements
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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


@login_required  # You need to be logged in to be able to change your password
def change_password(request):
    if request.method == 'POST':
        password_change_form = PasswordChangeCustomForm(request.user, data=request.POST)
        
        if password_change_form.is_valid():
            password_change_form.save()
            update_session_auth_hash(request, password_change_form.user)
            messages.success(
                request, 'Your password was successfully updated!')

        else:
            messages.error(request, 'Password change failed!')

    else:
        password_change_form = PasswordChangeCustomForm(request.user)

    return render(request, 'podrequest/account_settings.html', {'user_form': password_change_form})
