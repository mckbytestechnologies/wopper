# mck_website/api.py

import sys
import json
from datetime import datetime, date
from decimal import Decimal
from django.urls import reverse, NoReverseMatch
from django.forms.models import model_to_dict
from django.utils import timezone
from phonenumber_field.phonenumber import PhoneNumber
from django.db import models

from config import app_utils, app_logger
from mck_auth import api as auth_api
from mck_website.models import *
from mck_admin_console.models import *
from mck_auth.models import *

log_name = "app"
logger = app_logger.createLogger(log_name)


# ══════════════════════════════════════════════════════════════════════════════
# CATEGORY API FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

@app_logger.functionlogs(log=log_name)
def category_load_data(request, table_data):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    fResult = list()
    try:
        queryset = Category.objects.exclude(datamode='D').order_by('-updated_on')
        qs, total_records, total_display_records = app_utils.method_for_datatable_operations(
            request, queryset)

        final_data = list()
        for qs_instance in qs:
            qs_data = model_to_dict(qs_instance)
            data = list()
            edit_url = reverse('mck_website:mck_category_update', args=[qs_data['id']])

            for column in table_data['columns']:
                if column['column_name'] == "datamode":
                    if qs_instance.datamode == "A":
                        data.append('<span class="badge bg-success">Active</span>')
                        data.append(f'<div class="text-end"><a href="{edit_url}" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void(0)" class="text-danger ps-2" onclick="delete_object({qs_data["id"]})">Inactivate</a></div>')
                    else:
                        data.append('<span class="badge bg-danger">Inactive</span>')
                        data.append(f'<div class="text-end"><a href="{edit_url}" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void(0)" class="text-success ps-2" onclick="delete_object({qs_data["id"]})">Activate</a></div>')
                else:
                    if isinstance(qs_data.get(column['column_name']), PhoneNumber):
                        data.append(qs_data.get(column['column_name']).national_number)
                    elif isinstance(qs_data.get(column['column_name']), models.ImageField):
                        pass
                    else:
                        value = qs_data.get(column['column_name'], "-")
                        data.append(value)
            final_data.append(data)
        fResult = app_utils.final_dict(request, total_records, total_display_records, final_data)
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, fResult


@app_logger.functionlogs(log=log_name)
def category_retrieve_data(request, id):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        category = Category.objects.filter(id=id).first()
        if category:
            data['category'] = category
            result, msg = True, success_msg
        else:
            result, msg, data = True, success_msg, data
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def category_create_update(request, id=None, mode=None):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        accountuser = auth_api.get_request_accountuser(request)
        pDict = request.POST
        if mode == 'edit' and id:
            obj = Category.objects.filter(id=id).first()
            if not obj:
                error_msg = "Category not found"
                return False, error_msg, data
        else:
            obj = Category()
            obj.created_by = accountuser.id
            
        obj.name = pDict.get('name')
        obj.slug = pDict.get('slug')
        obj.description = pDict.get('description')
        obj.sort_order = pDict.get('sort_order', 0)
        obj.is_featured = True if pDict.get('is_featured') else False
        obj.show_on_homepage = True if pDict.get('show_on_homepage') else False

        if request.FILES.get('image'):
            obj.image = request.FILES.get('image')

        obj.updated_by = accountuser.id
        obj.save()

        data['category'] = obj
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def category_update_status(request, id):
    result = False
    message = 'Error'
    try:
        accountuser = auth_api.get_request_accountuser(request)
        obj = Category.objects.filter(id=id).first()
        if obj:
            obj.updated_by = accountuser.id
            obj.datamode = "A" if obj.datamode == "I" else "I"
            obj.save()
            result = True
            message = 'Success'
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, message


# ══════════════════════════════════════════════════════════════════════════════
# PRODUCT API FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

@app_logger.functionlogs(log=log_name)
def product_load_data(request, table_data):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    fResult = list()
    try:
        queryset = Product.objects.exclude(datamode='D').order_by('-updated_on')
        qs, total_records, total_display_records = app_utils.method_for_datatable_operations(
            request, queryset)

        final_data = list()
        for qs_instance in qs:
            qs_data = model_to_dict(qs_instance)
            data = list()
            edit_url = reverse('mck_website:mck_product_update', args=[qs_data['id']])

            for column in table_data['columns']:
                if column['column_name'] == "datamode":
                    if qs_instance.datamode == "A":
                        data.append('<span class="badge bg-success">Active</span>')
                        data.append(f'<div class="text-end"><a href="{edit_url}" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void(0)" class="text-danger ps-2" onclick="delete_object({qs_data["id"]})">Inactivate</a></div>')
                    else:
                        data.append('<span class="badge bg-danger">Inactive</span>')
                        data.append(f'<div class="text-end"><a href="{edit_url}" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void(0)" class="text-success ps-2" onclick="delete_object({qs_data["id"]})">Activate</a></div>')
                else:
                    if isinstance(qs_data.get(column['column_name']), PhoneNumber):
                        data.append(qs_data.get(column['column_name']).national_number)
                    else:
                        value = qs_data.get(column['column_name'], "-")
                        if isinstance(value, Decimal):
                            value = float(value)
                        data.append(value)
            final_data.append(data)
        fResult = app_utils.final_dict(request, total_records, total_display_records, final_data)
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, fResult


@app_logger.functionlogs(log=log_name)
def product_retrieve_data(request, id):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        product = Product.objects.filter(id=id).first()
        if product:
            data['product'] = product
            result, msg = True, success_msg
        else:
            result, msg, data = True, success_msg, data
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def product_create_update(request, id=None, mode=None):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        accountuser = auth_api.get_request_accountuser(request)
        pDict = request.POST
        
        category_id = pDict.get("category")
        if not category_id:
            error_msg = "Category is required"
            return False, error_msg, data
            
        if mode == 'edit' and id:
            obj = Product.objects.filter(id=id).first()
            if not obj:
                error_msg = "Product not found"
                return False, error_msg, data
        else:
            obj = Product()
            obj.created_by = accountuser.id
            
        try:
            category = Category.objects.get(id=category_id)
            obj.category = category
        except Category.DoesNotExist:
            error_msg = "Invalid category selected"
            return False, error_msg, data
            
        obj.name = pDict.get("name")
        obj.slug = pDict.get("slug")
        obj.sku = pDict.get("sku")
        obj.short_description = pDict.get("short_description")
        obj.description = pDict.get("description")

        price = pDict.get("price") or 0
        sale_price = pDict.get("sale_price") or None
        
        obj.price = float(price) if price else 0
        obj.sale_price = float(sale_price) if sale_price and sale_price != '0' else None
        obj.stock = int(pDict.get("stock") or 0)

        obj.is_featured = bool(pDict.get("is_featured"))
        obj.is_best_seller = bool(pDict.get("is_best_seller"))
        obj.is_flash_sale = bool(pDict.get("is_flash_sale"))
        obj.is_new_arrival = bool(pDict.get("is_new_arrival"))
        obj.is_trending = bool(pDict.get("is_trending"))
        obj.is_top_rated = bool(pDict.get("is_top_rated"))
        obj.is_active = bool(pDict.get("is_active"))

        if request.FILES.get("image"):
            obj.image = request.FILES.get("image")

        image_fields = ['image1', 'image2', 'image3', 'image4', 'image5']
        for field_name in image_fields:
            if request.FILES.get(field_name):
                setattr(obj, field_name, request.FILES.get(field_name))

        obj.updated_by = accountuser.id
        obj.save()
        
        data["product"] = {
            "id": obj.id,
            "name": obj.name,
            "slug": obj.slug,
            "sku": obj.sku,
            "price": str(obj.price),
            "sale_price": str(obj.sale_price) if obj.sale_price else None,
            "stock": obj.stock,
            "category_id": obj.category.id,
            "category_name": obj.category.name,
            "is_active": obj.is_active,
        }
        result, msg = True, success_msg
        
    except ValueError as e:
        result, msg = False, f"Invalid data format: {str(e)}"
        logger.error(f'ValueError at product_create_update: {e}')
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def product_update_status(request, id):
    result = False
    message = 'Error'
    try:
        accountuser = auth_api.get_request_accountuser(request)
        obj = Product.objects.filter(id=id).first()
        if obj:
            obj.updated_by = accountuser.id
            obj.datamode = "A" if obj.datamode == "I" else "I"
            obj.save()
            result = True
            message = 'Success'
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, message


