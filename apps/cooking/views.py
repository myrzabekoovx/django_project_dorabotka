from django.shortcuts import render, redirect
from .models import Recipe, RecipeRating
from .forms import RecipeForm, RecipeRatingForm
from django.contrib.auth.decorators import login_required



# Страница добавления нового рецепта
@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user  # Привязываем рецепт к пользователю
            recipe.save()
            return redirect('recipe_list')  # Перенаправляем на страницу рецептов
    else:
        form = RecipeForm()
    return render(request, 'cooking/add_recipe.html', {'form': form})

# Страница рецептов
def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'cooking/recipe_list.html', {'recipes': recipes})

# Страница рецепта с возможностью оставить оценку
@login_required
def recipe_detail(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    if request.method == 'POST':
        rating_form = RecipeRatingForm(request.POST)
        if rating_form.is_valid():
            rating = rating_form.save(commit=False)
            rating.recipe = recipe
            rating.user = request.user
            rating.save()
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        rating_form = RecipeRatingForm()
    ratings = recipe.ratings.all()
    avg_rating = ratings.aggregate(models.Avg('rating'))['rating__avg']
    return render(request, 'cooking/recipe_detail.html', {
        'recipe': recipe,
        'rating_form': rating_form,
        'ratings': ratings,
        'avg_rating': avg_rating
    })

