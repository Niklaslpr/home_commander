from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import RegisterForm, UpdateUserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

@user_passes_test(lambda u: u.is_superuser)
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)

        if form.is_valid():
            form.save()
            return redirect("/options")
    else:
        form = RegisterForm()

    return render(response, "authentication/register.html", {"form":form})

@login_required()
def change_password(response):
    if response.method == 'POST':
        form = PasswordChangeForm(response.user, response.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(response, user)
            messages.success(response, 'Das Passwort wurde erfolgreich geändert.')
            return redirect('change_password')
    else:
        form = PasswordChangeForm(response.user)
    return render(response, 'authentication/change_password.html', {'form':form})


@login_required
def edit_profile(response):
    if response.method == 'POST':
        form = UpdateUserForm(response.POST, instance=response.user)

        if form.is_valid():
            form.save()
            messages.success(response, 'Die Änderungen wurden erfolgreich gespeichert')
            return redirect('edit_profile')

    else:
        form = UpdateUserForm(instance=response.user)

    return render(response, 'authentication/edit_profile.html', {'form':form})