# ══════════════════════════════════════════════════════════════════════════════
# BLOG API FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

@app_logger.functionlogs(log=log_name)
def blog_load_data(request, table_data):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    fResult = list()
    try:
        queryset = Blog.objects.exclude(datamode='D').order_by('-updated_on')
        qs, total_records, total_display_records = app_utils.method_for_datatable_operations(
            request, queryset)

        final_data = list()
        for qs_instance in qs:
            qs_data = model_to_dict(qs_instance)
            data = list()
            edit_url = reverse('mck_website:mck_blog_update', args=[qs_data['id']])

            for column in table_data['columns']:
                if column['column_name'] == "datamode":
                    if qs_instance.datamode == "A":
                        data.append('<span class="badge bg-success">Active</span>')
                        data.append(f'<div class="text-end"><a href="{edit_url}" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void(0)" class="text-danger ps-2" onclick="delete_object({qs_data["id"]})">Inactivate</a></div>')
                    else:
                        data.append('<span class="badge bg-danger">Inactive</span>')
                        data.append(f'<div class="text-end"><a href="{edit_url}" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void(0)" class="text-success ps-2" onclick="delete_object({qs_data["id"]})">Activate</a></div>')
                elif column['column_name'] == "is_published":
                    if qs_instance.is_published:
                        data.append('<span class="badge bg-success">Published</span>')
                    else:
                        data.append('<span class="badge bg-warning">Draft</span>')
                elif column['column_name'] == "image":
                    if qs_instance.image:
                        data.append(f'<img src="{qs_instance.image.url}" width="50" height="50" style="object-fit:cover;" />')
                    else:
                        data.append('-')
                else:
                    value = qs_data.get(column['column_name'], "-")
                    if isinstance(value, (datetime, date)):
                        data.append(value.strftime('%Y-%m-%d %H:%M'))
                    else:
                        data.append(value)
            final_data.append(data)
        fResult = app_utils.final_dict(request, total_records, total_display_records, final_data)
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, fResult


@app_logger.functionlogs(log=log_name)
def blog_retrieve_data(request, id):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        blog = Blog.objects.filter(id=id).first()
        if blog:
            data['blog'] = blog
            result, msg = True, success_msg
        else:
            result, msg, data = True, success_msg, data
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def blog_create_update(request, id=None, mode=None):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        accountuser = auth_api.get_request_accountuser(request)
        pDict = request.POST
        
        if mode == 'edit' and id:
            obj = Blog.objects.filter(id=id).first()
            if not obj:
                error_msg = "Blog not found"
                return False, error_msg, data
        else:
            obj = Blog()
            obj.created_by = accountuser.id
        
        obj.title = pDict.get("title")
        obj.slug = pDict.get("slug")
        obj.description = pDict.get("description")
        
        is_published = pDict.get("is_published")
        obj.is_published = bool(is_published)
        
        if is_published and not obj.published_date:
            obj.published_date = timezone.now()
        elif not is_published:
            obj.published_date = None
        
        if request.FILES.get("image"):
            obj.image = request.FILES.get("image")

        obj.updated_by = accountuser.id
        obj.save()
        
        data["blog"] = {
            "id": obj.id,
            "title": obj.title,
            "slug": obj.slug,
            "is_published": obj.is_published,
        }
        result, msg = True, success_msg
        
    except ValueError as e:
        result, msg = False, f"Invalid data format: {str(e)}"
        logger.error(f'ValueError at blog_create_update: {e}')
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def blog_update_status(request, id):
    result = False
    message = 'Error'
    try:
        accountuser = auth_api.get_request_accountuser(request)
        obj = Blog.objects.filter(id=id).first()
        if obj:
            obj.updated_by = accountuser.id
            obj.datamode = "A" if obj.datamode == "I" else "I"
            obj.save()
            result = True
            message = 'Success'
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, message


# ══════════════════════════════════════════════════════════════════════════════
# HOMEPAGE VIDEO API FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

@app_logger.functionlogs(log=log_name)
def homepage_video_load_data(request, table_data):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    fResult = list()
    try:
        queryset = HomePageVideo.objects.exclude(datamode='D').order_by('sort_order')
        qs, total_records, total_display_records = app_utils.method_for_datatable_operations(
            request, queryset)

        final_data = list()
        for qs_instance in qs:
            qs_data = model_to_dict(qs_instance)
            data = list()
            edit_url = reverse('mck_website:mck_homepage_video_update', args=[qs_data['id']])

            for column in table_data['columns']:
                if column['column_name'] == "datamode":
                    if qs_instance.datamode == "A":
                        data.append('<span class="badge bg-success">Active</span>')
                        data.append(f'<div class="text-end"><a href="{edit_url}" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void(0)" class="text-danger ps-2" onclick="delete_object({qs_data["id"]})">Inactivate</a></div>')
                    else:
                        data.append('<span class="badge bg-danger">Inactive</span>')
                        data.append(f'<div class="text-end"><a href="{edit_url}" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void(0)" class="text-success ps-2" onclick="delete_object({qs_data["id"]})">Activate</a></div>')
                else:
                    value = qs_data.get(column['column_name'], "-")
                    if isinstance(value, Decimal):
                        value = float(value)
                    data.append(value)
            final_data.append(data)
        fResult = app_utils.final_dict(request, total_records, total_display_records, final_data)
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, fResult


@app_logger.functionlogs(log=log_name)
def homepage_video_retrieve_data(request, id):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        obj = HomePageVideo.objects.filter(id=id).first()
        if obj:
            data['homepage_video'] = obj
            result, msg = True, success_msg
        else:
            result, msg, data = True, success_msg, data
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def homepage_video_create_update(request, id=None, mode=None):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        accountuser = auth_api.get_request_accountuser(request)
        pDict = request.POST

        if mode == 'edit' and id:
            obj = HomePageVideo.objects.filter(id=id).first()
            if not obj:
                error_msg = "HomePageVideo not found"
                return False, error_msg, data
        else:
            obj = HomePageVideo()
            obj.created_by = accountuser.id

        obj.title = pDict.get('title')
        obj.cat_button = pDict.get('cat_button')
        obj.sort_order = pDict.get('sort_order') or 1

        if request.FILES.get('thumbnail_image'):
            obj.thumbnail_image = request.FILES.get('thumbnail_image')

        if request.FILES.get('video'):
            obj.video = request.FILES.get('video')

        obj.updated_by = accountuser.id
        obj.save()
        data['homepage_video'] = obj
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def homepage_video_update_status(request, id):
    result = False
    message = 'Error'
    try:
        accountuser = auth_api.get_request_accountuser(request)
        obj = HomePageVideo.objects.filter(id=id).first()
        if obj:
            obj.updated_by = accountuser.id
            obj.datamode = "A" if obj.datamode == "I" else "I"
            obj.save()
            result = True
            message = 'Success'
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, message


# ══════════════════════════════════════════════════════════════════════════════
# HERO BANNER API FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

@app_logger.functionlogs(log=log_name)
def hero_banner_load_data(request, table_data):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    fResult = list()
    try:
        queryset = HeroBanner.objects.exclude(datamode='D').order_by('sort_order')
        qs, total_records, total_display_records = app_utils.method_for_datatable_operations(
            request, queryset)

        final_data = list()
        for qs_instance in qs:
            qs_data = model_to_dict(qs_instance)
            data = list()
            edit_url = reverse('mck_website:mck_hero_banner_update', args=[qs_data['id']])

            for column in table_data['columns']:
                if column['column_name'] == "datamode":
                    if qs_instance.datamode == "A":
                        data.append('<span class="badge bg-success">Active</span>')
                        data.append(f'<div class="text-end"><a href="{edit_url}" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void(0)" class="text-danger ps-2" onclick="delete_object({qs_data["id"]})">Inactivate</a></div>')
                    else:
                        data.append('<span class="badge bg-danger">Inactive</span>')
                        data.append(f'<div class="text-end"><a href="{edit_url}" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void(0)" class="text-success ps-2" onclick="delete_object({qs_data["id"]})">Activate</a></div>')
                else:
                    value = qs_data.get(column['column_name'], "-")
                    if isinstance(value, Decimal):
                        value = float(value)
                    data.append(value)
            final_data.append(data)
        fResult = app_utils.final_dict(request, total_records, total_display_records, final_data)
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, fResult


