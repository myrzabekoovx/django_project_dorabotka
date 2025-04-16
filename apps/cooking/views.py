from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Recipe, Ingredient, CookingStep, Comment
from .forms import RecipeForm, CommentForm


@login_required
def create_recipe(request):

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            try:

                recipe = form.save(commit=False)
                recipe.author = request.user
                recipe.save()


                ingredients_text = form.cleaned_data.get('ingredients', '')
                self._process_ingredients(recipe, ingredients_text)

                steps_text = form.cleaned_data.get('cooking_steps', '')
                self._process_cooking_steps(recipe, steps_text)

                messages.success(request, 'Рецепт успешно создан!')
                return redirect('recipe_detail', slug=recipe.slug)

            except Exception as e:
                messages.error(request, f'Ошибка при создании рецепта: {str(e)}')

    else:
        form = RecipeForm()

    return render(request, 'recipes/create_recipe.html', {
        'form': form,
        'title': 'Создание нового рецепта'
    })


def _process_ingredients(self, recipe, ingredients_text):
    """Обработка и сохранение ингредиентов"""
    for line in ingredients_text.split('\n'):
        line = line.strip()
        if line:
            parts = line.split('-', 1)
            name = parts[0].strip()
            quantity = parts[1].strip() if len(parts) > 1 else ''
            Ingredient.objects.create(
                recipe=recipe,
                name=name,
                quantity=quantity
            )


def _process_cooking_steps(self, recipe, steps_text):
    """Обработка и сохранение шагов приготовления"""
    for i, step in enumerate(steps_text.split('\n'), 1):
        step = step.strip()
        if step:
            CookingStep.objects.create(
                recipe=recipe,
                step_number=i,
                instruction=step
            )


def recipe_detail(request, slug):
    """
    Просмотр деталей рецепта с комментариями
    """
    recipe = get_object_or_404(
        Recipe.objects.select_related('author', 'category')
        .prefetch_related('ingredients', 'steps', 'comments__author'),
        slug=slug
    )

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request, 'Для комментирования необходимо авторизоваться')
            return redirect('login')

        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            try:
                new_comment = comment_form.save(commit=False)
                new_comment.recipe = recipe
                new_comment.author = request.user
                new_comment.save()
                messages.success(request, 'Комментарий успешно добавлен!')
                return redirect('recipe_detail', slug=slug)
            except Exception as e:
                messages.error(request, f'Ошибка при добавлении комментария: {str(e)}')
    else:
        comment_form = CommentForm()

    return render(request, 'recipes/recipe_detail.html', {
        'recipe': recipe,
        'comments': recipe.comments.all(),
        'comment_form': comment_form,
        'title': recipe.title
    })