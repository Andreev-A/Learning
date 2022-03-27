import json

from django import forms
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.utils.decorators import method_decorator

from .models import Item, Review


class GoodForm(forms.Form):
    title = forms.RegexField(min_length=1, max_length=64, regex='\D')
    description = forms.RegexField(min_length=1, max_length=1024, regex='\D')
    price = forms.IntegerField(min_value=1, max_value=1000000)


class ReviewForm(forms.Form):
    text = forms.RegexField(min_length=1, max_length=1024, regex='\D')
    grade = forms.IntegerField(min_value=1, max_value=10)


@method_decorator(csrf_exempt, name='dispatch')
class AddItemView(View):
    """View для создания товара."""

    def post(self, request):
        try:
            form_data = json.loads(request.body)
            form = GoodForm(form_data)
            if form.is_valid():
                context = form.cleaned_data
                item = Item(title=context['title'],
                            description=context['description'],
                            price=context['price'])
                item.save()
                data = {'id': item.pk}
                return JsonResponse(data, status=201)
            else:
                return HttpResponse(status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class PostReviewView(View):
    """View для создания отзыва о товаре."""

    def post(self, request, item_id):
        try:
            form_data = json.loads(request.body)
            form = ReviewForm(form_data)

            if form.is_valid():
                context = form.cleaned_data
                try:
                    item = Item.objects.get(pk=item_id)
                    review = Review(text=context['text'],
                                    grade=context['grade'],
                                    item=item)
                    review.save()
                    return JsonResponse({'id': review.id}, status=201)
                except Item.DoesNotExist:
                    return HttpResponse(status=404)
            else:
                return HttpResponse(status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)


class GetItemView(View):
    """View для получения информации о товаре."""

    def get(self, request, item_id):
        try:
            item = Item.objects.prefetch_related('review_set').get(id=item_id)
        except Item.DoesNotExist:
            return JsonResponse(status=404, data={})
        item_dict = model_to_dict(item)
        item_reviews = [model_to_dict(x) for x in item.review_set.all()]
        item_reviews = sorted(
            item_reviews, key=lambda review: review['id'], reverse=True)[:5]
        for review in item_reviews:
            review.pop('item', None)
        item_dict['reviews'] = item_reviews
        return JsonResponse(item_dict, status=200)

#####################################################################################################################
# Решение задания по обработке данных от преподавателей
#####################################################################################################################
# import json
#
# from django.http import HttpResponse, JsonResponse
# from django.views import View
#
# from marshmallow import Schema, ValidationError, fields, post_load
# from marshmallow.validate import Length, Range
#
# from .models import Item, Review
#
#
# class ItemSchema(Schema):
#     id = fields.Int(dump_only=True)
#     title = fields.Str(required=True, validate=Length(1, 64))
#     description = fields.Str(required=True, validate=Length(1, 1024))
#     price = fields.Int(required=True, validate=Range(1, 1000000), strict=True)
#
#     @post_load
#     def make(self, data):
#         return Item(**data)
#
#
# class ReviewSchema(Schema):
#     id = fields.Int(dump_only=True)
#     grade = fields.Int(required=True, validate=Range(1, 10), strict=True)
#     text = fields.Str(required=True, validate=Length(1, 1024))
#
#     @post_load
#     def make(self, data):
#         return Review(**data)
#
#
# class AddItemView(View):
#     """View для создания товара."""
#
#     def post(self, request):
#         try:
#             document = json.loads(request.body)
#             schema = ItemSchema(strict=True)
#             item = schema.load(document).data
#             item.save()
#         except (json.JSONDecodeError, ValidationError, AssertionError):
#             return HttpResponse(status=400)
#         data = {'id': item.pk}
#         return JsonResponse(data, status=201)
#
#
# class PostReviewView(View):
#     """View для создания отзыва о товаре."""
#
#     def post(self, request, item_id):
#         try:
#             item = Item.objects.get(pk=item_id)
#             document = json.loads(request.body)
#             schema = ReviewSchema(strict=True)
#             review = schema.load(document).data
#             review.item = item
#             review.save()
#         except Item.DoesNotExist:
#             return HttpResponse(status=404)
#         except (json.JSONDecodeError, ValidationError):
#             return HttpResponse(status=400)
#         data = {'id': review.pk}
#         return JsonResponse(data, status=201)
#
#
# class GetItemView(View):
#     """View для получения информации о товаре.
#
#     Помимо основной информации выдает последние отзывы о товаре, не более 5
#     штук.
#     """
#
#     def get(self, request, item_id):
#         try:
#             item = Item.objects.get(pk=item_id)
#         except Item.DoesNotExist:
#             return HttpResponse(status=404)
#         schema = ItemSchema()
#         data = schema.dump(item).data
#         query = Review.objects.filter(item=item).order_by('-id')
#         reviews = query[:5]
#         schema = ReviewSchema(many=True)
#         data['reviews'] = schema.dump(reviews).data
#         return JsonResponse(data, status=200)

######################################################################################################################
# views(marshmallow)
######################################################################################################################
# import json
#
# from django.http import HttpResponse, JsonResponse
# from django.views import View
#
# from marshmallow import Schema, ValidationError, fields, post_load
# from marshmallow.validate import Length, Range
#
# from .models import Item, Review
#
#
# class ItemSchema(Schema):
#     id = fields.Int(dump_only=True)
#     title = fields.Str(required=True, validate=Length(1, 64))
#     description = fields.Str(required=True, validate=Length(1, 1024))
#     price = fields.Int(required=True, validate=Range(1, 1000000), strict=True)
#
#     @post_load
#     def make(self, data):
#         return Item(**data)
#
#
# class ReviewSchema(Schema):
#     id = fields.Int(dump_only=True)
#     grade = fields.Int(required=True, validate=Range(1, 10), strict=True)
#     text = fields.Str(required=True, validate=Length(1, 1024))
#
#     @post_load
#     def make(self, data):
#         return Review(**data)
#
#
# class AddItemView(View):
#     """View для создания товара."""
#
#     def post(self, request):
#
#         try:
#             document = json.loads(request.body)
#             schema = ItemSchema(strict=True)
#             item = schema.load(document).data
#             item.save()
#         except (json.JSONDecodeError, ValidationError):
#             return HttpResponse(status=400)
#
#         return JsonResponse({'id': item.pk}, status=201)
#
#
# class PostReviewView(View):
#     """View для создания отзыва о товаре."""
#
#     def post(self, request, item_id):
#
#         try:
#             item = Item.objects.get(pk=item_id)
#             document = json.loads(request.body)
#             schema = ReviewSchema(strict=True)
#             review = schema.load(document).data
#             review.item = item
#             review.save()
#         except Item.DoesNotExist:
#             return HttpResponse(status=404)
#         except (json.JSONDecodeError, ValidationError):
#             return HttpResponse(status=400)
#
#         return JsonResponse({'id': review.pk}, status=201)
#
#
# class GetItemView(View):
#     """View для получения информации о товаре.
#
#     Помимо основной информации выдает последние отзывы о товаре, не более 5
#     штук.
#     """
#
#     def get(self, request, item_id):
#
#         try:
#             item = Item.objects.get(pk=item_id)
#         except Item.DoesNotExist:
#             return HttpResponse(status=404)
#
#         schema = ItemSchema()
#         data = schema.dump(item).data
#         query = Review.objects.filter(item=item).order_by('-id')
#         reviews = query[:5]
#         schema = ReviewSchema(many=True)
#         data['reviews'] = schema.dump(reviews).data
#         return JsonResponse(data, status=200)

#######################################################################################################################
# views(django_forms)
#######################################################################################################################
# import json
#
# from django.http import HttpResponse, JsonResponse
# from django.views import View
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
# from django import forms
#
# from .models import Item, Review
#
#
# class AddItemForm(forms.Form):
#     title = forms.CharField(max_length=64, required=True, widget=forms.TextInput)
#     description = forms.CharField(max_length=1024, required=True)
#     price = forms.IntegerField(min_value=1, max_value=1000000, required=True)
#
#     def clean(self):
#         cleaned_data = super().clean()
#
#         if not isinstance(self.data.get('title'), str):
#             raise forms.ValidationError('The "title" field must be of type str.')
#
#         if not isinstance(self.data.get('description'), str):
#             raise forms.ValidationError('The "description" field must be of type str.')
#
#         return cleaned_data
#
#
# class AddReviewForm(forms.Form):
#     text = forms.CharField(max_length=1024, required=True)
#     grade = forms.IntegerField(min_value=1, max_value=10, required=True)
#
#     def clean(self):
#         cleaned_data = super().clean()
#
#         if not isinstance(self.data.get('text'), str):
#             raise forms.ValidationError('The "text" field must be of type str.')
#
#         return cleaned_data
#
#
# @method_decorator(csrf_exempt, name='dispatch')
# class AddItemView(View):
#
#     def post(self, request):
#
#         try:
#             form = AddItemForm(json.loads(request.body))
#         except json.JSONDecodeError:
#             return HttpResponse(status=400)
#
#         if not form.is_valid():
#             return HttpResponse(status=400)
#
#         new_item = Item(title=form.cleaned_data['title'],
#                         description=form.cleaned_data['description'],
#                         price=form.cleaned_data['price'])
#         new_item.save()
#         return JsonResponse({'id': new_item.id}, status=201, safe=False)
#
#
# @method_decorator(csrf_exempt, name='dispatch')
# class PostReviewView(View):
#
#     def post(self, request, item_id):
#
#         try:
#             form = AddReviewForm(json.loads(request.body))
#         except json.JSONDecodeError:
#             return HttpResponse(status=400)
#
#         if not form.is_valid():
#             return HttpResponse(status=400)
#
#         if not Item.objects.filter(pk=item_id).exists():
#             return HttpResponse(status=404)
#
#         review = Review(
#             text=form.cleaned_data['text'],
#             grade=form.cleaned_data['grade'],
#             item_id=item_id
#         )
#         review.save()
#         return JsonResponse({'id': review.id}, status=201)
#
#
# @method_decorator(csrf_exempt, name='dispatch')
# class GetItemView(View):
#
#     def get(self, request, item_id):
#
#         if not Item.objects.filter(pk=item_id).exists():
#             return HttpResponse(status=404)
#
#         item_data = Item.objects.filter(pk=item_id).first()
#         item_reviews = Review.objects.filter(item=item_id).order_by('-id')[:5]
#         reviews = []
#
#         for review in item_reviews:
#             reviews.append({'id': review.id, 'text': review.text, 'grade': review.grade})
#
#         result = {
#             'id': item_id,
#             'title': item_data.title,
#             'description': item_data.description,
#             'price': item_data.price,
#             'reviews': reviews
#         }
#         return JsonResponse(result, status=200)

#####################################################################################################################
# views(jsonschema)
#####################################################################################################################
# import json
# from jsonschema import validate
# from jsonschema.exceptions import ValidationError
# from django import forms
# from django.http import HttpResponse, JsonResponse
# from django.views import View
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
# from django.forms.models import model_to_dict
#
# from .models import Item, Review
#
# GOODS_SCHEMA = {
#     '$schema': 'http://json-schema.org/schema#',
#     'type': 'object',
#     'properties': {
#         'title': {
#             'type': 'string',
#             'minLength': 1,
#             'maxLength': 64,
#         },
#         'description': {
#             'type': 'string',
#             'minLength': 1,
#             'maxLength': 1024,
#         },
#         'price': {
#             'type': 'integer',
#             'minimum': 1,
#             'maximum': 1000000,
#         },
#     },
#     'required': ['title', 'description', 'price'],
# }
#
# REVIEW_SCHEMA = {
#     '$schema': 'http://json-schema.org/schema#',
#     'type': 'object',
#     'properties': {
#         'text': {
#             'type': 'string',
#             'minLength': 1,
#             'maxLength': 1024,
#         },
#         'grade': {
#             'type': 'integer',
#             'minimum': 1,
#             'maximum': 10,
#         },
#     },
#     'required': ['text', 'grade'],
# }
#
#
# @method_decorator(csrf_exempt, name='dispatch')
# class AddItemView(View):
#     """View для создания товара."""
#
#     def post(self, request):
#
#         try:
#             document = json.loads(request.body)
#             validate(document, GOODS_SCHEMA)
#         except (json.JSONDecodeError, ValidationError):
#             return HttpResponse(status=400)
#
#         item = Item(title=document['title'],
#                     description=document['description'],
#                     price=document['price'])
#         item.save()
#         return JsonResponse({'id': item.pk}, status=201)
#
#
# @method_decorator(csrf_exempt, name='dispatch')
# class PostReviewView(View):
#     """View для создания отзыва о товаре."""
#
#     def post(self, request, item_id):
#
#         try:
#             document = json.loads(request.body)
#             validate(document, REVIEW_SCHEMA)
#             item = Item.objects.get(id=item_id)
#             review = Review(text=document['text'],
#                             grade=document['grade'],
#                             item_id=item.pk)
#             review.save()
#         except Item.DoesNotExist:
#             return HttpResponse(status=404)
#         except (json.JSONDecodeError, ValidationError):
#             return HttpResponse(status=400)
#
#         return JsonResponse({'id': review.id}, status=201)
#
#
# class GetItemView(View):
#     """View для получения информации о товаре.
#
#     Помимо основной информации выдает последние отзывы о товаре, не более 5
#     штук.
#     """
#
#     def get(self, request, item_id):
#
#         try:
#             item = Item.objects.prefetch_related('review_set').get(id=item_id)
#         except Item.DoesNotExist:
#             return HttpResponse(status=404)
#
#         items = model_to_dict(item)
#         reviews = []
#
#         for i in item.review_set.all():
#             reviews.append(model_to_dict(i))
#
#         reviews = sorted(reviews, key=lambda review: review['id'], reverse=True)[:5]
#         items['reviews'] = reviews
#         return JsonResponse(items, status=200)