@app_logger.functionlogs(log=log_name)
def hero_banner_retrieve_data(request, id):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        obj = HeroBanner.objects.filter(id=id).first()
        if obj:
            data['hero_banner'] = obj
            result, msg = True, success_msg
        else:
            result, msg, data = True, success_msg, data
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def hero_banner_create_update(request, id=None, mode=None):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        accountuser = auth_api.get_request_accountuser(request)
        pDict = request.POST

        if mode == 'edit' and id:
            obj = HeroBanner.objects.filter(id=id).first()
            if not obj:
                error_msg = "HeroBanner not found"
                return False, error_msg, data
        else:
            obj = HeroBanner()
            obj.created_by = accountuser.id

        obj.title = pDict.get('title', '')
        obj.sort_order = pDict.get('sort_order') or 1
        obj.is_active = True if pDict.get('is_active') else False

        if request.FILES.get('desktop_image'):
            obj.desktop_image = request.FILES.get('desktop_image')

        if request.FILES.get('mobile_image'):
            obj.mobile_image = request.FILES.get('mobile_image')

        obj.updated_by = accountuser.id
        obj.save()
        data['hero_banner'] = obj
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def hero_banner_update_status(request, id):
    result = False
    message = 'Error'
    try:
        accountuser = auth_api.get_request_accountuser(request)
        obj = HeroBanner.objects.filter(id=id).first()
        if obj:
            obj.updated_by = accountuser.id
            obj.datamode = "A" if obj.datamode == "I" else "I"
            obj.save()
            result = True
            message = 'Success'
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, message


# ══════════════════════════════════════════════════════════════════════════════
# CUSTOMER API FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

@app_logger.functionlogs(log=log_name)
def customer_load_data(request, table_data):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    fResult = list()
    try:
        queryset = Customer.objects.exclude(datamode='D').order_by('-updated_on')
        qs, total_records, total_display_records = app_utils.method_for_datatable_operations(request, queryset)
        final_data = []
        for qs_instance in qs:
            qs_data = model_to_dict(qs_instance)
            data = []
            edit_url = reverse('mck_website:mck_customer_update', args=[qs_data['id']])
            for column in table_data['columns']:
                if column['column_name'] == 'datamode':
                    if qs_instance.datamode == "A":
                        data.append('<span class="badge bg-success">Active</span>')
                        data.append(f'<div class="text-end"><a href="{edit_url}" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void(0)" class="text-danger ps-2" onclick="delete_object({qs_data["id"]})">Inactivate</a></div>')
                    else:
                        data.append('<span class="badge bg-danger">Inactive</span>')
                        data.append(f'<div class="text-end"><a href="{edit_url}" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void(0)" class="text-success ps-2" onclick="delete_object({qs_data["id"]})">Activate</a></div>')
                else:
                    value = qs_data.get(column['column_name'], '-')
                    if isinstance(value, Decimal):
                        value = float(value)
                    elif isinstance(value, (datetime, date)):
                        value = value.strftime('%Y-%m-%d %H:%M')
                    data.append(str(value) if value is not None else '-')
            final_data.append(data)
        fResult = app_utils.final_dict(request, total_records, total_display_records, final_data)
        result, msg = True, 'Success'
    except Exception as e:
        result, msg = False, 'Internal Server Error'
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, fResult


@app_logger.functionlogs(log=log_name)
def customer_retrieve_data(request, id):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        obj = Customer.objects.filter(id=id).first()
        if obj:
            data['customer'] = obj
            result, msg = True, success_msg
        else:
            result, msg, data = True, success_msg, data
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def customer_create_update(request, id=None, mode=None):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        accountuser = auth_api.get_request_accountuser(request)
        p = request.POST
        if mode == 'edit' and id:
            obj = Customer.objects.filter(id=id).first()
            if not obj:
                error_msg = "Customer not found"
                return False, error_msg, data
        else:
            obj = Customer()
            obj.created_by = accountuser.id
            
        obj.first_name = p.get('first_name')
        obj.last_name = p.get('last_name')
        obj.email = p.get('email')
        obj.phone = p.get('phone')
        obj.gender = p.get('gender')
        obj.date_of_birth = p.get('date_of_birth') or None
        obj.is_verified = True if p.get('is_verified') else False
        obj.is_subscribed = True if p.get('is_subscribed') else False
        
        if request.FILES.get('profile_image'):
            obj.profile_image = request.FILES.get('profile_image')
            
        obj.updated_by = accountuser.id
        obj.save()
        data['customer'] = obj
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def customer_update_status(request, id):
    result = False
    message = 'Error'
    try:
        accountuser = auth_api.get_request_accountuser(request)
        obj = Customer.objects.filter(id=id).first()
        if obj:
            obj.updated_by = accountuser.id
            obj.datamode = "A" if obj.datamode == "I" else "I"
            obj.save()
            result = True
            message = 'Success'
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, message


# ══════════════════════════════════════════════════════════════════════════════
# ADDRESS API FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

@app_logger.functionlogs(log=log_name)
def address_load_data(request, table_data):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    fResult = list()
    try:
        queryset = Address.objects.exclude(datamode='D').order_by('-updated_on')
        qs, total_records, total_display_records = app_utils.method_for_datatable_operations(request, queryset)
        final_data = []
        for qs_instance in qs:
            qs_data = model_to_dict(qs_instance)
            data = []
            edit_url = reverse('mck_website:mck_address_update', args=[qs_data['id']])
            for column in table_data['columns']:
                if column['column_name'] == 'datamode':
                    if qs_instance.datamode == "A":
                        data.append('<span class="badge bg-success">Active</span>')
                        data.append(f'<div class="text-end"><a href="{edit_url}" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void(0)" class="text-danger ps-2" onclick="delete_object({qs_data["id"]})">Inactivate</a></div>')
                    else:
                        data.append('<span class="badge bg-danger">Inactive</span>')
                        data.append(f'<div class="text-end"><a href="{edit_url}" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void(0)" class="text-success ps-2" onclick="delete_object({qs_data["id"]})">Activate</a></div>')
                elif column['column_name'] == 'user':
                    user_info = f"{qs_instance.user.first_name} {qs_instance.user.last_name}" if qs_instance.user else '-'
                    data.append(user_info)
                else:
                    value = qs_data.get(column['column_name'], '-')
                    if isinstance(value, (datetime, date)):
                        value = value.strftime('%Y-%m-%d %H:%M')
                    data.append(str(value) if value is not None else '-')
            final_data.append(data)
        fResult = app_utils.final_dict(request, total_records, total_display_records, final_data)
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, fResult


@app_logger.functionlogs(log=log_name)
def address_retrieve_data(request, id):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        obj = Address.objects.filter(id=id).first()
        if obj:
            data['address'] = obj
            if obj.user:
                data['user_name'] = f"{obj.user.first_name} {obj.user.last_name}"
                data['user_email'] = obj.user.email
            result, msg = True, success_msg
        else:
            result, msg, data = True, success_msg, data
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def address_create_update(request, id=None, mode=None):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        accountuser = auth_api.get_request_accountuser(request)
        p = request.POST
        
        if mode == 'edit' and id:
            obj = Address.objects.filter(id=id).first()
            if not obj:
                error_msg = "Address not found"
                return False, error_msg, data
        else:
            obj = Address()
            obj.created_by = accountuser.id
        
        user_id = p.get('user') or p.get('user_id')
        if user_id:
            obj.user_id = user_id
        elif accountuser:
            obj.user = accountuser
        
        obj.address_type = p.get('address_type')
        obj.full_name = p.get('full_name')
        obj.phone = p.get('phone')
        obj.address_line1 = p.get('address_line1')
        obj.address_line2 = p.get('address_line2', '')
        obj.city = p.get('city')
        obj.state = p.get('state')
        obj.pincode = p.get('pincode')
        obj.country = p.get('country', 'India')
        obj.is_default = True if p.get('is_default') else False
        obj.updated_by = accountuser.id
        
        if obj.is_default and obj.user:
            Address.objects.filter(user=obj.user, is_default=True).exclude(id=obj.id).update(is_default=False)
        
        obj.save()
        data['address'] = obj
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def address_update_status(request, id):
    result = False
    message = 'Error'
    try:
        accountuser = auth_api.get_request_accountuser(request)
        obj = Address.objects.filter(id=id).first()
        if obj:
            obj.updated_by = accountuser.id
            obj.datamode = "A" if obj.datamode == "I" else "I"
            obj.save()
            result = True
            message = 'Success'
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, message


