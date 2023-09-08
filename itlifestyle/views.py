from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Profile


# Create Home View
def home(request):
    return render(request, 'home.html', {})


# Create All profiles view
def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {'profiles': profiles})

    else:
        messages.success(request, 'You Must Be Logged In To View This Page!')
        return redirect('home')


# Create User's Profile View
def profile(request, pk):
    if request.user.is_authenticated:
        user_profile = Profile.objects.get(user_id=pk)

        # Post Form logic
        if request.method == 'POST':
            # Get current user
            current_user_profile = request.user.profile

            # Get form data
            action = request.POST['follow']

            # Follow or Unfollow
            if action == 'unfollow':
                current_user_profile.follows.remove(user_profile)

            elif action == 'follow':
                current_user_profile.follows.add(user_profile)

            # Save the profile
            current_user_profile.save()

        return render(request, 'profile.html', {'user_profile': user_profile})

    else:
        messages.success(request, 'You Must Be Logged In To View This Page!')
        return redirect('home')
