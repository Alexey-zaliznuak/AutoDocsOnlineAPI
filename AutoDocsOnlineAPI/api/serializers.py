from django.conf import settings
from rest_framework import serializers
from rest_framework.utils import model_meta

from core.serializers import Base64FileField
from documents.models import (
    Document,
    Template,
)
from users.serializers import UserSerializer


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = (
            'id',
            'title',
            'author',
            'description',
            'is_official',
            'name_in_document',
        )
        read_only_fields = ('id', 'author', 'is_official',)


class DocumentSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        min_length=settings.DOCUMENT_TITLE_MIN_LENGTH,
        max_length=settings.DOCUMENT_TITLE_MAX_LENGTH
    )
    description = serializers.CharField(
        required=False,
        max_length=settings.DOCUMENT_DESCRIPTION_MAX_LENGTH
    )
    file = Base64FileField(required=True)
    templates = serializers.PrimaryKeyRelatedField(
        queryset=Template.objects.all(), many=True
    )

    class Meta:
        model = Document
        fields = (
            'id',
            'author',
            'title',
            'description',
            'file',
            'templates',
            'creation_date',
        )
        read_only_fields = ('id', 'author', 'creation_date')

    def create(self, validated_data):
        templates = validated_data.pop('templates')

        document = Document.objects.create(**validated_data)
        document.templates.set(templates)

        return document

    def update(self, instance, validated_data):
        info = model_meta.get_field_info(instance)

        m2m_fields = []
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)

        instance.save()

        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            field.set(value)

        return instance


class GetDocumentTemplateSerializer(TemplateSerializer):
    "The same as TemplateSerializer but do not have author field."
    class Meta:
        model = Template
        fields = (
            'id',
            'title',
            'description',
            'is_official',
            'name_in_document',
        )
        read_only_fields = ('id', 'author', 'is_official',)


class GetDocumentSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    templates = GetDocumentTemplateSerializer(many=True)

    class Meta:
        model = Document
        fields = (
            'id',
            'author',
            'title',
            'description',
            'file',
            'templates',
            'creation_date',
        )


# class GetRecipeSerializer(RecipeSerializer):
#     author = UserSerializer()
#     tags = TagSerializer(many=True)
#     ingredients = IngredientAmountSerializer(many=True)
#     is_favorited = serializers.SerializerMethodField()
#     is_in_shopping_cart = serializers.SerializerMethodField()

#     class Meta:
#         model = Recipe
#         fields = (
#             'id',
#             'tags',
#             'author',
#             'ingredients',
#             'name',
#             'image',
#             'text',
#             'cooking_time',
#             'is_favorited',
#             'is_in_shopping_cart',
#         )
#         read_only_fields = ('id', 'author')

#     def get_is_favorited(self, recipe):
#         return Favorite.objects.filter(
#             Q(user=self.context['request'].user.id) & Q(recipe=recipe)
#         ).exists()

#     def get_is_in_shopping_cart(self, recipe):
#         return ShoppingCart.objects.filter(
#             Q(user=self.context['request'].user.id) & Q(recipe=recipe)
#         ).exists()


# class DocumentSerializer(serializers.ModelSerializer):
#     author = serializers.PrimaryKeyRelatedField(
#         read_only=True
#     )
#     file = Base64FileField()

#     class Meta:
#         fields = '__all__'
#         model = Document


# class DocumentsPackageSerializer(serializers.ModelSerializer):
#     owner = serializers.PrimaryKeyRelatedField(
#         pk_field=serializers.CharField(),
#         source='owner.username',
#         read_only=True
#     )

#     class Meta:
#         fields = '__all__'
#         model = DocumentsPackage
#         read_only_fields = ('owner',)