# ══════════════════════════════════════════════════════════════════════════════
# COUPON API FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

@app_logger.functionlogs(log=log_name)
def coupon_load_data(request, table_data):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    fResult = list()
    try:
        queryset = Coupon.objects.exclude(datamode='D').order_by('-updated_on')
        qs, total_records, total_display_records = app_utils.method_for_datatable_operations(request, queryset)
        final_data = []
        for qs_instance in qs:
            qs_data = model_to_dict(qs_instance)
            data = []
            edit_url = reverse('mck_website:mck_coupon_update', args=[qs_data['id']])
            for column in table_data['columns']:
                if column['column_name'] == 'datamode':
                    if qs_instance.datamode == "A":
                        data.append('<span class="badge bg-success">Active</span>')
                        data.append(f'<div class="text-end"><a href="{edit_url}" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void(0)" class="text-danger ps-2" onclick="delete_object({qs_data["id"]})">Inactivate</a></div>')
                    else:
                        data.append('<span class="badge bg-danger">Inactive</span>')
                        data.append(f'<div class="text-end"><a href="{edit_url}" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void(0)" class="text-success ps-2" onclick="delete_object({qs_data["id"]})">Activate</a></div>')
                else:
                    value = qs_data.get(column['column_name'], '-')
                    if isinstance(value, Decimal):
                        value = float(value)
                    elif isinstance(value, (datetime, date)):
                        value = value.strftime('%Y-%m-%d')
                    data.append(str(value) if value is not None else '-')
            final_data.append(data)
        fResult = app_utils.final_dict(request, total_records, total_display_records, final_data)
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, fResult


@app_logger.functionlogs(log=log_name)
def coupon_retrieve_data(request, id):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        obj = Coupon.objects.filter(id=id).first()
        if obj:
            data['coupon'] = obj
            result, msg = True, success_msg
        else:
            result, msg, data = True, success_msg, data
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def coupon_create_update(request, id=None, mode=None):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        accountuser = auth_api.get_request_accountuser(request)
        p = request.POST
        
        if mode == 'edit' and id:
            obj = Coupon.objects.filter(id=id).first()
            if not obj:
                error_msg = "Coupon not found"
                return False, error_msg, data
        else:
            obj = Coupon()
            obj.created_by = accountuser.id
            
        obj.code = p.get('code')
        obj.description = p.get('description', '')
        obj.discount_type = p.get('discount_type')
        obj.discount_value = p.get('discount_value') or 0
        obj.minimum_order_amount = p.get('minimum_order_amount') or 0
        obj.maximum_discount_amount = p.get('maximum_discount_amount') or None
        obj.usage_limit = p.get('usage_limit') or None
        obj.per_user_limit = p.get('per_user_limit') or 1
        obj.valid_from = p.get('valid_from')
        obj.valid_until = p.get('valid_until')
        obj.is_active = True if p.get('is_active') else False
        obj.updated_by = accountuser.id
        obj.save()
        data['coupon'] = obj
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def coupon_update_status(request, id):
    result = False
    message = 'Error'
    try:
        accountuser = auth_api.get_request_accountuser(request)
        obj = Coupon.objects.filter(id=id).first()
        if obj:
            obj.updated_by = accountuser.id
            obj.datamode = "A" if obj.datamode == "I" else "I"
            obj.save()
            result = True
            message = 'Success'
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, message


# ══════════════════════════════════════════════════════════════════════════════
# PAYMENT GATEWAY API FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

@app_logger.functionlogs(log=log_name)
def payment_gateway_load_data(request, table_data):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    fResult = list()
    try:
        queryset = PaymentGateway.objects.exclude(datamode='D').order_by('sort_order')
        qs, total_records, total_display_records = app_utils.method_for_datatable_operations(request, queryset)
        final_data = []
        for qs_instance in qs:
            qs_data = model_to_dict(qs_instance)
            data = []
            edit_url = reverse('mck_website:mck_payment_gateway_update', args=[qs_data['id']])
            for column in table_data['columns']:
                if column['column_name'] == 'datamode':
                    if qs_instance.datamode == "A":
                        data.append('<span class="badge bg-success">Active</span>')
                        data.append(f'<div class="text-end"><a href="{edit_url}" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void(0)" class="text-danger ps-2" onclick="delete_object({qs_data["id"]})">Inactivate</a></div>')
                    else:
                        data.append('<span class="badge bg-danger">Inactive</span>')
                        data.append(f'<div class="text-end"><a href="{edit_url}" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void(0)" class="text-success ps-2" onclick="delete_object({qs_data["id"]})">Activate</a></div>')
                else:
                    value = qs_data.get(column['column_name'], '-')
                    if isinstance(value, (datetime, date)):
                        value = value.strftime('%Y-%m-%d %H:%M')
                    data.append(str(value) if value is not None else '-')
            final_data.append(data)
        fResult = app_utils.final_dict(request, total_records, total_display_records, final_data)
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, fResult


@app_logger.functionlogs(log=log_name)
def payment_gateway_retrieve_data(request, id):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        obj = PaymentGateway.objects.filter(id=id).first()
        if obj:
            data['payment_gateway'] = obj
            result, msg = True, success_msg
        else:
            result, msg, data = True, success_msg, data
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def payment_gateway_create_update(request, id=None, mode=None):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        accountuser = auth_api.get_request_accountuser(request)
        p = request.POST
        
        if mode == 'edit' and id:
            obj = PaymentGateway.objects.filter(id=id).first()
            if not obj:
                error_msg = "PaymentGateway not found"
                return False, error_msg, data
        else:
            obj = PaymentGateway()
            obj.created_by = accountuser.id
            
        obj.name = p.get('name')
        obj.code = p.get('code')
        obj.description = p.get('description', '')
        obj.is_active = True if p.get('is_active') else False
        obj.sort_order = p.get('sort_order') or 1
        obj.config_json = p.get('config_json', '')
        
        if request.FILES.get('logo'):
            obj.logo = request.FILES.get('logo')
            
        obj.updated_by = accountuser.id
        obj.save()
        data['payment_gateway'] = obj
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def payment_gateway_update_status(request, id):
    result = False
    message = 'Error'
    try:
        accountuser = auth_api.get_request_accountuser(request)
        obj = PaymentGateway.objects.filter(id=id).first()
        if obj:
            obj.updated_by = accountuser.id
            obj.datamode = "A" if obj.datamode == "I" else "I"
            obj.save()
            result = True
            message = 'Success'
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, message


# ══════════════════════════════════════════════════════════════════════════════
# CART API FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

@app_logger.functionlogs(log=log_name)
def cart_load_data(request, table_data):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    fResult = list()
    try:
        queryset = Cart.objects.exclude(datamode='D').order_by('-updated_on')
        qs, total_records, total_display_records = app_utils.method_for_datatable_operations(request, queryset)
        final_data = []
        for qs_instance in qs:
            qs_data = model_to_dict(qs_instance)
            data = []
            try:
                edit_url = reverse('mck_website:mck_cart_list')
            except NoReverseMatch:
                edit_url = '#'
            
            for column in table_data['columns']:
                if column['column_name'] == 'datamode':
                    if qs_instance.datamode == "A":
                        data.append('<span class="badge bg-success">Active</span>')
                        data.append(f'<div class="text-end"><a href="{edit_url}" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void(0)" class="text-danger ps-2" onclick="delete_object({qs_data["id"]})">Inactivate</a></div>')
                    else:
                        data.append('<span class="badge bg-danger">Inactive</span>')
                        data.append(f'<div class="text-end"><a href="{edit_url}" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void(0)" class="text-success ps-2" onclick="delete_object({qs_data["id"]})">Activate</a></div>')
                elif column['column_name'] == 'user':
                    if qs_instance.user:
                        user_display = str(qs_instance.user)
                        if hasattr(qs_instance.user, 'get_full_name'):
                            full_name = qs_instance.user.get_full_name()
                            if full_name:
                                user_display = f"{full_name} ({qs_instance.user.email})"
                        data.append(user_display)
                    else:
                        data.append('Guest')
                else:
                    value = qs_data.get(column['column_name'], '-')
                    if isinstance(value, (datetime, date)):
                        value = value.strftime('%Y-%m-%d %H:%M')
                    data.append(str(value) if value is not None else '-')
            final_data.append(data)
        fResult = app_utils.final_dict(request, total_records, total_display_records, final_data)
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, fResult


