import sys
from django.urls import reverse
from django.forms.models import model_to_dict
from phonenumber_field.phonenumber import PhoneNumber
from django.urls import reverse, NoReverseMatch

from config import app_utils
from config import app_logger
from mck_auth import api as auth_api
from mck_website.models import *
from mck_admin_console.models import *

log_name = "app"
logger = app_logger.createLogger(log_name)


from decimal import Decimal

app_logger.functionlogs(log=log_name)
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
                    data.append('<div class="text-success">'+qs_instance.get_datamode_display()+'</div>')
                    data.append('<div class="text-end"><a href="'+edit_url+'" class="text-primary pe-2 ps-2">Edit</a>')
                else:
                    if isinstance(qs_data.get(column['column_name']), PhoneNumber):
                        data.append(qs_data.get(column['column_name']).national_number)
                    elif isinstance(qs_data.get(column['column_name']), models.ImageField):
                        pass
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
        
        # Get category ID from request
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
            
        # Get and set the category
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

        # Handle decimal values properly
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
        elif not obj.image and mode != 'edit':
            # If no image is provided for new product, you might want to set a default or raise error
            error_msg = "Product image is required"
            return False, error_msg, data

        obj.updated_by = accountuser.id
        obj.save()
        
        # Handle many-to-many relationships if any (like additional images, tags, etc.)
        # If you have many-to-many fields, handle them here
        
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
            "is_active": obj.is_active
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
def poduct_create_update(request, id=None, mode=None):
    result = False
    success_msg = "Success"
    error_msg = 'Internal Server Error'
    data = dict()
    try:
        accountuser = auth_api.get_request_accountuser(request)
        pDict = request.POST
        if mode == 'edit' and id:
            obj = Product.objects.filter(id=id).first()
        else:
            obj = Product()
            obj.created_by = accountuser.id
            
        obj.name = pDict.get("name")
        obj.slug = pDict.get("slug")
        obj.sku = pDict.get("sku")

        obj.short_description = pDict.get(
            "short_description"
        )

        obj.description = pDict.get(
            "description"
        )

        obj.price = pDict.get("price") or 0
        obj.sale_price = pDict.get("sale_price") or 0
        obj.stock = pDict.get("stock") or 0

        obj.is_featured = (
            True if pDict.get(
                "is_featured"
            ) else False
        )

        obj.is_best_seller = (
            True if pDict.get(
                "is_best_seller"
            ) else False
        )

        obj.is_flash_sale = (
            True if pDict.get(
                "is_flash_sale"
            ) else False
        )

        obj.is_new_arrival = (
            True if pDict.get(
                "is_new_arrival"
            ) else False
        )

        obj.is_trending = (
            True if pDict.get(
                "is_trending"
            ) else False
        )

        obj.is_top_rated = (
            True if pDict.get(
                "is_top_rated"
            ) else False
        )

        obj.is_active = (
            True if pDict.get(
                "is_active"
            ) else False
        )

        if request.FILES.get("image"):
            obj.image = request.FILES.get(
                "image"
            )

        obj.updated_by = accountuser.id
        obj.save()
        data["product"] = obj
        result, msg = True, success_msg
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
            if obj.datamode == "I":
                obj.datamode = "A"
            else:
                obj.datamode = "I"
            obj.save()

        result = True
        message = 'Sucesss'
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, message






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
                    data.append('<div class="text-success">'+qs_instance.get_datamode_display()+'</div>')
                    data.append('<div class="text-end"><a href="'+edit_url+'" class="text-primary pe-2 ps-2">Edit</a>')
                    # if qs_instance.datamode == "A":
                    #     data.append('<div class="text-success">'+qs_instance.get_datamode_display()+'</div>')
                    #     data.append('<div class="text-end"><a href="'+edit_url+'" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void()" class="text-danger ps-2" onclick="delete_object('+str(qs_data['id'])+')">Inactivate</a></div>')
                    # else:
                    #     data.append('<div class="text-danger">'+qs_instance.get_datamode_display()+'</div>')
                    #     data.append('<div class="text-end"><a href="'+edit_url+'" class="text-primary pe-2 ps-2">Edit</a> | <a href="javascript:void()" class="text-success ps-2" onclick="delete_object('+str(qs_data['id'])+')">Activate</a></div>')
                else:
                    if isinstance(qs_data.get(column['column_name']), PhoneNumber):
                        data.append(qs_data.get(column['column_name']).national_number)
                    elif isinstance(qs_data.get(column['column_name']), models.ImageField):
                        pass
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
        else:
            obj = Category()
            obj.created_by = accountuser.id
            
        obj.name = pDict.get('name')
        obj.slug = pDict.get('slug')
        obj.description = pDict.get('description')
        obj.sort_order = pDict.get('sort_order', 0)

        obj.is_featured = True if pDict.get(
            'is_featured'
        ) else False

        obj.show_on_homepage = True if pDict.get(
            'show_on_homepage'
        ) else False

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
            if obj.datamode == "I":
                obj.datamode = "A"
            else:
                obj.datamode = "I"
            obj.save()

        result = True
        message = 'Sucesss'
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, message


# ─────────────────────────────────────────────────────────────────────────────
# ADD THESE FUNCTIONS to your existing api.py
# ─────────────────────────────────────────────────────────────────────────────


# ══════════════════════════════════════════════════════════════════════════════
# HomePageVideo
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
                    data.append(
                        '<div class="text-success">' + qs_instance.get_datamode_display() + '</div>'
                    )
                    data.append(
                        '<div class="text-end">'
                        '<a href="' + edit_url + '" class="text-primary pe-2 ps-2">Edit</a>'
                        '</div>'
                    )
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
        else:
            obj = HomePageVideo()
            obj.created_by = accountuser.id

        obj.title      = pDict.get('title')
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
# HeroBanner
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
                    data.append(
                        '<div class="text-success">' + qs_instance.get_datamode_display() + '</div>'
                    )
                    data.append(
                        '<div class="text-end">'
                        '<a href="' + edit_url + '" class="text-primary pe-2 ps-2">Edit</a>'
                        '</div>'
                    )
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
        else:
            obj = HeroBanner()
            obj.created_by = accountuser.id

        obj.title      = pDict.get('title', '')
        obj.sort_order = pDict.get('sort_order') or 1
        obj.is_active  = True if pDict.get('is_active') else False

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

