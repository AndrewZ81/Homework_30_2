from rest_framework.fields import SerializerMethodField
from rest_framework.relations import SlugRelatedField, PrimaryKeyRelatedField, StringRelatedField
from rest_framework.serializers import ModelSerializer

from advertisements.models import Category, Advertisement, Selection
from users.models import User, Location


class CategoryViewSetSerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class AdvertisementListViewSerializer(ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field="username"
    )
    category = StringRelatedField()
    locations = SerializerMethodField()

    class Meta:
        model = Advertisement
        fields = ["id", "name", "author", "price", "category", "locations"]

    def get_locations(self, ad):
        setattr(ad, "locations", [location.name for location in ad.author.location.all()])
        return ad.locations


class AdvertisementDetailViewSerializer(ModelSerializer):
    author_id = PrimaryKeyRelatedField(queryset=User.objects.all())
    author = SlugRelatedField(
        read_only=True,
        slug_field="username",
    )
    category_id = PrimaryKeyRelatedField(queryset=Category.objects.all())
    category = StringRelatedField()
    locations = SerializerMethodField()

    class Meta:
        model = Advertisement
        fields = "__all__"

    def get_locations(self, ad):
        setattr(ad, "locations", [location.name for location in ad.author.location.all()])
        return ad.locations


class AdvertisementUpdateViewSerializer(ModelSerializer):
    author_id = PrimaryKeyRelatedField(queryset=User.objects.all())
    author = SlugRelatedField(
        read_only=True,
        slug_field="username",
    )
    category_id = PrimaryKeyRelatedField(queryset=Category.objects.all())
    category = StringRelatedField()
    locations = SerializerMethodField()

    def get_locations(self, ad):
        return [location.name for location in ad.author.location.all()]

    def is_valid(self, *, raise_exception=False):
        advertisement_locations = self.initial_data.pop("location", [])
        setattr(self, "_location", advertisement_locations)
        return super().is_valid(raise_exception=raise_exception)

    def save(self, **kwargs):
        advertisement = super().save(**kwargs)
        if self._location:
            advertisement.author.location.clear()
            for loc in self._location:
                new_location, _ = Location.objects.get_or_create(name=loc)
                advertisement.author.location.add(new_location)
        advertisement.save()
        return advertisement

    class Meta:
        model = Advertisement
        fields = "__all__"


class SelectionDetailViewSerializer(ModelSerializer):
    """
    Сериализует подборку объявлений по id подборки
    """
    items = AdvertisementDetailViewSerializer(many=True)

    class Meta:
        model = Selection
        fields = "__all__"


class SelectionListViewSerializer(ModelSerializer):
    """
    Сериализует все подборки объявлений
    """

    class Meta:
        model = Selection
        fields = ["id", "name"]


class SelectionCreateViewSerializer(ModelSerializer):
    """
    Сериализует создание подборки объявлений
    """

    class Meta:
        model = Selection
        fields = "__all__"


class SelectionUpdateViewSerializer(ModelSerializer):
    """
    Сериализует изменение подборки объявлений
    """

    class Meta:
        model = Selection
        fields = "__all__"
