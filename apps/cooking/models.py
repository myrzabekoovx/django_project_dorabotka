from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название рецепта")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipes")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(verbose_name="Описание")
    cooking_time = models.PositiveIntegerField(verbose_name="Время приготовления (мин)")
    servings = models.PositiveIntegerField(verbose_name="Количество порций")
    image = models.ImageField(upload_to="recipes/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("recipe_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title

class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ingredients")
    name = models.CharField(max_length=100, verbose_name="Название ингредиента")
    quantity = models.CharField(max_length=50, verbose_name="Количество", blank=True)

    def __str__(self):
        return f"{self.name} - {self.quantity}"

class CookingStep(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="steps")
    step_number = models.PositiveIntegerField()
    instruction = models.TextField()

    class Meta:
        ordering = ['step_number']

    def __str__(self):
        return f"Шаг {self.step_number} для {self.recipe.title}"

class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="comments")  # Исправлено
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Комментарий от {self.author.username} к {self.recipe.title}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return f"Профиль {self.user.username}"