# ─────────────────────────────────────────────────────────────────────────────
# ADD THESE FUNCTIONS to your existing api.py
# ─────────────────────────────────────────────────────────────────────────────


# ══════════════════════════════════════════════════════════════════════════════
# CUSTOMER
# ══════════════════════════════════════════════════════════════════════════════

@app_logger.functionlogs(log=log_name)
def customer_load_data(request, table_data):
    result, fResult = False, list()
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
                    data.append('<div class="text-success">' + qs_instance.get_datamode_display() + '</div>')
                    data.append('<div class="text-end"><a href="' + edit_url + '" class="text-primary pe-2 ps-2">Edit</a></div>')
                else:
                    value = qs_data.get(column['column_name'], '-')
                    if isinstance(value, Decimal): value = float(value)
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
    result, data = False, {}
    try:
        obj = Customer.objects.filter(id=id).first()
        if obj: data['customer'] = obj
        result, msg = True, 'Success'
    except Exception as e:
        result, msg = False, 'Internal Server Error'
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data

@app_logger.functionlogs(log=log_name)
def customer_create_update(request, id=None, mode=None):
    result, data = False, {}
    try:
        accountuser = auth_api.get_request_accountuser(request)
        p = request.POST
        obj = Customer.objects.filter(id=id).first() if (mode == 'edit' and id) else Customer()
        if not (mode == 'edit' and id): obj.created_by = accountuser.id
        obj.first_name    = p.get('first_name')
        obj.last_name     = p.get('last_name')
        obj.email         = p.get('email')
        obj.phone         = p.get('phone')
        obj.gender        = p.get('gender')
        obj.date_of_birth = p.get('date_of_birth') or None
        obj.is_verified   = True if p.get('is_verified') else False
        obj.is_subscribed = True if p.get('is_subscribed') else False
        if request.FILES.get('profile_image'):
            obj.profile_image = request.FILES.get('profile_image')
        obj.updated_by = accountuser.id
        obj.save()
        data['customer'] = obj
        result, msg = True, 'Success'
    except Exception as e:
        result, msg = False, 'Internal Server Error'
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data

@app_logger.functionlogs(log=log_name)
def customer_update_status(request, id):
    result, message = False, 'Error'
    try:
        accountuser = auth_api.get_request_accountuser(request)
        obj = Customer.objects.filter(id=id).first()
        if obj:
            obj.updated_by = accountuser.id
            obj.datamode = 'A' if obj.datamode == 'I' else 'I'
            obj.save()
        result, message = True, 'Success'
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, message


# ══════════════════════════════════════════════════════════════════════════════
# ADDRESS
# ══════════════════════════════════════════════════════════════════════════════
# Updated address functions with user instead of customer

@app_logger.functionlogs(log=log_name)
def address_load_data(request, table_data):
    result, fResult = False, list()
    try:
        # Change: Use user instead of customer, and exclude 'D' datamode
        queryset = Address.objects.exclude(datamode='D').order_by('-updated_on')
        qs, total_records, total_display_records = app_utils.method_for_datatable_operations(request, queryset)
        final_data = []
        for qs_instance in qs:
            qs_data = model_to_dict(qs_instance)
            data = []
            edit_url = reverse('mck_website:mck_address_update', args=[qs_data['id']])
            for column in table_data['columns']:
                if column['column_name'] == 'datamode':
                    data.append('<div class="text-success">' + qs_instance.get_datamode_display() + '</div>')
                    data.append('<div class="text-end"><a href="' + edit_url + '" class="text-primary pe-2 ps-2">Edit</a></div>')
                elif column['column_name'] == 'user':
                    # Display user information instead of customer
                    user_info = f"{qs_instance.user.first_name} {qs_instance.user.last_name}" if qs_instance.user else '-'
                    data.append(user_info)
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
def address_retrieve_data(request, id):
    result, data = False, {}
    try:
        obj = Address.objects.filter(id=id).first()
        if obj:
            data['address'] = obj
            # Also return user info if needed
            if obj.user:
                data['user_name'] = f"{obj.user.first_name} {obj.user.last_name}"
                data['user_email'] = obj.user.email
        result, msg = True, 'Success'
    except Exception as e:
        result, msg = False, 'Internal Server Error'
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def address_create_update(request, id=None, mode=None):
    result, data = False, {}
    try:
        accountuser = auth_api.get_request_accountuser(request)
        p = request.POST
        
        # Get or create address object
        obj = Address.objects.filter(id=id).first() if (mode == 'edit' and id) else Address()
        
        if not (mode == 'edit' and id):
            obj.created_by = accountuser.id
        
        # IMPORTANT: Change from customer_id to user_id
        # Get user_id from POST or use the logged-in user
        user_id = p.get('user') or p.get('user_id')
        if user_id:
            obj.user_id = user_id
        elif accountuser:
            # If no user specified, use the logged-in user
            obj.user = accountuser
        
        obj.address_type   = p.get('address_type')
        obj.full_name      = p.get('full_name')
        obj.phone          = p.get('phone')
        obj.address_line1  = p.get('address_line1')
        obj.address_line2  = p.get('address_line2', '')
        obj.city           = p.get('city')
        obj.state          = p.get('state')
        obj.pincode        = p.get('pincode')
        obj.country        = p.get('country', 'India')
        obj.is_default     = True if p.get('is_default') else False
        obj.updated_by     = accountuser.id
        
        # If this is set as default, unset other default addresses for this user
        if obj.is_default and obj.user:
            Address.objects.filter(user=obj.user, is_default=True).exclude(id=obj.id).update(is_default=False)
        
        obj.save()
        
        data['address'] = obj
        result, msg = True, 'Success'
        
    except Exception as e:
        result, msg = False, 'Internal Server Error'
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def address_update_status(request, id):
    result, message = False, 'Error'
    try:
        accountuser = auth_api.get_request_accountuser(request)
        obj = Address.objects.filter(id=id).first()
        if obj:
            obj.updated_by = accountuser.id
            obj.datamode = 'A' if obj.datamode == 'I' else 'I'
            obj.save()
        result, message = True, 'Success'
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, message