@app_logger.functionlogs(log=log_name)
def cart_retrieve_data(request, id):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        obj = Cart.objects.filter(id=id).first()
        if obj:
            data['cart'] = obj
            data['user_id'] = obj.user.id if obj.user else None
            data['username'] = str(obj.user) if obj.user else 'Anonymous'
            result, msg = True, success_msg
        else:
            result, msg, data = True, success_msg, data
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def cart_create_update(request, id=None, mode=None):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        accountuser = auth_api.get_request_accountuser(request)
        p = request.POST
        
        if mode == 'edit' and id:
            obj = Cart.objects.filter(id=id).first()
            if not obj:
                error_msg = "Cart not found"
                return False, error_msg, data
        else:
            obj = Cart()
            obj.created_by = accountuser.id
        
        if request.user.is_authenticated:
            obj.user = request.user
        
        if not request.user.is_authenticated:
            obj.session_key = p.get('session_key', request.session.session_key or '')
        
        obj.coupon_id = p.get('coupon') or None
        obj.updated_by = accountuser.id
        obj.save()
        
        data['cart'] = obj
        data['user_assigned'] = bool(obj.user)
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def cart_update_status(request, id):
    result = False
    message = 'Error'
    try:
        accountuser = auth_api.get_request_accountuser(request)
        obj = Cart.objects.filter(id=id).first()
        if obj:
            obj.updated_by = accountuser.id
            obj.datamode = "A" if obj.datamode == "I" else "I"
            obj.save()
            result = True
            message = 'Success'
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, message


# ══════════════════════════════════════════════════════════════════════════════
# CART ITEM API FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

@app_logger.functionlogs(log=log_name)
def cart_item_load_data(request, table_data):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    fResult = list()
    try:
        queryset = CartItem.objects.exclude(datamode='D').order_by('-updated_on')
        qs, total_records, total_display_records = app_utils.method_for_datatable_operations(request, queryset)
        final_data = []
        for qs_instance in qs:
            qs_data = model_to_dict(qs_instance)
            data = []
            edit_url = reverse('mck_website:mck_cart_item_update', args=[qs_data['id']])
            for column in table_data['columns']:
                if column['column_name'] == 'datamode':
                    if qs_instance.datamode == "A":
                        data.append('<span class="badge bg-success">Active</span>')
                        data.append(f'<div class="text-end"><a href="{edit_url}" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void(0)" class="text-danger ps-2" onclick="delete_object({qs_data["id"]})">Inactivate</a></div>')
                    else:
                        data.append('<span class="badge bg-danger">Inactive</span>')
                        data.append(f'<div class="text-end"><a href="{edit_url}" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void(0)" class="text-success ps-2" onclick="delete_object({qs_data["id"]})">Activate</a></div>')
                elif column['column_name'] == 'product':
                    data.append(str(qs_instance.product))
                elif column['column_name'] == 'cart':
                    data.append(str(qs_instance.cart))
                else:
                    value = qs_data.get(column['column_name'], '-')
                    if isinstance(value, Decimal):
                        value = float(value)
                    data.append(str(value) if value is not None else '-')
            final_data.append(data)
        fResult = app_utils.final_dict(request, total_records, total_display_records, final_data)
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, fResult


@app_logger.functionlogs(log=log_name)
def cart_item_retrieve_data(request, id):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        obj = CartItem.objects.filter(id=id).first()
        if obj:
            data['cart_item'] = obj
            result, msg = True, success_msg
        else:
            result, msg, data = True, success_msg, data
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def cart_item_create_update(request, id=None, mode=None):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        accountuser = auth_api.get_request_accountuser(request)
        p = request.POST
        
        if mode == 'edit' and id:
            obj = CartItem.objects.filter(id=id).first()
            if not obj:
                error_msg = "CartItem not found"
                return False, error_msg, data
        else:
            obj = CartItem()
            obj.created_by = accountuser.id
            
        obj.cart_id = p.get('cart')
        obj.product_id = p.get('product')
        obj.quantity = p.get('quantity') or 1
        obj.price = p.get('price') or 0
        obj.updated_by = accountuser.id
        obj.save()
        data['cart_item'] = obj
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def cart_item_update_status(request, id):
    result = False
    message = 'Error'
    try:
        accountuser = auth_api.get_request_accountuser(request)
        obj = CartItem.objects.filter(id=id).first()
        if obj:
            obj.updated_by = accountuser.id
            obj.datamode = "A" if obj.datamode == "I" else "I"
            obj.save()
            result = True
            message = 'Success'
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, message


# ══════════════════════════════════════════════════════════════════════════════
# ORDER API FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

@app_logger.functionlogs(log=log_name)
def order_load_data(request, table_data):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    fResult = list()
    try:
        queryset = Order.objects.exclude(datamode='D').order_by('-updated_on')
        qs, total_records, total_display_records = app_utils.method_for_datatable_operations(
            request, queryset)

        final_data = list()
        for qs_instance in qs:
            qs_data = model_to_dict(qs_instance)
            data = list()
            edit_url = reverse('mck_website:mck_order_update', args=[qs_data['id']])
            items_url = reverse('mck_website:mck_order_item_list', args=[qs_data['id']])

            for column in table_data['columns']:
                if column['column_name'] == 'datamode':
                    if qs_instance.datamode == "A":
                        data.append('<span class="badge bg-success">Active</span>')
                        data.append(f'<div class="text-end"><a href="{edit_url}" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void(0)" class="text-danger ps-2" onclick="delete_object({qs_data["id"]})">Inactivate</a></div>')
                    else:
                        data.append('<span class="badge bg-danger">Inactive</span>')
                        data.append(f'<div class="text-end"><a href="{edit_url}" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void(0)" class="text-success ps-2" onclick="delete_object({qs_data["id"]})">Activate</a></div>')
                elif column['column_name'] == 'user':
                    customer_name = "Guest"
                    if qs_instance.user:
                        customer_name = f"{qs_instance.user.first_name} {qs_instance.user.last_name}".strip() or qs_instance.user.email
                    data.append(customer_name)
                elif column['column_name'] == 'status':
                    status_colors = {
                        'pending': 'warning',
                        'confirmed': 'info',
                        'processing': 'primary',
                        'shipped': 'success',
                        'delivered': 'success',
                        'cancelled': 'danger',
                        'returned': 'secondary',
                        'refunded': 'dark'
                    }
                    status_display = qs_instance.get_status_display()
                    color = status_colors.get(qs_instance.status, 'secondary')
                    data.append(f'<span class="badge bg-{color}">{status_display}</span>')
                elif column['column_name'] == 'total_amount':
                    data.append(f'<strong>₹{float(qs_data.get("total_amount", 0)):.2f}</strong>')
                elif column['column_name'] == 'items_count':
                    item_count = qs_instance.items.filter(datamode='A').count()
                    if item_count > 0:
                        data.append(f'<a href="{items_url}" class="btn btn-sm btn-info">{item_count} items</a>')
                    else:
                        data.append('<span class="text-muted">0</span>')
                elif column['column_name'] == 'order_number':
                    data.append(f'<a href="{edit_url}" class="text-primary">{qs_data.get("order_number", "-")}</a>')
                else:
                    value = qs_data.get(column['column_name'], "-")
                    if isinstance(value, (datetime, date)):
                        value = value.strftime('%Y-%m-%d %H:%M')
                    data.append(value)
            final_data.append(data)
        fResult = app_utils.final_dict(request, total_records, total_display_records, final_data)
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, fResult


