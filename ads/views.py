from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from ads.models import Carousel_ad
from ads.serializers import CarouselAdSerializer
from store.models import Stock


"""
Carousel_ad views
"""
class CarouselAdsList(generics.GenericAPIView,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin):
    """
    View to list all the carousel ads, and add new ones
    """
    serializer_class = CarouselAdSerializer

    filter_fields = '__all__'

    def get_queryset(self):
        user = self.request.user
        store_manager = Group.objects.get(name='Manager')
        store_worker = Group.objects.get(name='Worker')
        user_group = user.groups.first()

        queryset = Carousel_ad.objects.none()

        if user.is_staff:
            queryset = Carousel_ad.objects.filter(is_deleted=False)

        elif user_group == store_manager or user_group == store_worker:
            store = Stock.objects.filter(workers=user).first()

            if store is not None:
                queryset = Carousel_ad.objects.filter(is_deleted=False, is_active=True) | Carousel_ad.objects.filter(is_deleted=False, store=store)

        else:
            queryset = Carousel_ad.objects.filter(is_deleted=False, is_active=True)

        return queryset


    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = request.user
        store_manager = Group.objects.get(name='Manager')
        user_group = user.groups.first()

        request_data = request.data

        if user.is_staff:

            return self.create(request, *args, **kwargs)

        if user_group == store_manager:
            store = Stock.objects.filter(workers=user).first()

            if store is not None:
                request_data['store'] = str(store.id)
                request_data['created_by'] = str(user.id)

                return self.create(request, *args, **kwargs)

        return JsonResponse({"detail": "You are not allowed to perform such operation"}, status=403, safe=False)


class CarouselAdDetails(generics.GenericAPIView,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin):
    """
    View to deal with a particular carousel_ad
    """
    serializer_class = CarouselAdSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        user = self.request.user
        store_manager = Group.objects.get(name='Manager')
        store_worker = Group.objects.get(name='Worker')
        user_group = user.groups.first()

        queryset = Carousel_ad.objects.none()

        if user.is_staff:
            queryset = Carousel_ad.objects.filter(is_deleted=False)

        elif user_group == store_manager or user_group == store_worker:
            store = Stock.objects.filter(workers=user).first()

            if store is not None:
                queryset = Carousel_ad.objects.filter(is_deleted=False, is_active=True) | Carousel_ad.objects.filter(is_deleted=False, store=store)

        else:
            queryset = Carousel_ad.objects.filter(is_deleted=False, is_active=True)

        return queryset

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        carousel_ad = self.get_object()

        user = request.user
        store_manager = Group.objects.get(name='Manager')
        user_group = user.groups.first()

        if user.is_staff:
            carousel_ad.is_deleted = True
            carousel_ad.save()

            return JsonResponse(None, status=204, safe=False)

        if user_group == store_manager:
            store = Stock.objects.filter(workers=user).first()

            if store is not None:
                if store == carousel_ad.store:
                    carousel_ad.is_deleted = True
                    carousel_ad.save()

                    return JsonResponse(None, status=204, safe=False)

        return JsonResponse({"detail": "You are not allowed to perform such operation"}, status=403, safe=False)


"""
Banner_ad views
"""