# ══════════════════════════════════════════════════════════════════════════════
# COUPON
# ══════════════════════════════════════════════════════════════════════════════

@app_logger.functionlogs(log=log_name)
def coupon_load_data(request, table_data):
    result, fResult = False, list()
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
                    data.append('<div class="text-success">' + qs_instance.get_datamode_display() + '</div>')
                    data.append('<div class="text-end"><a href="' + edit_url + '" class="text-primary pe-2 ps-2">Edit</a></div>')
                else:
                    value = qs_data.get(column['column_name'], '-')
                    if isinstance(value, Decimal): value = float(value)
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
def coupon_retrieve_data(request, id):
    result, data = False, {}
    try:
        obj = Coupon.objects.filter(id=id).first()
        if obj: data['coupon'] = obj
        result, msg = True, 'Success'
    except Exception as e:
        result, msg = False, 'Internal Server Error'
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data

@app_logger.functionlogs(log=log_name)
def coupon_create_update(request, id=None, mode=None):
    result, data = False, {}
    try:
        accountuser = auth_api.get_request_accountuser(request)
        p = request.POST
        obj = Coupon.objects.filter(id=id).first() if (mode == 'edit' and id) else Coupon()
        if not (mode == 'edit' and id): obj.created_by = accountuser.id
        obj.code                    = p.get('code')
        obj.description             = p.get('description', '')
        obj.discount_type           = p.get('discount_type')
        obj.discount_value          = p.get('discount_value') or 0
        obj.minimum_order_amount    = p.get('minimum_order_amount') or 0
        obj.maximum_discount_amount = p.get('maximum_discount_amount') or None
        obj.usage_limit             = p.get('usage_limit') or None
        obj.per_user_limit          = p.get('per_user_limit') or 1
        obj.valid_from              = p.get('valid_from')
        obj.valid_until             = p.get('valid_until')
        obj.is_active               = True if p.get('is_active') else False
        obj.updated_by              = accountuser.id
        obj.save()
        data['coupon'] = obj
        result, msg = True, 'Success'
    except Exception as e:
        result, msg = False, 'Internal Server Error'
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data

@app_logger.functionlogs(log=log_name)
def coupon_update_status(request, id):
    result, message = False, 'Error'
    try:
        accountuser = auth_api.get_request_accountuser(request)
        obj = Coupon.objects.filter(id=id).first()
        if obj:
            obj.updated_by = accountuser.id
            obj.datamode = 'A' if obj.datamode == 'I' else 'I'
            obj.save()
        result, message = True, 'Success'
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, message


# ══════════════════════════════════════════════════════════════════════════════
# PAYMENT GATEWAY
# ══════════════════════════════════════════════════════════════════════════════

@app_logger.functionlogs(log=log_name)
def payment_gateway_load_data(request, table_data):
    result, fResult = False, list()
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
                    data.append('<div class="text-success">' + qs_instance.get_datamode_display() + '</div>')
                    data.append('<div class="text-end"><a href="' + edit_url + '" class="text-primary pe-2 ps-2">Edit</a></div>')
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
def payment_gateway_retrieve_data(request, id):
    result, data = False, {}
    try:
        obj = PaymentGateway.objects.filter(id=id).first()
        if obj: data['payment_gateway'] = obj
        result, msg = True, 'Success'
    except Exception as e:
        result, msg = False, 'Internal Server Error'
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data

@app_logger.functionlogs(log=log_name)
def payment_gateway_create_update(request, id=None, mode=None):
    result, data = False, {}
    try:
        accountuser = auth_api.get_request_accountuser(request)
        p = request.POST
        obj = PaymentGateway.objects.filter(id=id).first() if (mode == 'edit' and id) else PaymentGateway()
        if not (mode == 'edit' and id): obj.created_by = accountuser.id
        obj.name        = p.get('name')
        obj.code        = p.get('code')
        obj.description = p.get('description', '')
        obj.is_active   = True if p.get('is_active') else False
        obj.sort_order  = p.get('sort_order') or 1
        obj.config_json = p.get('config_json', '')
        if request.FILES.get('logo'):
            obj.logo = request.FILES.get('logo')
        obj.updated_by = accountuser.id
        obj.save()
        data['payment_gateway'] = obj
        result, msg = True, 'Success'
    except Exception as e:
        result, msg = False, 'Internal Server Error'
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data

@app_logger.functionlogs(log=log_name)
def payment_gateway_update_status(request, id):
    result, message = False, 'Error'
    try:
        accountuser = auth_api.get_request_accountuser(request)
        obj = PaymentGateway.objects.filter(id=id).first()
        if obj:
            obj.updated_by = accountuser.id
            obj.datamode = 'A' if obj.datamode == 'I' else 'I'
            obj.save()
        result, message = True, 'Success'
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, message


