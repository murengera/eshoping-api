from django.contrib.auth.models import Group
from rest_framework import serializers
from store.models import Stock,StockRating
from UserCustom.serializer import UserSerializer




class StoreSerializer(serializers.ModelSerializer):

    # workers = UserSerializer(read_only=True, many=True)
    # icon = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = Stock
        exclude = ('is_deleted', )

    def to_representation(self, obj):
        serialized_data = super(StoreSerializer, self).to_representation(obj)

        # serialized_data.pop('workers')

        user = None
        request = self.context.get("request")

        if request and hasattr(request, "user"):
            user = request.user
            user_group = user.groups.first()
            store_manager = Group.objects.get(name="Manager")

            if user_group == store_manager:
                user_store = Stock.objects.filter(workers=user).first()
                if not user_store:
                    serialized_data.pop('workers')
                    return serialized_data

                if user_store.id == obj.id:
                    s_workers = obj.workers.all()
                    store_workers = []

                    for s_worker in s_workers:
                        worker = UserSerializer(s_worker, context=self.context).data
                        store_workers.append(worker)

                    serialized_data['workers'] = store_workers

                else:
                    serialized_data.pop('workers')

            else:
                serialized_data.pop('workers')

        return serialized_data



class StoreMiniSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stock
        exclude = ('is_deleted', )

    def to_representation(self, instance):
        serialized_data = super(StoreMiniSerializer, self).to_representation(instance)

        serialized_data.pop('workers')
        serialized_data.pop('activated_by')

        return serialized_data
class StoreReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockRating
        fields = '__all__'

    def to_representation(self, instance):
        serialized_data = super(StoreReviewSerializer, self).to_representation(instance)

        if instance.reviewer:
            serialized_data['reviewer'] = UserSerializer(instance.reviewer, context=self.context).data

        return serialized_data
