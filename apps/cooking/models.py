from django.db import models
from django.contrib.auth.models import User

# Модель рецепта
class Recipe(models.Model):
    title = models.CharField(max_length=200)
    ingredients = models.TextField()
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Связь с пользователем

    def __str__(self):
        return self.title

# Модель для оценки рецептов
class RecipeRating(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()  # Оценка от 1 до 5

    class Meta:
        unique_together = ('recipe', 'user')

    def __str__(self):
        return f"{self.recipe.title} - {self.rating} by {self.user.username}"

