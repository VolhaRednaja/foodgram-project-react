import django_filters as filters

from recipes.models import Ingredient, Recipe


class IngredientsFilter(filters.FilterSet):
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
    )

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        to_field_name="slug",
        method="get_tags",
    )
    is_favorited = filters.CharFilter(method="get_is_favorited")
    is_in_shopping_cart = filters.CharFilter(
        method='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ["author", "tags", "is_favorited", "is_in_shopping_cart"]

    def get_tags(self, queryset, name, value):
        tags = self.request.tags
        if value:
            for tag in tags:
                queryset = queryset.filter(tags__slug=tag)
        return queryset

    def get_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value:
            return queryset.filter(in_carts__user=user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value:
            return queryset.filter(in_carts__user=user)
        return queryset
