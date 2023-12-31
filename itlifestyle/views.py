from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Profile, UserPost
from .forms import PostForm


# Create Home View
def home(request):
    if request.user.is_authenticated:
        form = PostForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.save()
                messages.success(request, 'Your Post Has Been Posted!')
                return redirect('home')

        posts = UserPost.objects.all().order_by('-created_at')
        return render(request, 'home.html', {'posts': posts, 'form': form})

    else:
        messages.success(request, 'You Must Be Logged In To View This Page!')
        return redirect('home')


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
        posts = UserPost.objects.filter(user_id=pk).order_by('-created_at')

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

        return render(request, 'profile.html', {'user_profile': user_profile, 'posts': posts})

    else:
        messages.success(request, 'You Must Be Logged In To View This Page!')
        return redirect('home')
