from django_filters import FilterSet


class MenuFiltering(FilterSet):
    """
    A filter class to implement filters on items of the menu.
    """
    from django_filters.rest_framework import NumberFilter, ModelMultipleChoiceFilter
    from .models import Tag, Item, Section

    start_price = NumberFilter(field_name='price', lookup_expr='gte')
    end_price = NumberFilter(field_name='price', lookup_expr='lte')
    tag = ModelMultipleChoiceFilter(field_name='tags', queryset=Tag.objects.all())
    section = ModelMultipleChoiceFilter(field_name='sections', queryset=Section.objects.all())
    category = ModelMultipleChoiceFilter(field_name='category', queryset=Item.objects.all())
    price = NumberFilter(field_name='price')

    class Meta:
        from .models import Item

        model = Item
        fields = ('start_price', 'end_price', 'tag', 'category', 'price', 'section')


class TagFiltering(FilterSet):
    from django_filters.rest_framework import ModelMultipleChoiceFilter
    from .models import Tag

    tag = ModelMultipleChoiceFilter(field_name='tag', queryset=Tag.objects.all())

    class Meta:
        from .models import Tag

        model = Tag
        fields = ('tag', )


class SectionFiltering(FilterSet):
    from django_filters.rest_framework import ModelMultipleChoiceFilter
    from .models import Section

    name = ModelMultipleChoiceFilter(field_name='name', queryset=Section.objects.all())

    class Meta:
        from .models import Section

        model = Section
        fields = ('name', )