# ══════════════════════════════════════════════════════════════════════════════
# CART
# ══════════════════════════════════════════════════════════════════════════════
@app_logger.functionlogs(log=log_name)
def cart_load_data(request, table_data):
    result, fResult = False, list()
    try:
        queryset = Cart.objects.exclude(datamode='D').order_by('-updated_on')
        qs, total_records, total_display_records = app_utils.method_for_datatable_operations(request, queryset)
        final_data = []
        for qs_instance in qs:
            qs_data = model_to_dict(qs_instance)
            data = []
            # FIXED: Check if edit_url exists and is valid
            try:
                edit_url = reverse('mck_website:mck_cart_list', args=[qs_data['id']])
            except NoReverseMatch:
                edit_url = '#'
            
            for column in table_data['columns']:
                if column['column_name'] == 'datamode':
                    data.append('<div class="text-success">' + qs_instance.get_datamode_display() + '</div>')
                    data.append('<div class="text-end"><a href="' + edit_url + '" class="text-primary pe-2 ps-2">Edit</a></div>')
                elif column['column_name'] == 'user':  # CHANGED from 'customer' to 'user'
                    # Handle user display properly
                    if qs_instance.user:
                        user_display = str(qs_instance.user)
                        # If you want to show email or username
                        if hasattr(qs_instance.user, 'get_full_name'):
                            full_name = qs_instance.user.get_full_name()
                            if full_name:
                                user_display = f"{full_name} ({qs_instance.user.email})"
                        data.append(user_display)
                    else:
                        # Check if there's a session_key for anonymous users
                        session_info = qs_instance.session_key if qs_instance.session_key else 'Anonymous'
                        data.append(f'Guest ({session_info[:8]}...)')  # Show first 8 chars of session
                elif column['column_name'] == 'coupon':
                    data.append(str(qs_instance.coupon) if qs_instance.coupon else '-')
                elif column['column_name'] == 'session_key':
                    # Handle session key display
                    session_val = qs_instance.session_key
                    if session_val:
                        data.append(session_val[:20] + '...' if len(session_val) > 20 else session_val)
                    else:
                        data.append('-')
                else:
                    value = qs_data.get(column['column_name'], '-')
                    data.append(str(value) if value is not None else '-')
            final_data.append(data)
        fResult = app_utils.final_dict(request, total_records, total_display_records, final_data)
        result, msg = True, 'Success'
    except Exception as e:
        result, msg = False, 'Internal Server Error'
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s - %s' % (exc_traceback.tb_lineno, type(e).__name__, str(e)))
        logger.error(f"Full error: {e}", exc_info=True)
    return result, msg, fResult

@app_logger.functionlogs(log=log_name)
def cart_retrieve_data(request, id):
    result, data = False, {}
    try:
        obj = Cart.objects.filter(id=id).first()
        if obj: 
            data['cart'] = obj
            # Include user info in response
            data['user_id'] = obj.user.id if obj.user else None
            data['username'] = str(obj.user) if obj.user else 'Anonymous'
        result, msg = True, 'Success'
    except Exception as e:
        result, msg = False, 'Internal Server Error'
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data

@app_logger.functionlogs(log=log_name)
def cart_create_update(request, id=None, mode=None):
    result, data = False, {}
    try:
        accountuser = auth_api.get_request_accountuser(request)
        p = request.POST
        
        # Get or create cart object
        obj = Cart.objects.filter(id=id).first() if (mode == 'edit' and id) else Cart()
        
        if not (mode == 'edit' and id):
            obj.created_by = accountuser.id
        
        # THE FIX: Always attach the Django auth user
        if request.user.is_authenticated:
            obj.user = request.user  # Changed from customer_id to user
        
        # Handle session for non-authenticated users
        if not request.user.is_authenticated:
            obj.session_key = p.get('session_key', request.session.session_key or '')
        
        obj.coupon_id = p.get('coupon') or None
        obj.updated_by = accountuser.id
        obj.save()
        
        data['cart'] = obj
        data['user_assigned'] = bool(obj.user)
        result, msg = True, 'Success'
        
    except Exception as e:
        result, msg = False, 'Internal Server Error'
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data

@app_logger.functionlogs(log=log_name)
def cart_update_status(request, id):
    result, message = False, 'Error'
    try:
        accountuser = auth_api.get_request_accountuser(request)
        obj = Cart.objects.filter(id=id).first()
        if obj:
            obj.updated_by = accountuser.id
            obj.datamode = 'A' if obj.datamode == 'I' else 'I'
            obj.save()
        result, message = True, 'Success'
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, message

# ══════════════════════════════════════════════════════════════════════════════
# CART ITEM
# ══════════════════════════════════════════════════════════════════════════════

@app_logger.functionlogs(log=log_name)
def cart_item_load_data(request, table_data):
    result, fResult = False, list()
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
                    data.append('<div class="text-success">' + qs_instance.get_datamode_display() + '</div>')
                    data.append('<div class="text-end"><a href="' + edit_url + '" class="text-primary pe-2 ps-2">Edit</a></div>')
                elif column['column_name'] == 'product':
                    data.append(str(qs_instance.product))
                elif column['column_name'] == 'cart':
                    data.append(str(qs_instance.cart))
                else:
                    value = qs_data.get(column['column_name'], '-')
                    if isinstance(value, Decimal): value = float(value)
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
def cart_item_retrieve_data(request, id):
    result, data = False, {}
    try:
        obj = CartItem.objects.filter(id=id).first()
        if obj: data['cart_item'] = obj
        result, msg = True, 'Success'
    except Exception as e:
        result, msg = False, 'Internal Server Error'
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data

@app_logger.functionlogs(log=log_name)
def cart_item_create_update(request, id=None, mode=None):
    result, data = False, {}
    try:
        accountuser = auth_api.get_request_accountuser(request)
        p = request.POST
        obj = CartItem.objects.filter(id=id).first() if (mode == 'edit' and id) else CartItem()
        if not (mode == 'edit' and id): obj.created_by = accountuser.id
        obj.cart_id    = p.get('cart')
        obj.product_id = p.get('product')
        obj.quantity   = p.get('quantity') or 1
        obj.price      = p.get('price') or 0
        obj.updated_by = accountuser.id
        obj.save()
        data['cart_item'] = obj
        result, msg = True, 'Success'
    except Exception as e:
        result, msg = False, 'Internal Server Error'
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data

@app_logger.functionlogs(log=log_name)
def cart_item_update_status(request, id):
    result, message = False, 'Error'
    try:
        accountuser = auth_api.get_request_accountuser(request)
        obj = CartItem.objects.filter(id=id).first()
        if obj:
            obj.updated_by = accountuser.id
            obj.datamode = 'A' if obj.datamode == 'I' else 'I'
            obj.save()
        result, message = True, 'Success'
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, message


