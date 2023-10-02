from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def home(request):
    #Checking to see if logging in
    if request.method == "POST":
        email_adress = request.POST['email_adress']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=email_adress, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,"Logowanie udalo sie!")
            return redirect('home')
        else:
            messages.success(request, "Logowanie nie udalo sie. Sprobuj ponownie..")
            return redirect('home')
    else:
        return render(request, 'home.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, "Zostales wylogowany...")
    return redirect('home')