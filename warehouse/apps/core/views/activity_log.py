from rest_framework import generics, viewsets, mixins, permissions
from django_filters import rest_framework as rest_framework_filters
from ..serializers.activity_log import ActivityLogSerializer
from ..models.activity_log import ActivityLog
from django_filters.rest_framework import DjangoFilterBackend

# def datetime_search(queryset, name, value):
#     queryset = queryset.filter(Q(accountables__employee__first_name__icontains=value) | Q(accountables__employee__last_name__icontains=value))
#     return queryset


class ActivityLogFilter(rest_framework_filters.FilterSet):
    datetime_min = rest_framework_filters.DateTimeFilter(
        field_name="logged_at",
        lookup_expr="gte",
        label="Start (Format: YYYY-mm-dd HH:ii:ss)",
    )
    datetime_max = rest_framework_filters.DateTimeFilter(
        field_name="logged_at",
        lookup_expr="lte",
        label="End (Format: YYYY-mm-dd HH:ii:ss)",
    )

    class Meta:
        model = ActivityLog
        fields = ["datetime_min", "datetime_max"]


class ActivityLogViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (rest_framework_filters.DjangoFilterBackend,)
    filterset_class = ActivityLogFilter
    # filterset_fields = ('employee',)