@app_logger.functionlogs(log=log_name)
def order_retrieve_data(request, id):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        order = Order.objects.filter(id=id).first()
        if order:
            data['order'] = order
            data['items'] = order.items.filter(datamode='A')
            result, msg = True, success_msg
        else:
            result, msg, data = True, success_msg, data
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def order_create_update(request, id=None, mode=None):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        accountuser = auth_api.get_request_accountuser(request)
        pDict = request.POST
        
        if mode == 'edit' and id:
            obj = Order.objects.filter(id=id).first()
            if not obj:
                error_msg = "Order not found"
                return False, error_msg, data
        else:
            obj = Order()
            obj.created_by = accountuser.id
            if not pDict.get('order_number'):
                obj.order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{Order.objects.count() + 1:04d}"
        
        obj.order_number = pDict.get('order_number', obj.order_number)
        obj.status = pDict.get('status', 'pending')
        obj.subtotal = pDict.get('subtotal', 0)
        obj.discount_amount = pDict.get('discount_amount', 0)
        obj.shipping_charge = pDict.get('shipping_charge', 0)
        obj.tax_amount = pDict.get('tax_amount', 0)
        obj.total_amount = pDict.get('total_amount', 0)
        obj.notes = pDict.get('notes', '')
        
        obj.shipping_full_name = pDict.get('shipping_full_name', '')
        obj.shipping_phone = pDict.get('shipping_phone', '')
        obj.shipping_address_line1 = pDict.get('shipping_address_line1', '')
        obj.shipping_address_line2 = pDict.get('shipping_address_line2', '')
        obj.shipping_city = pDict.get('shipping_city', '')
        obj.shipping_state = pDict.get('shipping_state', '')
        obj.shipping_pincode = pDict.get('shipping_pincode', '')
        obj.shipping_country = pDict.get('shipping_country', 'India')
        
        if pDict.get('user'):
            obj.user_id = pDict.get('user')
        if pDict.get('coupon'):
            obj.coupon_id = pDict.get('coupon')
        if pDict.get('delivered_on'):
            obj.delivered_on = pDict.get('delivered_on')
        
        obj.updated_by = accountuser.id
        obj.save()
        
        data['order'] = obj
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def order_update_status(request, id):
    result = False
    message = 'Error'
    try:
        accountuser = auth_api.get_request_accountuser(request)
        obj = Order.objects.filter(id=id).first()
        if obj:
            obj.updated_by = accountuser.id
            obj.datamode = "A" if obj.datamode == "I" else "I"
            obj.save()
            result = True
            message = 'Success'
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, message


# ══════════════════════════════════════════════════════════════════════════════
# ORDER ITEM API FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

@app_logger.functionlogs(log=log_name)
def order_item_load_data(request, table_data, order_id=None):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    fResult = list()
    try:
        if order_id:
            queryset = OrderItem.objects.filter(order_id=order_id, datamode__in=['A', 'I']).order_by('-updated_on')
        else:
            queryset = OrderItem.objects.exclude(datamode='D').order_by('-updated_on')
        
        qs, total_records, total_display_records = app_utils.method_for_datatable_operations(request, queryset)

        final_data = list()
        for qs_instance in qs:
            qs_data = model_to_dict(qs_instance)
            data = list()
            edit_url = reverse('mck_website:mck_order_item_update', args=[qs_data['id']])

            for column in table_data['columns']:
                if column['column_name'] == 'datamode':
                    if qs_instance.datamode == "A":
                        data.append('<span class="badge bg-success">Active</span>')
                        data.append(f'<div class="text-end"><a href="{edit_url}" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void(0)" class="text-danger ps-2" onclick="delete_object({qs_data["id"]})">Inactivate</a></div>')
                    else:
                        data.append('<span class="badge bg-danger">Inactive</span>')
                        data.append(f'<div class="text-end"><a href="{edit_url}" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void(0)" class="text-success ps-2" onclick="delete_object({qs_data["id"]})">Activate</a></div>')
                elif column['column_name'] == 'unit_price':
                    data.append(f'₹{float(qs_data.get("unit_price", 0)):.2f}')
                elif column['column_name'] == 'total_price':
                    data.append(f'<strong>₹{float(qs_data.get("total_price", 0)):.2f}</strong>')
                elif column['column_name'] == 'order':
                    order_url = reverse('mck_website:mck_order_update', args=[qs_instance.order.id])
                    data.append(f'<a href="{order_url}">{qs_instance.order.order_number}</a>')
                elif column['column_name'] == 'product_name':
                    product_url = reverse('mck_website:mck_product_update', args=[qs_instance.product.id]) if qs_instance.product else '#'
                    data.append(f'<a href="{product_url}">{qs_data.get("product_name", "-")}</a>')
                elif column['column_name'] == 'quantity':
                    data.append(f'<span class="badge bg-secondary">{qs_data.get("quantity", 0)}</span>')
                else:
                    data.append(qs_data.get(column['column_name'], "-"))
            final_data.append(data)
        fResult = app_utils.final_dict(request, total_records, total_display_records, final_data)
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, fResult


@app_logger.functionlogs(log=log_name)
def order_item_retrieve_data(request, id):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        order_item = OrderItem.objects.filter(id=id).first()
        if order_item:
            data['order_item'] = order_item
            data['order'] = order_item.order
            result, msg = True, success_msg
        else:
            result, msg, data = True, success_msg, data
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def order_item_create_update(request, id=None, mode=None, order_id=None):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        accountuser = auth_api.get_request_accountuser(request)
        pDict = request.POST
        
        if mode == 'edit' and id:
            obj = OrderItem.objects.filter(id=id).first()
            if not obj:
                error_msg = "OrderItem not found"
                return False, error_msg, data
        else:
            obj = OrderItem()
            obj.created_by = accountuser.id
            if order_id:
                obj.order_id = order_id
        
        if pDict.get('order'):
            obj.order_id = pDict.get('order')
        
        if pDict.get('product'):
            product = Product.objects.filter(id=pDict.get('product')).first()
            if product:
                obj.product = product
                if not pDict.get('product_name'):
                    obj.product_name = product.name
                if not pDict.get('product_sku'):
                    obj.product_sku = product.sku
        
        obj.product_name = pDict.get('product_name', obj.product_name)
        obj.product_sku = pDict.get('product_sku', obj.product_sku)
        obj.product_image = pDict.get('product_image', obj.product_image)
        obj.unit_price = pDict.get('unit_price', 0)
        obj.quantity = pDict.get('quantity', 1)
        
        if pDict.get('total_price'):
            obj.total_price = pDict.get('total_price')
        else:
            obj.total_price = float(obj.unit_price) * int(obj.quantity)
        
        obj.updated_by = accountuser.id
        obj.save()
        
        data['order_item'] = obj
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def order_item_update_status(request, id):
    result = False
    message = 'Error'
    try:
        accountuser = auth_api.get_request_accountuser(request)
        obj = OrderItem.objects.filter(id=id).first()
        if obj:
            obj.updated_by = accountuser.id
            obj.datamode = "A" if obj.datamode == "I" else "I"
            obj.save()
            result = True
            message = 'Success'
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, message


# ══════════════════════════════════════════════════════════════════════════════
# PRODUCT REVIEW API FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

