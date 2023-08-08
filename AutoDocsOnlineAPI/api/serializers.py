from django.conf import settings
from rest_framework import serializers

from core.serializers import Base64FileField, ModelWithUpdateForM2MFields
from documents.models import (
    Document,
    Template,
    TemplateValue,
    UserDefaultTemplateValue,
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


class CreateUpdateDocumentSerializer(ModelWithUpdateForM2MFields):
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


class CreateUpdateTemplateValueSerializer(serializers.ModelSerializer):
    template = serializers.PrimaryKeyRelatedField(
        queryset=Template.objects.all()
    )
    value = serializers.CharField(
        max_length=settings.TEMPLATE_VALUE_VALUE_MAX_LENGTH
    )

    class Meta:
        model = UserDefaultTemplateValue
        fields = (
            'template',
            'value',
        )
        read_only_fields = ('id',)


class GetUserDefaultTemplateValueSerializer(serializers.ModelSerializer):
    value = serializers.CharField(source='template_value.value')
    template = TemplateSerializer(source='template_value.template')

    class Meta:
        model = UserDefaultTemplateValue
        fields = (
            'id',
            'template',
            'value',
        )
        read_only_fields = ('id',)


class CreateUpdateUserDefaultTemplateValueSerializer(
    serializers.ModelSerializer
):
    template_value = CreateUpdateTemplateValueSerializer()

    class Meta:
        model = UserDefaultTemplateValue
        fields = (
            'template_value',
        )

    def create(self, validated_data):
        template_value = validated_data.pop('template_value')
        template_value, _ = TemplateValue.objects.get_or_create(
            **template_value
        )

        obj = UserDefaultTemplateValue.objects.create(
            **validated_data,
            template_value=template_value
        )

        return obj

    def update(self, instance, validated_data):
        # You can`t change template

        template_value = validated_data.pop('template_value', None)

        if template_value:
            template_value, _ = TemplateValue.objects.get_or_create(
                template=instance.template_value.template,
                value=template_value['value']
            )
            instance.template_value = template_value

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance


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
