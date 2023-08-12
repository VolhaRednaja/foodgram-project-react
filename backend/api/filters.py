from django_filters.rest_fraemwork import FilterSet, filters

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
        gueryset=Tag.objects.all(),
    )
    is_favorited = filters.BooleanFilter(method="get_is_favorited")
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ["author", "tags", "is_favorited", "is_in_shopping_cart"]

    """
    def get_tags(self, queryset, name, value):
        tags = self.request.tags
        if value:
            for tag in tags:
                queryset = queryset.filter(tags__slug=tag)
        return queryset
    """

    def get_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value:
            return queryset.filter(is_favorited__user=user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value:
            return queryset.filter(is_in_shopping_cart__user=user)
        return queryset