@app_logger.functionlogs(log=log_name)
def product_review_load_data(request, table_data):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    fResult = list()
    try:
        queryset = ProductReview.objects.exclude(datamode='D').order_by('-updated_on')
        qs, total_records, total_display_records = app_utils.method_for_datatable_operations(request, queryset)
        final_data = []
        for qs_instance in qs:
            qs_data = model_to_dict(qs_instance)
            data = []
            edit_url = reverse('mck_website:mck_product_review_update', args=[qs_data['id']])
            for column in table_data['columns']:
                if column['column_name'] == 'datamode':
                    if qs_instance.datamode == "A":
                        data.append('<span class="badge bg-success">Active</span>')
                        data.append(f'<div class="text-end"><a href="{edit_url}" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void(0)" class="text-danger ps-2" onclick="delete_object({qs_data["id"]})">Inactivate</a></div>')
                    else:
                        data.append('<span class="badge bg-danger">Inactive</span>')
                        data.append(f'<div class="text-end"><a href="{edit_url}" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void(0)" class="text-success ps-2" onclick="delete_object({qs_data["id"]})">Activate</a></div>')
                elif column['column_name'] == 'product':
                    data.append(str(qs_instance.product))
                elif column['column_name'] == 'customer':
                    data.append(str(qs_instance.customer) if qs_instance.customer else '-')
                else:
                    value = qs_data.get(column['column_name'], '-')
                    if isinstance(value, (datetime, date)):
                        value = value.strftime('%Y-%m-%d %H:%M')
                    data.append(str(value) if value is not None else '-')
            final_data.append(data)
        fResult = app_utils.final_dict(request, total_records, total_display_records, final_data)
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, fResult


@app_logger.functionlogs(log=log_name)
def product_review_retrieve_data(request, id):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        obj = ProductReview.objects.filter(id=id).first()
        if obj:
            data['product_review'] = obj
            result, msg = True, success_msg
        else:
            result, msg, data = True, success_msg, data
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def product_review_create_update(request, id=None, mode=None):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        accountuser = auth_api.get_request_accountuser(request)
        p = request.POST
        
        if mode == 'edit' and id:
            obj = ProductReview.objects.filter(id=id).first()
            if not obj:
                error_msg = "ProductReview not found"
                return False, error_msg, data
        else:
            obj = ProductReview()
            obj.created_by = accountuser.id
            
        obj.product_id = p.get('product')
        obj.customer_id = p.get('customer') or None
        obj.order_item_id = p.get('order_item') or None
        obj.rating = p.get('rating') or 1
        obj.title = p.get('title', '')
        obj.body = p.get('body')
        obj.is_approved = True if p.get('is_approved') else False
        obj.updated_by = accountuser.id
        obj.save()
        data['product_review'] = obj
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def product_review_update_status(request, id):
    result = False
    message = 'Error'
    try:
        accountuser = auth_api.get_request_accountuser(request)
        obj = ProductReview.objects.filter(id=id).first()
        if obj:
            obj.updated_by = accountuser.id
            obj.datamode = "A" if obj.datamode == "I" else "I"
            obj.save()
            result = True
            message = 'Success'
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, message


# ══════════════════════════════════════════════════════════════════════════════
# NEWSLETTER API FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

@app_logger.functionlogs(log=log_name)
def newsletter_load_data(request, table_data):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    fResult = list()
    try:
        queryset = Newsletter.objects.exclude(datamode='D').order_by('-updated_on')
        qs, total_records, total_display_records = app_utils.method_for_datatable_operations(request, queryset)
        final_data = []
        for qs_instance in qs:
            qs_data = model_to_dict(qs_instance)
            data = []
            for column in table_data['columns']:
                if column['column_name'] == 'datamode':
                    if qs_instance.datamode == "A":
                        data.append('<span class="badge bg-success">Active</span>')
                        data.append(f'<div class="text-end"><a href="javascript:void(0)" class="text-danger ps-2" onclick="delete_object({qs_data["id"]})">Inactivate</a></div>')
                    else:
                        data.append('<span class="badge bg-danger">Inactive</span>')
                        data.append(f'<div class="text-end"><a href="javascript:void(0)" class="text-success ps-2" onclick="delete_object({qs_data["id"]})">Activate</a></div>')
                else:
                    value = qs_data.get(column['column_name'], '-')
                    if isinstance(value, (datetime, date)):
                        value = value.strftime('%Y-%m-%d %H:%M')
                    data.append(str(value) if value is not None else '-')
            final_data.append(data)
        fResult = app_utils.final_dict(request, total_records, total_display_records, final_data)
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, fResult


@app_logger.functionlogs(log=log_name)
def newsletter_retrieve_data(request, id):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        obj = Newsletter.objects.filter(id=id).first()
        if obj:
            data['newsletter'] = obj
            result, msg = True, success_msg
        else:
            result, msg, data = True, success_msg, data
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def newsletter_create_update(request, id=None, mode=None):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        accountuser = auth_api.get_request_accountuser(request)
        p = request.POST
        
        if mode == 'edit' and id:
            obj = Newsletter.objects.filter(id=id).first()
            if not obj:
                error_msg = "Newsletter not found"
                return False, error_msg, data
        else:
            obj = Newsletter()
            obj.created_by = accountuser.id
            
        obj.email = p.get('email')
        obj.is_active = True if p.get('is_active') else False
        obj.updated_by = accountuser.id
        obj.save()
        data['newsletter'] = obj
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def newsletter_update_status(request, id):
    result = False
    message = 'Error'
    try:
        accountuser = auth_api.get_request_accountuser(request)
        obj = Newsletter.objects.filter(id=id).first()
        if obj:
            obj.updated_by = accountuser.id
            obj.datamode = "A" if obj.datamode == "I" else "I"
            obj.save()
            result = True
            message = 'Success'
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, message


# ══════════════════════════════════════════════════════════════════════════════
# CONTACT US API FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

@app_logger.functionlogs(log=log_name)
def contact_us_load_data(request, table_data):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    fResult = list()
    try:
        queryset = Contact.objects.exclude(datamode='D').order_by('-updated_on')
        qs, total_records, total_display_records = app_utils.method_for_datatable_operations(request, queryset)
        final_data = []
        for qs_instance in qs:
            qs_data = model_to_dict(qs_instance)
            data = []
            edit_url = reverse('mck_website:mck_contact_us_update', args=[qs_data['id']])
            for column in table_data['columns']:
                if column['column_name'] == 'datamode':
                    if qs_instance.datamode == "A":
                        data.append('<span class="badge bg-success">Active</span>')
                        data.append(f'<div class="text-end"><a href="{edit_url}" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void(0)" class="text-danger ps-2" onclick="delete_object({qs_data["id"]})">Inactivate</a></div>')
                    else:
                        data.append('<span class="badge bg-danger">Inactive</span>')
                        data.append(f'<div class="text-end"><a href="{edit_url}" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void(0)" class="text-success ps-2" onclick="delete_object({qs_data["id"]})">Activate</a></div>')
                else:
                    value = qs_data.get(column['column_name'], '-')
                    if isinstance(value, (datetime, date)):
                        value = value.strftime('%Y-%m-%d %H:%M')
                    data.append(str(value) if value is not None else '-')
            final_data.append(data)
        fResult = app_utils.final_dict(request, total_records, total_display_records, final_data)
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, fResult


@app_logger.functionlogs(log=log_name)
def contact_us_retrieve_data(request, id):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        obj = Contact.objects.filter(id=id).first()
        if obj:
            data['contact_us'] = obj
            result, msg = True, success_msg
        else:
            result, msg, data = True, success_msg, data
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def contact_us_create_update(request, id=None, mode=None):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        accountuser = auth_api.get_request_accountuser(request)
        p = request.POST
        
        if mode == 'edit' and id:
            obj = Contact.objects.filter(id=id).first()
            if not obj:
                error_msg = "Contact not found"
                return False, error_msg, data
        else:
            obj = Contact()
            obj.created_by = accountuser.id
            
        obj.name = p.get('name')
        obj.email = p.get('email')
        obj.phone = p.get('phone', '')
        obj.subject = p.get('subject')
        obj.message = p.get('message')
        obj.status = p.get('status', 'new')
        obj.admin_notes = p.get('admin_notes', '')
        if p.get('replied_on'):
            obj.replied_on = p.get('replied_on')
        obj.updated_by = accountuser.id
        obj.save()
        data['contact_us'] = obj
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def contact_us_update_status(request, id):
    result = False
    message = 'Error'
    try:
        accountuser = auth_api.get_request_accountuser(request)
        obj = Contact.objects.filter(id=id).first()
        if obj:
            obj.updated_by = accountuser.id
            obj.datamode = "A" if obj.datamode == "I" else "I"
            obj.save()
            result = True
            message = 'Success'
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, message


# ══════════════════════════════════════════════════════════════════════════════
# SITE SETTINGS API FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

