import django_filters

from django.forms import Select, TextInput

from .models import Order


class OrderFilter(django_filters.FilterSet):
    product_name = django_filters.CharFilter(
        field_name='product__name',
        lookup_expr='icontains',
        label='Product',
        widget=TextInput(attrs={
            'class': 'form-input'
        })
        )
    status = django_filters.ChoiceFilter(
        choices=Order.ORDER_STATUSES,
        widget=Select(attrs={
            'class': 'form-input',
        })
        )
    date_created = django_filters.DateFromToRangeFilter(
        widget=django_filters.widgets.RangeWidget(attrs={
            'placeholder': 'YYYY/MM/DD',
            'type': 'date',
            'class': 'form-input'
            })
            )

    class Meta:
        model = Order
        fields = ['status', 'date_created']