# ══════════════════════════════════════════════════════════════════════════════
# WISHLIST
# ══════════════════════════════════════════════════════════════════════════════

@app_logger.functionlogs(log=log_name)
def wishlist_load_data(request, table_data):
    result, fResult = False, list()
    try:
        queryset = Wishlist.objects.exclude(datamode='D').order_by('-updated_on')
        qs, total_records, total_display_records = app_utils.method_for_datatable_operations(request, queryset)
        final_data = []
        for qs_instance in qs:
            qs_data = model_to_dict(qs_instance)
            data = []
            edit_url = reverse('mck_website:mck_wishlist_update', args=[qs_data['id']])
            for column in table_data['columns']:
                if column['column_name'] == 'datamode':
                    data.append('<div class="text-success">' + qs_instance.get_datamode_display() + '</div>')
                    data.append('<div class="text-end"><a href="' + edit_url + '" class="text-primary pe-2 ps-2">Edit</a></div>')
                elif column['column_name'] == 'customer':
                    data.append(str(qs_instance.customer))
                elif column['column_name'] == 'product':
                    data.append(str(qs_instance.product))
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
def wishlist_retrieve_data(request, id):
    result, data = False, {}
    try:
        obj = Wishlist.objects.filter(id=id).first()
        if obj: data['wishlist'] = obj
        result, msg = True, 'Success'
    except Exception as e:
        result, msg = False, 'Internal Server Error'
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data

@app_logger.functionlogs(log=log_name)
def wishlist_create_update(request, id=None, mode=None):
    result, data = False, {}
    try:
        accountuser = auth_api.get_request_accountuser(request)
        p = request.POST
        obj = Wishlist.objects.filter(id=id).first() if (mode == 'edit' and id) else Wishlist()
        if not (mode == 'edit' and id): obj.created_by = accountuser.id
        obj.customer_id = p.get('customer')
        obj.product_id  = p.get('product')
        obj.updated_by  = accountuser.id
        obj.save()
        data['wishlist'] = obj
        result, msg = True, 'Success'
    except Exception as e:
        result, msg = False, 'Internal Server Error'
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data

@app_logger.functionlogs(log=log_name)
def wishlist_update_status(request, id):
    result, message = False, 'Error'
    try:
        accountuser = auth_api.get_request_accountuser(request)
        obj = Wishlist.objects.filter(id=id).first()
        if obj:
            obj.updated_by = accountuser.id
            obj.datamode = 'A' if obj.datamode == 'I' else 'I'
            obj.save()
        result, message = True, 'Success'
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, message


# ══════════════════════════════════════════════════════════════════════════════
# ORDER
# ══════════════════════════════════════════════════════════════════════════════
@app_logger.functionlogs(log=log_name)
def order_load_data(request, table_data):
    result, fResult = False, list()
    try:
        queryset = Order.objects.exclude(datamode='D').order_by('-updated_on')
        qs, total_records, total_display_records = app_utils.method_for_datatable_operations(request, queryset)
        final_data = []
        
        # Import NoReverseMatch at the top of your file
        from django.urls import NoReverseMatch
        
        for qs_instance in qs:
            qs_data = model_to_dict(qs_instance)
            data = []
            
            # Safe edit URL generation
            edit_url = '#'
            try:
                edit_url = reverse('mck_website:mck_order_update', args=[qs_data['id']])
            except NoReverseMatch:
                edit_url = f"/admin/order/{qs_data['id']}/edit/"
            
            for column in table_data['columns']:
                column_name = column['column_name']
                
                if column_name == 'datamode':
                    data.append('<div class="text-success">' + qs_instance.get_datamode_display() + '</div>')
                    data.append('<div class="text-end"><a href="' + edit_url + '" class="text-primary pe-2 ps-2">Edit</a></div>')
                
                elif column_name == 'user':  # CHANGED from 'customer' to 'user'
                    if qs_instance.user:
                        # Display user info (email or username)
                        user_display = qs_instance.user.email if hasattr(qs_instance.user, 'email') else str(qs_instance.user)
                        if hasattr(qs_instance.user, 'get_full_name'):
                            full_name = qs_instance.user.get_full_name()
                            if full_name:
                                user_display = f"{full_name} ({user_display})"
                        data.append(user_display)
                    else:
                        data.append('Guest')
                
                elif column_name == 'customer':  # Handle if 'customer' still in table_data
                    # Map to user field
                    if qs_instance.user:
                        data.append(str(qs_instance.user))
                    else:
                        data.append('-')
                
                else:
                    value = qs_data.get(column_name, '-')
                    if isinstance(value, Decimal): 
                        value = float(value)
                    data.append(str(value) if value is not None else '-')
            
            final_data.append(data)
        
        fResult = app_utils.final_dict(request, total_records, total_display_records, final_data)
        result, msg = True, 'Success'
        
    except Exception as e:
        result, msg = False, 'Internal Server Error'
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s - %s' % (exc_traceback.tb_lineno, type(e).__name__, str(e)))
        logger.error(f"Full error: {e}", exc_info=True)
    
    return result, msg, fResult


