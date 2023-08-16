from django_filters.rest_framework import FilterSet, filters

from recipes.models import Ingredient, Recipe, Tag


class IngredientsFilter(FilterSet):
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
    )

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        to_field_name="slug",
        queryset=Tag.objects.all(),
    )

    is_favorited = filters.BooleanFilter(
        method='get_favorite',
        label='Favorited',
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_shopping',
        label='Is in shopping list',
    )

    class Meta:
        model = Recipe
        fields = (
            'is_favorited',
            'author',
            'tags',
            'is_in_shopping_cart',
        )

    def get_favorite(self, queryset, name, item_value):
        if self.request.user.is_authenticated and item_value:
            queryset = Recipe.objects.filter(
                in_favorite__user=self.request.user
                )
        return queryset

    def get_shopping(self, queryset, name, item_value):
        if self.request.user.is_authenticated and item_value:
            queryset = Recipe.objects.filter(
                shopping_cart__user=self.request.user
                )
        return queryset
