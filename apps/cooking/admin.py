from django.contrib import admin
from .models import Recipe, Category, Ingredient, Comment, UserProfile


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'is_approved')
    list_filter = ('is_approved', 'created_at', 'category')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    actions = ['approve_recipes']

    def approve_recipes(self, request, queryset):
        queryset.update(is_approved=True)
    approve_recipes.short_description = "Одобрить выбранные рецепты"


class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1


RecipeAdmin.inlines = [IngredientInline]


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(UserProfile)