@app_logger.functionlogs(log=log_name)
def order_retrieve_data(request, id):
    result, data = False, {}
    try:
        obj = Order.objects.filter(id=id).first()
        if obj: 
            data['order'] = obj
            # Include user info in response
            if obj.user:
                data['user_id'] = obj.user.id
                data['user_email'] = obj.user.email if hasattr(obj.user, 'email') else str(obj.user)
            else:
                data['user_id'] = None
                data['user_email'] = 'Guest'
        result, msg = True, 'Success'
    except Exception as e:
        result, msg = False, 'Internal Server Error'
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s - %s' % (exc_traceback.tb_lineno, type(e).__name__, str(e)))
        logger.error(f"Full error: {e}", exc_info=True)
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def order_create_update(request, id=None, mode=None):
    result, data = False, {}
    try:
        accountuser = auth_api.get_request_accountuser(request)
        p = request.POST
        
        # Get or create order object
        obj = Order.objects.filter(id=id).first() if (mode == 'edit' and id) else Order()
        
        if not (mode == 'edit' and id): 
            obj.created_by = accountuser.id if accountuser else 'system'
        
        # THE FIX: Use 'user' instead of 'customer_id'
        if request.user and request.user.is_authenticated:
            obj.user = request.user  # Changed from customer_id to user
        else:
            # For guest checkout, you might still want to capture email/name
            guest_email = p.get('guest_email')
            if guest_email:
                # Store guest email in a separate field or create temporary user
                # For now, just store as note or create a session-based identifier
                obj.notes = f"Guest Checkout - Email: {guest_email}\n" + (obj.notes or '')
        
        # Order fields
        obj.order_number = p.get('order_number')
        obj.status = p.get('status', 'pending')
        obj.coupon_id = p.get('coupon') or None
        
        # Shipping information
        obj.shipping_full_name = p.get('shipping_full_name')
        obj.shipping_phone = p.get('shipping_phone')
        obj.shipping_address_line1 = p.get('shipping_address_line1')
        obj.shipping_address_line2 = p.get('shipping_address_line2', '')
        obj.shipping_city = p.get('shipping_city')
        obj.shipping_state = p.get('shipping_state')
        obj.shipping_pincode = p.get('shipping_pincode')
        obj.shipping_country = p.get('shipping_country', 'India')
        
        # Amount fields
        obj.subtotal = p.get('subtotal') or 0
        obj.discount_amount = p.get('discount_amount') or 0
        obj.shipping_charge = p.get('shipping_charge') or 0
        obj.tax_amount = p.get('tax_amount') or 0
        obj.total_amount = p.get('total_amount') or 0
        
        # Additional fields
        obj.notes = p.get('notes', '')
        obj.delivered_on = p.get('delivered_on') or None
        
        obj.updated_by = accountuser.id if accountuser else 'system'
        obj.save()
        
        data['order'] = obj
        data['user_assigned'] = bool(obj.user)
        result, msg = True, 'Success'
        
    except Exception as e:
        result, msg = False, 'Internal Server Error'
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s - %s' % (exc_traceback.tb_lineno, type(e).__name__, str(e)))
        logger.error(f"Full error: {e}", exc_info=True)
    
    return result, msg, data


@app_logger.functionlogs(log=log_name)
def order_update_status(request, id):
    result, message = False, 'Error'
    try:
        accountuser = auth_api.get_request_accountuser(request)
        obj = Order.objects.filter(id=id).first()
        if obj:
            obj.updated_by = accountuser.id if accountuser else 'system'
            obj.datamode = 'A' if obj.datamode == 'I' else 'I'
            obj.save()
        result, message = True, 'Success'
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s - %s' % (exc_traceback.tb_lineno, type(e).__name__, str(e)))
        logger.error(f"Full error: {e}", exc_info=True)
    return result, message

# ══════════════════════════════════════════════════════════════════════════════
# ORDER ITEM
# ══════════════════════════════════════════════════════════════════════════════

@app_logger.functionlogs(log=log_name)
def order_item_load_data(request, table_data):
    result, fResult = False, list()
    try:
        queryset = OrderItem.objects.exclude(datamode='D').order_by('-updated_on')
        qs, total_records, total_display_records = app_utils.method_for_datatable_operations(request, queryset)
        final_data = []
        for qs_instance in qs:
            qs_data = model_to_dict(qs_instance)
            data = []
            edit_url = reverse('mck_website:mck_order_item_update', args=[qs_data['id']])
            for column in table_data['columns']:
                if column['column_name'] == 'datamode':
                    data.append('<div class="text-success">' + qs_instance.get_datamode_display() + '</div>')
                    data.append('<div class="text-end"><a href="' + edit_url + '" class="text-primary pe-2 ps-2">Edit</a></div>')
                elif column['column_name'] == 'order':
                    data.append(str(qs_instance.order))
                else:
                    value = qs_data.get(column['column_name'], '-')
                    if isinstance(value, Decimal): value = float(value)
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
def order_item_retrieve_data(request, id):
    result, data = False, {}
    try:
        obj = OrderItem.objects.filter(id=id).first()
        if obj: data['order_item'] = obj
        result, msg = True, 'Success'
    except Exception as e:
        result, msg = False, 'Internal Server Error'
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data

@app_logger.functionlogs(log=log_name)
def order_item_create_update(request, id=None, mode=None):
    result, data = False, {}
    try:
        accountuser = auth_api.get_request_accountuser(request)
        p = request.POST
        obj = OrderItem.objects.filter(id=id).first() if (mode == 'edit' and id) else OrderItem()
        if not (mode == 'edit' and id): obj.created_by = accountuser.id
        obj.order_id      = p.get('order')
        obj.product_id    = p.get('product') or None
        obj.product_name  = p.get('product_name')
        obj.product_sku   = p.get('product_sku')
        obj.product_image = p.get('product_image', '')
        obj.unit_price    = p.get('unit_price') or 0
        obj.quantity      = p.get('quantity') or 1
        obj.total_price   = p.get('total_price') or 0
        obj.updated_by    = accountuser.id
        obj.save()
        data['order_item'] = obj
        result, msg = True, 'Success'
    except Exception as e:
        result, msg = False, 'Internal Server Error'
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data

@app_logger.functionlogs(log=log_name)
def order_item_update_status(request, id):
    result, message = False, 'Error'
    try:
        accountuser = auth_api.get_request_accountuser(request)
        obj = OrderItem.objects.filter(id=id).first()
        if obj:
            obj.updated_by = accountuser.id
            obj.datamode = 'A' if obj.datamode == 'I' else 'I'
            obj.save()
        result, message = True, 'Success'
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, message


# ══════════════════════════════════════════════════════════════════════════════
# PAYMENT
# ══════════════════════════════════════════════════════════════════════════════

