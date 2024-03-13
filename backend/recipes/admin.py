from django.contrib import admin

from recipes.models import Recipe, RecipeIngredient


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'author',
        'in_favorites'
    )
    list_editable = (
        'name',
        'cooking_time',
        'text',
        'tags',
        'image',
        'author'
    )
    list_filter = (
        'name',
        'author',
        'tags'
    )
    readonly_fields = ('in_favorites',)
    empty_value_display = '-пусто-'

    @admin.display(description='В избранном')
    def in_favorites(self, obj):
        return obj.favorite_recipe.count()


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'recipe',
        'ingredient',
        'amount'
    )
    list_editable = (
        'recipe',
        'ingredient',
        'amount'
    )
