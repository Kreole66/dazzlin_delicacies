from django.db import models
from django.contrib.auth.models import User


DIFFICULTY_CHOICES = [
    ('easy', 'Easy'),
    ('medium', 'Medium'),
    ('moderate', 'Moderate'),
    ('difficult', 'Difficult'),
    ('very_difficult', 'Very Difficult'),
]

CATEGORY_CHOICES = [
    ('breakfast', 'Breakfast'),
    ('lunch', 'Lunch'),
    ('dinner', 'Dinner'),
    ('dessert', 'Dessert'),
]


class Recipe(models.Model):
    category = models.CharField(max_length=15, choices=CATEGORY_CHOICES, default='breakfast')
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='recipe_images/')
    cooking_duration = models.IntegerField(help_text="Duration in minutes", default=15)
    difficulty = models.CharField(max_length=15, choices=DIFFICULTY_CHOICES)
    ingredients = models.TextField()
    instructions = models.TextField()
    time_created = models.DateTimeField(auto_now_add=True)
    time_edited = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=10, blank=True)
    location = models.CharField(max_length=10, blank=True)
    hobbies = models.TextField(blank=True)
    favorite_recipes = models.ManyToManyField('Recipe', blank=True)