@app_logger.functionlogs(log=log_name)
def site_settings_retrieve_data(request):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        obj = SiteSettings.load()
        data['site_settings'] = obj
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def site_settings_update(request):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        accountuser = auth_api.get_request_accountuser(request)
        p = request.POST
        obj = SiteSettings.load()
        
        obj.site_name = p.get('site_name')
        obj.site_tagline = p.get('site_tagline', '')
        obj.site_email = p.get('site_email')
        obj.site_phone = p.get('site_phone', '')
        obj.site_phone_alt = p.get('site_phone_alt', '')
        obj.site_address = p.get('site_address', '')
        obj.facebook_url = p.get('facebook_url', '')
        obj.instagram_url = p.get('instagram_url', '')
        obj.twitter_url = p.get('twitter_url', '')
        obj.youtube_url = p.get('youtube_url', '')
        obj.linkedin_url = p.get('linkedin_url', '')
        obj.meta_title = p.get('meta_title', '')
        obj.meta_description = p.get('meta_description', '')
        obj.meta_keywords = p.get('meta_keywords', '')
        obj.google_analytics_id = p.get('google_analytics_id', '')
        obj.privacy_policy = p.get('privacy_policy', '')
        obj.terms_conditions = p.get('terms_conditions', '')
        obj.return_policy = p.get('return_policy', '')
        obj.shipping_policy = p.get('shipping_policy', '')
        obj.currency_code = p.get('currency_code', 'INR')
        obj.currency_symbol = p.get('currency_symbol', '₹')
        obj.free_shipping_above = p.get('free_shipping_above') or 0
        obj.tax_percentage = p.get('tax_percentage') or 0
        
        if request.FILES.get('site_logo'):
            obj.site_logo = request.FILES.get('site_logo')
        if request.FILES.get('site_favicon'):
            obj.site_favicon = request.FILES.get('site_favicon')
            
        obj.updated_by = accountuser.id
        obj.save()
        data['site_settings'] = obj
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


# ══════════════════════════════════════════════════════════════════════════════
# USER API FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════
@app_logger.functionlogs(log=log_name)
def user_load_data(request, table_data):
    """Load user data for datatable"""
    result, fResult = False, list()
    try:
        # Use is_active to filter (since datamode may not exist)
        queryset = User.objects.filter(is_active=True).order_by('-date_joined')
        qs, total_records, total_display_records = app_utils.method_for_datatable_operations(request, queryset)
        final_data = []
        
        for qs_instance in qs:
            qs_data = model_to_dict(qs_instance)
            data = []
            edit_url = reverse('mck_website:mck_user_update', args=[qs_data['id']])
            view_url = reverse('mck_website:mck_user_list')
            
            for column in table_data['columns']:
                if column['column_name'] == 'datamode':
                    # Use is_active for status
                    status_badge = 'success' if qs_instance.is_active else 'danger'
                    status_text = 'Active' if qs_instance.is_active else 'Inactive'
                    data.append(f'<span class="badge bg-{status_badge}">{status_text}</span>')
                    
                    # Action buttons
                    actions = f'''
                    <div class="btn-group" role="group">
                        <a href="{view_url}" class="btn btn-sm btn-info" title="View">
                            <i class="bi bi-eye"></i>
                        </a>
                        <a href="{edit_url}" class="btn btn-sm btn-primary" title="Edit">
                            <i class="bi bi-pencil"></i>
                        </a>
                        <button onclick="toggleUserStatus({qs_data['id']})" class="btn btn-sm btn-warning" title="Toggle Status">
                            <i class="bi bi-arrow-repeat"></i>
                        </button>
                        <button onclick="deleteUser({qs_data['id']})" class="btn btn-sm btn-danger" title="Delete">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                    '''
                    data.append(actions)
                    
                elif column['column_name'] == 'registration_status':
                    # Simplified registration status
                    if not qs_instance.is_profile_completed:
                        status = 'PROFILE_PENDING'
                    else:
                        status = 'COMPLETED'
                    status_map = {
                        'PROFILE_PENDING': ('warning', 'Profile Pending'),
                        'COMPLETED': ('success', 'Completed')
                    }
                    badge_class, display_text = status_map.get(status, ('secondary', status))
                    data.append(f'<span class="badge bg-{badge_class}">{display_text}</span>')
                    
                elif column['column_name'] == 'is_profile_completed':
                    icon = '✅' if qs_instance.is_profile_completed else '❌'
                    data.append(icon)
                    
                elif column['column_name'] == 'has_paid':
                    # Placeholder - remove or implement when Payment model exists
                    data.append('❌')
                    
                elif column['column_name'] == 'active_plan':
                    # Placeholder - remove or implement when Payment model exists
                    data.append('No Plan')
                    
                elif column['column_name'] == 'is_active':
                    badge = 'success' if qs_instance.is_active else 'danger'
                    status_text = 'Active' if qs_instance.is_active else 'Inactive'
                    data.append(f'<span class="badge bg-{badge}">{status_text}</span>')
                    
                elif column['column_name'] == 'mobile_number':
                    mobile = qs_instance.mobile_number
                    data.append(str(mobile.as_international) if mobile else '-')
                    
                elif column['column_name'] == 'date_joined':
                    data.append(qs_instance.date_joined.strftime('%Y-%m-%d %H:%M') if qs_instance.date_joined else '-')
                    
                elif column['column_name'] == 'last_login':
                    data.append(qs_instance.last_login.strftime('%Y-%m-%d %H:%M') if qs_instance.last_login else 'Never')
                    
                else:
                    value = qs_data.get(column['column_name'], '-')
                    data.append(str(value) if value is not None else '-')
                    
            final_data.append(data)
            
        fResult = app_utils.final_dict(request, total_records, total_display_records, final_data)
        result, msg = True, 'Success'
    except Exception as e:
        result, msg = False, 'Internal Server Error'
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, fResult


@app_logger.functionlogs(log=log_name)
def user_retrieve_data(request, id):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        obj = User.objects.filter(id=id).first()
        if obj:
            data['user'] = obj
            data['payments'] = obj.payments.all().order_by('-payment_date')
            data['payment_count'] = obj.payments.count()
            data['completed_payments'] = obj.payments.filter(status='COMPLETED').count()
            data['pending_payments'] = obj.payments.filter(status='PENDING').count()
            result, msg = True, success_msg
        else:
            result, msg, data = True, success_msg, data
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def user_create_update(request, id=None, mode=None):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        accountuser = auth_api.get_request_accountuser(request)
        p = request.POST
        
        if mode == 'edit' and id:
            obj = User.objects.filter(id=id).first()
            if not obj:
                error_msg = "User not found"
                return False, error_msg, data
        else:
            obj = User()
            obj.created_by = accountuser.id
            
        obj.username = p.get('username')
        obj.first_name = p.get('first_name', '')
        obj.last_name = p.get('last_name', '')
        obj.email = p.get('email')
        obj.mobile_number = p.get('mobile_number') or None
        obj.is_profile_completed = True if p.get('is_profile_completed') else False
        obj.is_active = True if p.get('is_active') else False
        obj.is_staff = True if p.get('is_staff') else False
        obj.is_superuser = True if p.get('is_superuser') else False
        
        password = p.get('password')
        if password:
            obj.set_password(password)
            
        obj.updated_by = accountuser.id
        obj.save()
        
        data['user'] = obj
        result, msg = True, success_msg
    except Exception as e:
        result, msg = False, error_msg
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def user_update_status(request, id):
    result = False
    message = 'Error'
    try:
        accountuser = auth_api.get_request_accountuser(request)
        obj = User.objects.filter(id=id).first()
        if obj:
            obj.updated_by = accountuser.id
            obj.datamode = "A" if obj.datamode == "I" else "I"
            obj.is_active = obj.datamode == "A"
            obj.save()
            result = True
            message = 'Success'
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, message


@app_logger.functionlogs(log=log_name)
def user_delete(request, id):
    result = False
    message = 'Error'
    try:
        accountuser = auth_api.get_request_accountuser(request)
        obj = User.objects.filter(id=id).first()
        if obj:
            obj.updated_by = accountuser.id
            obj.datamode = 'D'
            obj.is_active = False
            obj.save()
            result = True
            message = 'Success'
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, message