@app_logger.functionlogs(log=log_name)
def payment_load_data(request, table_data):
    result, fResult = False, list()
    try:
        queryset = Payment.objects.exclude(datamode='D').order_by('-updated_on')
        qs, total_records, total_display_records = app_utils.method_for_datatable_operations(request, queryset)
        final_data = []
        for qs_instance in qs:
            qs_data = model_to_dict(qs_instance)
            data = []
            edit_url = reverse('mck_website:mck_payment_update', args=[qs_data['id']])
            for column in table_data['columns']:
                if column['column_name'] == 'datamode':
                    data.append('<div class="text-success">' + qs_instance.get_datamode_display() + '</div>')
                    data.append('<div class="text-end"><a href="' + edit_url + '" class="text-primary pe-2 ps-2">Edit</a></div>')
                elif column['column_name'] == 'order':
                    data.append(str(qs_instance.order))
                elif column['column_name'] == 'payment_gateway':
                    data.append(str(qs_instance.payment_gateway) if qs_instance.payment_gateway else '-')
                else:
                    value = qs_data.get(column['column_name'], '-')
                    if isinstance(value, Decimal): value = float(value)
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
def payment_retrieve_data(request, id):
    result, data = False, {}
    try:
        obj = Payment.objects.filter(id=id).first()
        if obj: data['payment'] = obj
        result, msg = True, 'Success'
    except Exception as e:
        result, msg = False, 'Internal Server Error'
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data

@app_logger.functionlogs(log=log_name)
def payment_create_update(request, id=None, mode=None):
    result, data = False, {}
    try:
        accountuser = auth_api.get_request_accountuser(request)
        p = request.POST
        obj = Payment.objects.filter(id=id).first() if (mode == 'edit' and id) else Payment()
        if not (mode == 'edit' and id): obj.created_by = accountuser.id
        obj.order_id           = p.get('order')
        obj.payment_gateway_id = p.get('payment_gateway') or None
        obj.transaction_id     = p.get('transaction_id')
        obj.gateway_order_id   = p.get('gateway_order_id', '')
        obj.amount             = p.get('amount') or 0
        obj.currency           = p.get('currency', 'INR')
        obj.status             = p.get('status', 'pending')
        obj.gateway_response   = p.get('gateway_response', '')
        obj.paid_on            = p.get('paid_on') or None
        obj.updated_by         = accountuser.id
        obj.save()
        data['payment'] = obj
        result, msg = True, 'Success'
    except Exception as e:
        result, msg = False, 'Internal Server Error'
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data

@app_logger.functionlogs(log=log_name)
def payment_update_status(request, id):
    result, message = False, 'Error'
    try:
        accountuser = auth_api.get_request_accountuser(request)
        obj = Payment.objects.filter(id=id).first()
        if obj:
            obj.updated_by = accountuser.id
            obj.datamode = 'A' if obj.datamode == 'I' else 'I'
            obj.save()
        result, message = True, 'Success'
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, message


# ══════════════════════════════════════════════════════════════════════════════
# PRODUCT REVIEW
# ══════════════════════════════════════════════════════════════════════════════

@app_logger.functionlogs(log=log_name)
def product_review_load_data(request, table_data):
    result, fResult = False, list()
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
                    data.append('<div class="text-success">' + qs_instance.get_datamode_display() + '</div>')
                    data.append('<div class="text-end"><a href="' + edit_url + '" class="text-primary pe-2 ps-2">Edit</a></div>')
                elif column['column_name'] == 'product':
                    data.append(str(qs_instance.product))
                elif column['column_name'] == 'customer':
                    data.append(str(qs_instance.customer) if qs_instance.customer else '-')
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
def product_review_retrieve_data(request, id):
    result, data = False, {}
    try:
        obj = ProductReview.objects.filter(id=id).first()
        if obj: data['product_review'] = obj
        result, msg = True, 'Success'
    except Exception as e:
        result, msg = False, 'Internal Server Error'
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data

@app_logger.functionlogs(log=log_name)
def product_review_create_update(request, id=None, mode=None):
    result, data = False, {}
    try:
        accountuser = auth_api.get_request_accountuser(request)
        p = request.POST
        obj = ProductReview.objects.filter(id=id).first() if (mode == 'edit' and id) else ProductReview()
        if not (mode == 'edit' and id): obj.created_by = accountuser.id
        obj.product_id    = p.get('product')
        obj.customer_id   = p.get('customer') or None
        obj.order_item_id = p.get('order_item') or None
        obj.rating        = p.get('rating') or 1
        obj.title         = p.get('title', '')
        obj.body          = p.get('body')
        obj.is_approved   = True if p.get('is_approved') else False
        obj.updated_by    = accountuser.id
        obj.save()
        data['product_review'] = obj
        result, msg = True, 'Success'
    except Exception as e:
        result, msg = False, 'Internal Server Error'
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data

@app_logger.functionlogs(log=log_name)
def product_review_update_status(request, id):
    result, message = False, 'Error'
    try:
        accountuser = auth_api.get_request_accountuser(request)
        obj = ProductReview.objects.filter(id=id).first()
        if obj:
            obj.updated_by = accountuser.id
            obj.datamode = 'A' if obj.datamode == 'I' else 'I'
            obj.save()
        result, message = True, 'Success'
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, message


# ══════════════════════════════════════════════════════════════════════════════
# NEWSLETTER
# ══════════════════════════════════════════════════════════════════════════════

@app_logger.functionlogs(log=log_name)
def newsletter_load_data(request, table_data):
    result, fResult = False, list()
    try:
        queryset = Newsletter.objects.exclude(datamode='D').order_by('-updated_on')
        qs, total_records, total_display_records = app_utils.method_for_datatable_operations(request, queryset)
        final_data = []
        for qs_instance in qs:
            qs_data = model_to_dict(qs_instance)
            data = []
            edit_url = reverse('mck_website:mck_newsletter_update', args=[qs_data['id']])
            for column in table_data['columns']:
                if column['column_name'] == 'datamode':
                    data.append('<div class="text-success">' + qs_instance.get_datamode_display() + '</div>')
                    data.append('<div class="text-end"><a href="' + edit_url + '" class="text-primary pe-2 ps-2">Edit</a></div>')
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
def newsletter_retrieve_data(request, id):
    result, data = False, {}
    try:
        obj = Newsletter.objects.filter(id=id).first()
        if obj: data['newsletter'] = obj
        result, msg = True, 'Success'
    except Exception as e:
        result, msg = False, 'Internal Server Error'
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data

