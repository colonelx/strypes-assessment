from django_filters import rest_framework as rest_framework_filters
from rest_framework import permissions, viewsets
from .models import StorageSpace, STORAGE_SPACE_PRIOS
from .serializers.storage_space import StorageSpaceSerializer
from django.db.models import Q

def full_name_search(queryset, name, value):
    queryset = queryset.filter(Q(accountables__employee__first_name__icontains=value) | Q(accountables__employee__last_name__icontains=value))
    return queryset

class StorageSpaceEmployeeFilter(rest_framework_filters.FilterSet):
    name = rest_framework_filters.CharFilter(label="Employee name (first or last)", method=full_name_search)
    priority = rest_framework_filters.ChoiceFilter(field_name='priority', choices=STORAGE_SPACE_PRIOS)

class StorageSpaceViewSet(viewsets.ModelViewSet):
    '''
    TODO: That way I can separate the two serializers, define different fields and achieve 
    the difference between List and Detail. However for the sake of this task, I have already
    provided in the single type serializers how I can fetch and filter the different 
    task requirements, so I don't deem necessary to implement that.


    serializer_class = StorageSpaceListSerializer
    detail_serializer_class = StorageSpaceDetailSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            if hasattr(self, 'detail_serializer_class'):
                return self.detail_serializer_class

        return super(StorageSpaceViewSet, self).get_serializer_class()
    '''
    queryset = StorageSpace.objects
    serializer_class = StorageSpaceSerializer
    permission_classes = [permissions.IsAuthenticated]

    # ASSUME: Since, we don't have empoloyee list endpoint, I see no point in filtering
    # on employee_id, therefore I am introducing a filter to search by first_name and last_name.
    filterset_class = StorageSpaceEmployeeFilter

    