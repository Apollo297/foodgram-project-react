from django.contrib import admin

from recipes.models import (
    Recipe,
    RecipeIngredient
)


class RecipeIngredientsInLine(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


class RecipeTagsInLine(admin.TabularInline):
    model = Recipe.tags.through
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'cooking_time',
        'text',
        'author',
        'image',
        'in_favorites'
    )
    list_editable = (
        'name',
        'cooking_time',
        'text',
        'image',
        'author'
    )
    list_filter = (
        'name',
        'author',
        'tags'
    )
    inlines = (RecipeIngredientsInLine, RecipeTagsInLine)
    search_fields = (
        'name',
        'author'
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
