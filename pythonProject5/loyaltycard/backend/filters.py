from django_filters import rest_framework as filters

from backend.models import LoyaltyCard


class LoyaltyCardFilter(filters.FilterSet):
    issue_date = filters.DateFromToRangeFilter()
    expiry_date = filters.DateFromToRangeFilter()

    """Фильтры для карт лояльности."""

    class Meta:
        model = LoyaltyCard
        fields = ['issue_date', 'expiry_date']
