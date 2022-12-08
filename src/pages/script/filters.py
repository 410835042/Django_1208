from pages.models import Search
import django_filters


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Search
        fields = '__all__'