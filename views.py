from datetime import timezone
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Recipe, Comment, UserProfile
from .forms import RecipeForm, CommentForm, UserProfileForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('all_recipes')  # Redirect to all_recipes after login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user_login')  # Redirect to all_recipes after registration
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def all_recipes(request):
    query = request.GET.get('q')
    recipes = Recipe.objects.all()

    if query:
        recipes = recipes.filter(title__icontains=query)

    return render(request, 'all_recipes.html', {'recipes': recipes})


def create_recipe(request):
    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST, request.FILES)
        if recipe_form.is_valid():
            recipe = recipe_form.save(commit=False)
            recipe.save()
            return redirect('all_recipes')
    else:
        recipe_form = RecipeForm()
    return render(request, 'create_recipe.html', {'recipe_form': recipe_form})


def recipe_detail(request, recipe_id):
    recipe = Recipe.objects.get(pk=recipe_id)
    comments = recipe.comments.all()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.recipe = recipe
            comment.save()
            return redirect('recipe_detail', recipe_id=recipe_id)
    else:
        comment_form = CommentForm()
    return render(request, 'recipe_detail.html', {'recipe': recipe, 'comments': comments, 'comment_form': comment_form})


def edit_recipe(request, recipe_id):
    recipe = Recipe.objects.get(pk=recipe_id)

    if request.method == 'POST':
        # Check if 'delete' parameter is present in the form
        if 'delete' in request.POST:
            # Delete the recipe
            recipe.delete()
            # Redirect to a relevant page after deletion (e.g., home or recipe list)
            return HttpResponseRedirect('all_recipes')

        recipe_form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if recipe_form.is_valid():
            recipe = recipe_form.save(commit=False)
            recipe.time_edited = timezone.now()
            recipe.save()
            return redirect('profile')
    else:
        recipe_form = RecipeForm(instance=recipe)

    return render(request, 'edit_recipe.html', {'recipe_form': recipe_form, 'recipe_id': recipe_id})


def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user  # Assuming you're using authentication
            profile.save()
            return redirect('profile_detail')  # Replace 'profile_detail' with your profile detail URL name
    else:
        form = UserProfileForm(
            instance=request.user.userprofile)  # Assuming a OneToOneField relationship between User and UserProfile

    return render(request, 'edit_profile.html', {'form': form})


def profile_detail(request):
    try:
        profile = UserProfile.objects.get(user=request.user)  # Get the UserProfile instance for the logged-in user
        return render(request, 'profile_detail.html', {'profile': profile})
    except UserProfile.DoesNotExist:
        return redirect('edit_profile')