@app_logger.functionlogs(log=log_name)
def newsletter_create_update(request, id=None, mode=None):
    result, data = False, {}
    try:
        accountuser = auth_api.get_request_accountuser(request)
        p = request.POST
        obj = Newsletter.objects.filter(id=id).first() if (mode == 'edit' and id) else Newsletter()
        if not (mode == 'edit' and id): obj.created_by = accountuser.id
        obj.email     = p.get('email')
        obj.is_active = True if p.get('is_active') else False
        obj.updated_by = accountuser.id
        obj.save()
        data['newsletter'] = obj
        result, msg = True, 'Success'
    except Exception as e:
        result, msg = False, 'Internal Server Error'
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data

@app_logger.functionlogs(log=log_name)
def newsletter_update_status(request, id):
    result, message = False, 'Error'
    try:
        accountuser = auth_api.get_request_accountuser(request)
        obj = Newsletter.objects.filter(id=id).first()
        if obj:
            obj.updated_by = accountuser.id
            obj.datamode = 'A' if obj.datamode == 'I' else 'I'
            obj.save()
        result, message = True, 'Success'
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, message


# ══════════════════════════════════════════════════════════════════════════════
# CONTACT US
# ══════════════════════════════════════════════════════════════════════════════

@app_logger.functionlogs(log=log_name)
def contact_us_load_data(request, table_data):
    result, fResult = False, list()
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
                    data.append('<div class="text-success">' + qs_instance.get_datamode_display() + '</div>')
                    data.append('<div class="text-end"><a href="' + edit_url + '" class="text-primary pe-2 ps-2">Edit</a></div>')
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
def contact_us_retrieve_data(request, id):
    result, data = False, {}
    try:
        obj = Contact.objects.filter(id=id).first()
        if obj: data['contact_us'] = obj
        result, msg = True, 'Success'
    except Exception as e:
        result, msg = False, 'Internal Server Error'
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data

@app_logger.functionlogs(log=log_name)
def contact_us_create_update(request, id=None, mode=None):
    result, data = False, {}
    try:
        accountuser = auth_api.get_request_accountuser(request)
        p = request.POST
        obj = Contact.objects.filter(id=id).first() if (mode == 'edit' and id) else ContactUs()
        if not (mode == 'edit' and id): obj.created_by = accountuser.id
        obj.name        = p.get('name')
        obj.email       = p.get('email')
        obj.phone       = p.get('phone', '')
        obj.subject     = p.get('subject')
        obj.message     = p.get('message')
        obj.status      = p.get('status', 'new')
        obj.admin_notes = p.get('admin_notes', '')
        obj.replied_on  = p.get('replied_on') or None
        obj.updated_by  = accountuser.id
        obj.save()
        data['contact'] = obj
        result, msg = True, 'Success'
    except Exception as e:
        result, msg = False, 'Internal Server Error'
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data

@app_logger.functionlogs(log=log_name)
def contact_us_update_status(request, id):
    result, message = False, 'Error'
    try:
        accountuser = auth_api.get_request_accountuser(request)
        obj = Contact.objects.filter(id=id).first()
        if obj:
            obj.updated_by = accountuser.id
            obj.datamode = 'A' if obj.datamode == 'I' else 'I'
            obj.save()
        result, message = True, 'Success'
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, message


# ══════════════════════════════════════════════════════════════════════════════
# SITE SETTINGS  (singleton – no list/delete, just retrieve + update)
# ══════════════════════════════════════════════════════════════════════════════

@app_logger.functionlogs(log=log_name)
def site_settings_retrieve_data(request):
    result, data = False, {}
    try:
        obj = SiteSettings.load()
        data['site_settings'] = obj
        result, msg = True, 'Success'
    except Exception as e:
        result, msg = False, 'Internal Server Error'
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, data

@app_logger.functionlogs(log=log_name)
def site_settings_update(request):
    result, data = False, {}
    try:
        accountuser = auth_api.get_request_accountuser(request)
        p = request.POST
        obj = SiteSettings.load()
        obj.site_name           = p.get('site_name')
        obj.site_tagline        = p.get('site_tagline', '')
        obj.site_email          = p.get('site_email')
        obj.site_phone          = p.get('site_phone', '')
        obj.site_phone_alt      = p.get('site_phone_alt', '')
        obj.site_address        = p.get('site_address', '')
        obj.facebook_url        = p.get('facebook_url', '')
        obj.instagram_url       = p.get('instagram_url', '')
        obj.twitter_url         = p.get('twitter_url', '')
        obj.youtube_url         = p.get('youtube_url', '')
        obj.linkedin_url        = p.get('linkedin_url', '')
        obj.meta_title          = p.get('meta_title', '')
        obj.meta_description    = p.get('meta_description', '')
        obj.meta_keywords       = p.get('meta_keywords', '')
        obj.google_analytics_id = p.get('google_analytics_id', '')
        obj.privacy_policy      = p.get('privacy_policy', '')
        obj.terms_conditions    = p.get('terms_conditions', '')
        obj.return_policy       = p.get('return_policy', '')
        obj.shipping_policy     = p.get('shipping_policy', '')
        obj.currency_code       = p.get('currency_code', 'INR')
        obj.currency_symbol     = p.get('currency_symbol', '₹')
        obj.free_shipping_above = p.get('free_shipping_above') or 0
        obj.tax_percentage      = p.get('tax_percentage') or 0
        if request.FILES.get('site_logo'):
            obj.site_logo = request.FILES.get('site_logo')
        if request.FILES.get('site_favicon'):
            obj.site_favicon = request.FILES.get('site_favicon')
        obj.updated_by = accountuser.id
        obj.save()
        data['site_settings'] = obj
        result, msg = True, 'Success'
    except Exception as e:
        result, msg = False, 'Internal Server Error'
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return result, msg, datall