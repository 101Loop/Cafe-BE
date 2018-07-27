from django_filters import FilterSet


class RangeFiltering(FilterSet):
    from django_filters.rest_framework import NumberFilter, ModelMultipleChoiceFilter, CharFilter

    start_price = NumberFilter(field_name='price', lookup_expr='gte')
    end_price = NumberFilter(field_name='price', lookup_expr='lte')
    tag = ModelMultipleChoiceFilter(field_name='tags')
    category = CharFilter(field_name='category')

    class Meta:
        from .models import Item

        model = Item
        fields = ('start_price', 'end_price', 'tag', 'category')
