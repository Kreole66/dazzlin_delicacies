from django import forms
from .models import Recipe, Comment, UserProfile


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('category', 'title', 'image', 'cooking_duration', 'difficulty', 'ingredients', 'instructions')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('user', 'contact', 'location', 'hobbies', 'favorite_recipes')