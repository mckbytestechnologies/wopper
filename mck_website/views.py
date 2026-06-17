# mck_website/views.py

import os
import sys
import json
import logging
import random
import uuid
from datetime import date, timedelta
from decimal import Decimal, DecimalException

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import Prefetch, Q
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView, DetailView, ListView
from django.views.decorators.csrf import csrf_protect

from mck_website import api
from mck_website import forms
from mck_auth import build_table as bt
from mck_auth import role_validations as rv

from config import app_logger, app_seo as seo
from mck_website import forms
from mck_admin_console.models import Contact
from mck_auth.models import User
from mck_website.models import Order, Category, Product, Blog

LOG_NAME = "app"
logger = app_logger.createLogger(LOG_NAME)


# ─────────────────────────────────────────────────────────────────────────────
# Category Views
# ─────────────────────────────────────────────────────────────────────────────

@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class CategoryList(TemplateView):
    template_name = "table_data_list.html"

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_kwargs'] = seo.get_page_tags("FAQCategoryList")
        has_permission, accountuser = rv.validate_requested_user_function(request)
        if not has_permission:
            return render(request, "access_denied.html", context)
        context['table_data'] = bt.build_category_table(request)
        return render(request, self.template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, *args, **kwargs):
        context = dict()
        try:
            context['page_kwargs'] = seo.get_page_tags("FAQCategoryList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            table_data = bt.build_category_table(request)
            context['table_data'] = table_data
            result, msg, data = api.category_load_data(request, table_data)
            return HttpResponse(json.dumps(data))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return HttpResponse(json.dumps(context))


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class CategoryCreateView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            context['name'] = "Category"
            context['page_kwargs'] = seo.get_page_tags("CategoryList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            form = forms.CategoryCreateUpdateForm()
            context['form'] = form
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            context['name'] = "Category"
            context['page_kwargs'] = seo.get_page_tags("CategoryList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            form = forms.CategoryCreateUpdateForm(request.POST, request.FILES)
            logger.debug(request.POST)
            if form.is_valid():
                result, msg, data = api.category_create_update(request)
                logger.debug(data)
                return HttpResponseRedirect(reverse("mck_website:mck_category_list"))
            else:
                context['form'] = form
                logger.warning(form.errors)
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class CategoryUpdateView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, id=None, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            mode = "edit"
            context['name'] = "Category"
            context['page_kwargs'] = seo.get_page_tags("CategoryList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            context['mode'] = mode
            result, msg, data = api.category_retrieve_data(request, id)
            form = forms.CategoryCreateUpdateForm(
                instance=data.get("category"),
                mode=mode
            )
            context['form'] = form
            context['data'] = data
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            mode = "edit"
            context['name'] = "Category"
            context['page_kwargs'] = seo.get_page_tags("CategoryList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            result, msg, data = api.category_retrieve_data(request, id)
            form = forms.CategoryCreateUpdateForm(
                request.POST,
                request.FILES,
                instance=data.get("category"),
                mode=mode
            )
            if form.is_valid():
                result, msg, data = api.category_create_update(request, id, mode)
                return HttpResponseRedirect(reverse("mck_website:mck_category_list"))
            else:
                logger.warning(form.errors)
                context['form'] = form
                context['mode'] = mode
                context['data'] = data
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class CategoryDeleteView(TemplateView):
    """Toggles a Category between Active ('A') and Inactive ('I')."""

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, *args, **kwargs):
        try:
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return JsonResponse(dict(result=False, message="Access denied"), status=403)
            result, message = api.category_update_status(request, id)
            return JsonResponse(dict(result=result, message=message))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return JsonResponse(dict(result=False, message="Internal Server Error"), status=500)


# ─────────────────────────────────────────────────────────────────────────────
# Product Views
# ─────────────────────────────────────────────────────────────────────────────

@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class ProductList(TemplateView):
    template_name = "table_data_list.html"

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_kwargs'] = seo.get_page_tags("ProductList")
        has_permission, accountuser = rv.validate_requested_user_function(request)
        if not has_permission:
            return render(request, "access_denied.html", context)
        context['table_data'] = bt.build_product_table(request)
        return render(request, self.template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, *args, **kwargs):
        context = dict()
        try:
            context['page_kwargs'] = seo.get_page_tags("ProductList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            table_data = bt.build_product_table(request)
            context['table_data'] = table_data
            result, msg, data = api.product_load_data(request, table_data)
            return HttpResponse(json.dumps(data))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return HttpResponse(json.dumps(context))


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class ProductCreateView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            context['name'] = "Product"
            context['page_kwargs'] = seo.get_page_tags("ProductList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            form = forms.ProductCreateUpdateForm()
            context['form'] = form
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            context['name'] = "Product"
            context['page_kwargs'] = seo.get_page_tags("ProductList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            form = forms.ProductCreateUpdateForm(request.POST, request.FILES)
            logger.debug(request.POST)
            if form.is_valid():
                result, msg, data = api.product_create_update(request)
                logger.debug(data)
                return HttpResponseRedirect(reverse("mck_website:mck_product_list"))
            else:
                context['form'] = form
                logger.warning(form.errors)
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class ProductUpdateView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, id=None, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            mode = "edit"
            context['name'] = "Product"
            context['page_kwargs'] = seo.get_page_tags("ProductList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            context['mode'] = mode
            result, msg, data = api.product_retrieve_data(request, id)
            form = forms.ProductCreateUpdateForm(
                instance=data.get("product"),
                mode=mode
            )
            context['form'] = form
            context['data'] = data
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            mode = "edit"
            context['name'] = "Product"
            context['page_kwargs'] = seo.get_page_tags("ProductList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            result, msg, data = api.product_retrieve_data(request, id)
            form = forms.ProductCreateUpdateForm(
                request.POST,
                request.FILES,
                instance=data.get("product"),
                mode=mode
            )
            if form.is_valid():
                result, msg, data = api.product_create_update(request, id, mode)
                return HttpResponseRedirect(reverse("mck_website:mck_product_list"))
            else:
                logger.warning(form.errors)
                context['form'] = form
                context['mode'] = mode
                context['data'] = data
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class ProductDeleteView(TemplateView):
    """Toggles a Product between Active ('A') and Inactive ('I')."""

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, *args, **kwargs):
        try:
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return JsonResponse(dict(result=False, message="Access denied"), status=403)
            result, message = api.product_update_status(request, id)
            return JsonResponse(dict(result=result, message=message))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return JsonResponse(dict(result=False, message="Internal Server Error"), status=500)


# ─────────────────────────────────────────────────────────────────────────────
# Blog Views
# ─────────────────────────────────────────────────────────────────────────────

@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class BlogList(TemplateView):
    template_name = "table_data_list.html"

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_kwargs'] = seo.get_page_tags("BlogList")
        has_permission, accountuser = rv.validate_requested_user_function(request)
        if not has_permission:
            return render(request, "access_denied.html", context)
        context['table_data'] = bt.build_blog_table(request)
        return render(request, self.template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, *args, **kwargs):
        context = dict()
        try:
            context['page_kwargs'] = seo.get_page_tags("BlogList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            table_data = bt.build_blog_table(request)
            context['table_data'] = table_data
            result, msg, data = api.blog_load_data(request, table_data)
            return HttpResponse(json.dumps(data))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return HttpResponse(json.dumps(context))


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class BlogCreateView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            context['name'] = "Blog"
            context['page_kwargs'] = seo.get_page_tags("BlogList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            form = forms.BlogCreateUpdateForm()
            context['form'] = form
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            context['name'] = "Blog"
            context['page_kwargs'] = seo.get_page_tags("BlogList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            form = forms.BlogCreateUpdateForm(request.POST, request.FILES)
            logger.debug(request.POST)
            if form.is_valid():
                result, msg, data = api.blog_create_update(request)
                logger.debug(data)
                return HttpResponseRedirect(reverse("mck_website:mck_blog_list"))
            else:
                context['form'] = form
                logger.warning(form.errors)
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class BlogUpdateView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, id=None, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            mode = "edit"
            context['name'] = "Blog"
            context['page_kwargs'] = seo.get_page_tags("BlogList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            context['mode'] = mode
            result, msg, data = api.blog_retrieve_data(request, id)
            form = forms.BlogCreateUpdateForm(
                instance=data.get("blog"),
                mode=mode
            )
            context['form'] = form
            context['data'] = data
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            mode = "edit"
            context['name'] = "Blog"
            context['page_kwargs'] = seo.get_page_tags("BlogList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            result, msg, data = api.blog_retrieve_data(request, id)
            form = forms.BlogCreateUpdateForm(
                request.POST,
                request.FILES,
                instance=data.get("blog"),
                mode=mode
            )
            if form.is_valid():
                result, msg, data = api.blog_create_update(request, id, mode)
                return HttpResponseRedirect(reverse("mck_website:mck_blog_list"))
            else:
                logger.warning(form.errors)
                context['form'] = form
                context['mode'] = mode
                context['data'] = data
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class BlogDeleteView(TemplateView):
    """Toggles a Blog between Active ('A') and Inactive ('I')."""

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, *args, **kwargs):
        try:
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return JsonResponse(dict(result=False, message="Access denied"), status=403)
            result, message = api.blog_update_status(request, id)
            return JsonResponse(dict(result=result, message=message))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return JsonResponse(dict(result=False, message="Internal Server Error"), status=500)


# ─────────────────────────────────────────────────────────────────────────────
# HomePageVideo Views
# ─────────────────────────────────────────────────────────────────────────────

@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class HomePageVideoList(TemplateView):
    template_name = "table_data_list.html"

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_kwargs'] = seo.get_page_tags("HomePageVideoList")
        has_permission, accountuser = rv.validate_requested_user_function(request)
        if not has_permission:
            return render(request, "access_denied.html", context)
        context['table_data'] = bt.build_homepage_video_table(request)
        return render(request, self.template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, *args, **kwargs):
        context = dict()
        try:
            context['page_kwargs'] = seo.get_page_tags("HomePageVideoList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            table_data = bt.build_homepage_video_table(request)
            context['table_data'] = table_data
            result, msg, data = api.homepage_video_load_data(request, table_data)
            return HttpResponse(json.dumps(data))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return HttpResponse(json.dumps(context))


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class HomePageVideoCreateView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            context['name'] = "Homepage Video"
            context['page_kwargs'] = seo.get_page_tags("HomePageVideoList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            context['form'] = forms.HomePageVideoCreateUpdateForm()
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            context['name'] = "Homepage Video"
            context['page_kwargs'] = seo.get_page_tags("HomePageVideoList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            form = forms.HomePageVideoCreateUpdateForm(request.POST, request.FILES)
            if form.is_valid():
                result, msg, data = api.homepage_video_create_update(request)
                return HttpResponseRedirect(reverse("mck_website:mck_homepage_video_list"))
            else:
                context['form'] = form
                logger.warning(form.errors)
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class HomePageVideoUpdateView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, id=None, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            mode = "edit"
            context['name'] = "Homepage Video"
            context['page_kwargs'] = seo.get_page_tags("HomePageVideoList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            context['mode'] = mode
            result, msg, data = api.homepage_video_retrieve_data(request, id)
            context['form'] = forms.HomePageVideoCreateUpdateForm(
                instance=data.get("homepage_video"),
                mode=mode
            )
            context['data'] = data
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            mode = "edit"
            context['name'] = "Homepage Video"
            context['page_kwargs'] = seo.get_page_tags("HomePageVideoList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            result, msg, data = api.homepage_video_retrieve_data(request, id)
            form = forms.HomePageVideoCreateUpdateForm(
                request.POST,
                request.FILES,
                instance=data.get("homepage_video"),
                mode=mode
            )
            if form.is_valid():
                result, msg, data = api.homepage_video_create_update(request, id, mode)
                return HttpResponseRedirect(reverse("mck_website:mck_homepage_video_list"))
            else:
                logger.warning(form.errors)
                context['form'] = form
                context['mode'] = mode
                context['data'] = data
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class HomePageVideoDeleteView(TemplateView):
    """Toggles datamode A ↔ I."""

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, *args, **kwargs):
        try:
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return JsonResponse(dict(result=False, message="Access denied"), status=403)
            result, message = api.homepage_video_update_status(request, id)
            return JsonResponse(dict(result=result, message=message))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return JsonResponse(dict(result=False, message="Internal Server Error"), status=500)


# ─────────────────────────────────────────────────────────────────────────────
# HeroBanner Views
# ─────────────────────────────────────────────────────────────────────────────

@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class HeroBannerList(TemplateView):
    template_name = "table_data_list.html"

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_kwargs'] = seo.get_page_tags("HeroBannerList")
        has_permission, accountuser = rv.validate_requested_user_function(request)
        if not has_permission:
            return render(request, "access_denied.html", context)
        context['table_data'] = bt.build_hero_banner_table(request)
        return render(request, self.template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, *args, **kwargs):
        context = dict()
        try:
            context['page_kwargs'] = seo.get_page_tags("HeroBannerList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            table_data = bt.build_hero_banner_table(request)
            context['table_data'] = table_data
            result, msg, data = api.hero_banner_load_data(request, table_data)
            return HttpResponse(json.dumps(data))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return HttpResponse(json.dumps(context))


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class HeroBannerCreateView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            context['name'] = "Hero Banner"
            context['page_kwargs'] = seo.get_page_tags("HeroBannerList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            context['form'] = forms.HeroBannerCreateUpdateForm()
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            context['name'] = "Hero Banner"
            context['page_kwargs'] = seo.get_page_tags("HeroBannerList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            form = forms.HeroBannerCreateUpdateForm(request.POST, request.FILES)
            if form.is_valid():
                result, msg, data = api.hero_banner_create_update(request)
                return HttpResponseRedirect(reverse("mck_website:mck_hero_banner_list"))
            else:
                context['form'] = form
                logger.warning(form.errors)
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class HeroBannerUpdateView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, id=None, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            mode = "edit"
            context['name'] = "Hero Banner"
            context['page_kwargs'] = seo.get_page_tags("HeroBannerList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            context['mode'] = mode
            result, msg, data = api.hero_banner_retrieve_data(request, id)
            context['form'] = forms.HeroBannerCreateUpdateForm(
                instance=data.get("hero_banner"),
                mode=mode
            )
            context['data'] = data
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            mode = "edit"
            context['name'] = "Hero Banner"
            context['page_kwargs'] = seo.get_page_tags("HeroBannerList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            result, msg, data = api.hero_banner_retrieve_data(request, id)
            form = forms.HeroBannerCreateUpdateForm(
                request.POST,
                request.FILES,
                instance=data.get("hero_banner"),
                mode=mode
            )
            if form.is_valid():
                result, msg, data = api.hero_banner_create_update(request, id, mode)
                return HttpResponseRedirect(reverse("mck_website:mck_hero_banner_list"))
            else:
                logger.warning(form.errors)
                context['form'] = form
                context['mode'] = mode
                context['data'] = data
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class HeroBannerDeleteView(TemplateView):
    """Toggles datamode A ↔ I."""

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, *args, **kwargs):
        try:
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return JsonResponse(dict(result=False, message="Access denied"), status=403)
            result, message = api.hero_banner_update_status(request, id)
            return JsonResponse(dict(result=result, message=message))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return JsonResponse(dict(result=False, message="Internal Server Error"), status=500)


# ─────────────────────────────────────────────────────────────────────────────
# Customer Views
# ─────────────────────────────────────────────────────────────────────────────

@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class CustomerList(TemplateView):
    template_name = "table_data_list.html"

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_kwargs'] = seo.get_page_tags("CustomerList")
        has_permission, accountuser = rv.validate_requested_user_function(request)
        if not has_permission:
            return render(request, "access_denied.html", context)
        context['table_data'] = bt.build_customer_table(request)
        return render(request, self.template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, *args, **kwargs):
        context = dict()
        try:
            context['page_kwargs'] = seo.get_page_tags("CustomerList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            table_data = bt.build_customer_table(request)
            context['table_data'] = table_data
            result, msg, data = api.customer_load_data(request, table_data)
            return HttpResponse(json.dumps(data))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return HttpResponse(json.dumps(context))


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class CustomerCreateView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            context['name'] = "Customer"
            context['page_kwargs'] = seo.get_page_tags("CustomerList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            form = forms.CustomerCreateUpdateForm()
            context['form'] = form
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            context['name'] = "Customer"
            context['page_kwargs'] = seo.get_page_tags("CustomerList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            form = forms.CustomerCreateUpdateForm(request.POST, request.FILES)
            if form.is_valid():
                result, msg, data = api.customer_create_update(request)
                return HttpResponseRedirect(reverse("mck_website:mck_customer_list"))
            else:
                context['form'] = form
                logger.warning(form.errors)
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class CustomerUpdateView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, id=None, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            mode = "edit"
            context['name'] = "Customer"
            context['page_kwargs'] = seo.get_page_tags("CustomerList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            context['mode'] = mode
            result, msg, data = api.customer_retrieve_data(request, id)
            form = forms.CustomerCreateUpdateForm(
                instance=data.get("customer"),
                mode=mode
            )
            context['form'] = form
            context['data'] = data
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            mode = "edit"
            context['name'] = "Customer"
            context['page_kwargs'] = seo.get_page_tags("CustomerList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            result, msg, data = api.customer_retrieve_data(request, id)
            form = forms.CustomerCreateUpdateForm(
                request.POST,
                request.FILES,
                instance=data.get("customer"),
                mode=mode
            )
            if form.is_valid():
                result, msg, data = api.customer_create_update(request, id, mode)
                return HttpResponseRedirect(reverse("mck_website:mck_customer_list"))
            else:
                logger.warning(form.errors)
                context['form'] = form
                context['mode'] = mode
                context['data'] = data
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class CustomerDeleteView(TemplateView):
    """Toggles Customer between Active ('A') and Inactive ('I')."""

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, *args, **kwargs):
        try:
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return JsonResponse(dict(result=False, message="Access denied"), status=403)
            result, message = api.customer_update_status(request, id)
            return JsonResponse(dict(result=result, message=message))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return JsonResponse(dict(result=False, message="Internal Server Error"), status=500)


# ─────────────────────────────────────────────────────────────────────────────
# Address Views
# ─────────────────────────────────────────────────────────────────────────────

@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class AddressList(TemplateView):
    template_name = "table_data_list.html"

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_kwargs'] = seo.get_page_tags("AddressList")
        has_permission, accountuser = rv.validate_requested_user_function(request)
        if not has_permission:
            return render(request, "access_denied.html", context)
        context['table_data'] = bt.build_address_table(request)
        return render(request, self.template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, *args, **kwargs):
        context = dict()
        try:
            context['page_kwargs'] = seo.get_page_tags("AddressList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            table_data = bt.build_address_table(request)
            context['table_data'] = table_data
            result, msg, data = api.address_load_data(request, table_data)
            return HttpResponse(json.dumps(data))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return HttpResponse(json.dumps(context))


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class AddressCreateView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            context['name'] = "Address"
            context['page_kwargs'] = seo.get_page_tags("AddressList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            form = forms.AddressCreateUpdateForm()
            context['form'] = form
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            context['name'] = "Address"
            context['page_kwargs'] = seo.get_page_tags("AddressList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            form = forms.AddressCreateUpdateForm(request.POST, request.FILES)
            if form.is_valid():
                result, msg, data = api.address_create_update(request)
                return HttpResponseRedirect(reverse("mck_website:mck_address_list"))
            else:
                context['form'] = form
                logger.warning(form.errors)
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class AddressUpdateView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, id=None, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            mode = "edit"
            context['name'] = "Address"
            context['page_kwargs'] = seo.get_page_tags("AddressList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            context['mode'] = mode
            result, msg, data = api.address_retrieve_data(request, id)
            form = forms.AddressCreateUpdateForm(
                instance=data.get("address"),
                mode=mode
            )
            context['form'] = form
            context['data'] = data
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            mode = "edit"
            context['name'] = "Address"
            context['page_kwargs'] = seo.get_page_tags("AddressList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            result, msg, data = api.address_retrieve_data(request, id)
            form = forms.AddressCreateUpdateForm(
                request.POST,
                request.FILES,
                instance=data.get("address"),
                mode=mode
            )
            if form.is_valid():
                result, msg, data = api.address_create_update(request, id, mode)
                return HttpResponseRedirect(reverse("mck_website:mck_address_list"))
            else:
                logger.warning(form.errors)
                context['form'] = form
                context['mode'] = mode
                context['data'] = data
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class AddressDeleteView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, *args, **kwargs):
        try:
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return JsonResponse(dict(result=False, message="Access denied"), status=403)
            result, message = api.address_update_status(request, id)
            return JsonResponse(dict(result=result, message=message))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return JsonResponse(dict(result=False, message="Internal Server Error"), status=500)


# ─────────────────────────────────────────────────────────────────────────────
# Coupon Views
# ─────────────────────────────────────────────────────────────────────────────

@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class CouponList(TemplateView):
    template_name = "table_data_list.html"

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_kwargs'] = seo.get_page_tags("CouponList")
        has_permission, accountuser = rv.validate_requested_user_function(request)
        if not has_permission:
            return render(request, "access_denied.html", context)
        context['table_data'] = bt.build_coupon_table(request)
        return render(request, self.template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, *args, **kwargs):
        context = dict()
        try:
            context['page_kwargs'] = seo.get_page_tags("CouponList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            table_data = bt.build_coupon_table(request)
            context['table_data'] = table_data
            result, msg, data = api.coupon_load_data(request, table_data)
            return HttpResponse(json.dumps(data))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return HttpResponse(json.dumps(context))


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class CouponCreateView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            context['name'] = "Coupon"
            context['page_kwargs'] = seo.get_page_tags("CouponList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            form = forms.CouponCreateUpdateForm()
            context['form'] = form
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            context['name'] = "Coupon"
            context['page_kwargs'] = seo.get_page_tags("CouponList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            form = forms.CouponCreateUpdateForm(request.POST, request.FILES)
            if form.is_valid():
                result, msg, data = api.coupon_create_update(request)
                return HttpResponseRedirect(reverse("mck_website:mck_coupon_list"))
            else:
                context['form'] = form
                logger.warning(form.errors)
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class CouponUpdateView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, id=None, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            mode = "edit"
            context['name'] = "Coupon"
            context['page_kwargs'] = seo.get_page_tags("CouponList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            context['mode'] = mode
            result, msg, data = api.coupon_retrieve_data(request, id)
            form = forms.CouponCreateUpdateForm(
                instance=data.get("coupon"),
                mode=mode
            )
            context['form'] = form
            context['data'] = data
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            mode = "edit"
            context['name'] = "Coupon"
            context['page_kwargs'] = seo.get_page_tags("CouponList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            result, msg, data = api.coupon_retrieve_data(request, id)
            form = forms.CouponCreateUpdateForm(
                request.POST,
                request.FILES,
                instance=data.get("coupon"),
                mode=mode
            )
            if form.is_valid():
                result, msg, data = api.coupon_create_update(request, id, mode)
                return HttpResponseRedirect(reverse("mck_website:mck_coupon_list"))
            else:
                logger.warning(form.errors)
                context['form'] = form
                context['mode'] = mode
                context['data'] = data
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class CouponDeleteView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, *args, **kwargs):
        try:
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return JsonResponse(dict(result=False, message="Access denied"), status=403)
            result, message = api.coupon_update_status(request, id)
            return JsonResponse(dict(result=result, message=message))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return JsonResponse(dict(result=False, message="Internal Server Error"), status=500)


# ─────────────────────────────────────────────────────────────────────────────
# PaymentGateway Views
# ─────────────────────────────────────────────────────────────────────────────

@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class PaymentGatewayList(TemplateView):
    template_name = "table_data_list.html"

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_kwargs'] = seo.get_page_tags("PaymentGatewayList")
        has_permission, accountuser = rv.validate_requested_user_function(request)
        if not has_permission:
            return render(request, "access_denied.html", context)
        context['table_data'] = bt.build_payment_gateway_table(request)
        return render(request, self.template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, *args, **kwargs):
        context = dict()
        try:
            context['page_kwargs'] = seo.get_page_tags("PaymentGatewayList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            table_data = bt.build_payment_gateway_table(request)
            context['table_data'] = table_data
            result, msg, data = api.payment_gateway_load_data(request, table_data)
            return HttpResponse(json.dumps(data))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return HttpResponse(json.dumps(context))


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class PaymentGatewayCreateView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            context['name'] = "Payment Gateway"
            context['page_kwargs'] = seo.get_page_tags("PaymentGatewayList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            form = forms.PaymentGatewayCreateUpdateForm()
            context['form'] = form
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            context['name'] = "Payment Gateway"
            context['page_kwargs'] = seo.get_page_tags("PaymentGatewayList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            form = forms.PaymentGatewayCreateUpdateForm(request.POST, request.FILES)
            if form.is_valid():
                result, msg, data = api.payment_gateway_create_update(request)
                return HttpResponseRedirect(reverse("mck_website:mck_payment_gateway_list"))
            else:
                context['form'] = form
                logger.warning(form.errors)
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class PaymentGatewayUpdateView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, id=None, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            mode = "edit"
            context['name'] = "Payment Gateway"
            context['page_kwargs'] = seo.get_page_tags("PaymentGatewayList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            context['mode'] = mode
            result, msg, data = api.payment_gateway_retrieve_data(request, id)
            form = forms.PaymentGatewayCreateUpdateForm(
                instance=data.get("payment_gateway"),
                mode=mode
            )
            context['form'] = form
            context['data'] = data
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            mode = "edit"
            context['name'] = "Payment Gateway"
            context['page_kwargs'] = seo.get_page_tags("PaymentGatewayList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            result, msg, data = api.payment_gateway_retrieve_data(request, id)
            form = forms.PaymentGatewayCreateUpdateForm(
                request.POST,
                request.FILES,
                instance=data.get("payment_gateway"),
                mode=mode
            )
            if form.is_valid():
                result, msg, data = api.payment_gateway_create_update(request, id, mode)
                return HttpResponseRedirect(reverse("mck_website:mck_payment_gateway_list"))
            else:
                logger.warning(form.errors)
                context['form'] = form
                context['mode'] = mode
                context['data'] = data
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class PaymentGatewayDeleteView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, *args, **kwargs):
        try:
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return JsonResponse(dict(result=False, message="Access denied"), status=403)
            result, message = api.payment_gateway_update_status(request, id)
            return JsonResponse(dict(result=result, message=message))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return JsonResponse(dict(result=False, message="Internal Server Error"), status=500)


# ─────────────────────────────────────────────────────────────────────────────
# Cart Views
# ─────────────────────────────────────────────────────────────────────────────

@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class CartList(TemplateView):
    template_name = "table_data_list.html"

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_kwargs'] = seo.get_page_tags("CartList")
        has_permission, accountuser = rv.validate_requested_user_function(request)
        if not has_permission:
            return render(request, "access_denied.html", context)
        context['table_data'] = bt.build_cart_table(request)
        return render(request, self.template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, *args, **kwargs):
        context = dict()
        try:
            context['page_kwargs'] = seo.get_page_tags("CartList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            table_data = bt.build_cart_table(request)
            context['table_data'] = table_data
            result, msg, data = api.cart_load_data(request, table_data)
            return HttpResponse(json.dumps(data))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return HttpResponse(json.dumps(context))


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class CartDeleteView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, *args, **kwargs):
        try:
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return JsonResponse(dict(result=False, message="Access denied"), status=403)
            result, message = api.cart_update_status(request, id)
            return JsonResponse(dict(result=result, message=message))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return JsonResponse(dict(result=False, message="Internal Server Error"), status=500)


# ─────────────────────────────────────────────────────────────────────────────
# Order Views
# ─────────────────────────────────────────────────────────────────────────────

@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class OrderList(TemplateView):
    template_name = "table_data_list.html"

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_kwargs'] = seo.get_page_tags("OrderList")
        has_permission, accountuser = rv.validate_requested_user_function(request)
        if not has_permission:
            return render(request, "access_denied.html", context)
        context['table_data'] = bt.build_order_table(request)
        return render(request, self.template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, *args, **kwargs):
        context = dict()
        try:
            context['page_kwargs'] = seo.get_page_tags("OrderList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            table_data = bt.build_order_table(request)
            context['table_data'] = table_data
            result, msg, data = api.order_load_data(request, table_data)
            return HttpResponse(json.dumps(data))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return HttpResponse(json.dumps(context))


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class OrderCreateView(TemplateView):
    
    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            context['name'] = "Order"
            context['page_kwargs'] = seo.get_page_tags("OrderList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            form = forms.OrderForm()
            context['form'] = form
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            context['name'] = "Order"
            context['page_kwargs'] = seo.get_page_tags("OrderList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            form = forms.OrderForm(request.POST)
            logger.debug(request.POST)
            if form.is_valid():
                result, msg, data = api.order_create_update(request)
                logger.debug(data)
                return HttpResponseRedirect(reverse("mck_website:mck_order_list"))
            else:
                context['form'] = form
                logger.warning(form.errors)
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class OrderUpdateView(TemplateView):
    
    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, id=None, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            mode = "edit"
            context['name'] = "Order"
            context['page_kwargs'] = seo.get_page_tags("OrderList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            context['mode'] = mode
            result, msg, data = api.order_retrieve_data(request, id)
            form = forms.OrderForm(
                instance=data.get("order"),
                mode=mode
            )
            context['form'] = form
            context['data'] = data
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            mode = "edit"
            context['name'] = "Order"
            context['page_kwargs'] = seo.get_page_tags("OrderList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            result, msg, data = api.order_retrieve_data(request, id)
            form = forms.OrderForm(
                request.POST,
                instance=data.get("order"),
                mode=mode
            )
            if form.is_valid():
                result, msg, data = api.order_create_update(request, id, mode)
                return HttpResponseRedirect(reverse("mck_website:mck_order_list"))
            else:
                logger.warning(form.errors)
                context['form'] = form
                context['mode'] = mode
                context['data'] = data
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class OrderDeleteView(TemplateView):
    """Toggles an Order between Active ('A') and Inactive ('I')."""

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, *args, **kwargs):
        try:
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return JsonResponse(dict(result=False, message="Access denied"), status=403)
            result, message = api.order_update_status(request, id)
            return JsonResponse(dict(result=result, message=message))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return JsonResponse(dict(result=False, message="Internal Server Error"), status=500)


# ─────────────────────────────────────────────────────────────────────────────
# OrderItem Views
# ─────────────────────────────────────────────────────────────────────────────

@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class OrderItemList(TemplateView):
    template_name = "table_data_list.html"

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, order_id=None, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_kwargs'] = seo.get_page_tags("OrderItemList")
        has_permission, accountuser = rv.validate_requested_user_function(request)
        if not has_permission:
            return render(request, "access_denied.html", context)
        
        if order_id:
            request.session['current_order_id'] = order_id
            context['order'] = Order.objects.filter(id=order_id).first()
        
        context['table_data'] = bt.build_order_item_table(request, order_id)
        return render(request, self.template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, order_id=None, *args, **kwargs):
        context = dict()
        try:
            context['page_kwargs'] = seo.get_page_tags("OrderItemList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            
            if not order_id:
                order_id = request.session.get('current_order_id')
            
            table_data = bt.build_order_item_table(request, order_id)
            context['table_data'] = table_data
            result, msg, data = api.order_item_load_data(request, table_data, order_id)
            return HttpResponse(json.dumps(data))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return HttpResponse(json.dumps(context))


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class OrderItemCreateView(TemplateView):
    
    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, order_id=None, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            context['name'] = "Order Item"
            context['page_kwargs'] = seo.get_page_tags("OrderItemList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            
            form = forms.OrderItemForm(order_id=order_id)
            context['form'] = form
            if order_id:
                context['order'] = Order.objects.filter(id=order_id).first()
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, order_id=None, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            context['name'] = "Order Item"
            context['page_kwargs'] = seo.get_page_tags("OrderItemList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            
            form = forms.OrderItemForm(request.POST)
            logger.debug(request.POST)
            if form.is_valid():
                result, msg, data = api.order_item_create_update(request, order_id=order_id)
                logger.debug(data)
                if order_id:
                    return HttpResponseRedirect(reverse("mck_website:mck_order_item_list", args=[order_id]))
                return HttpResponseRedirect(reverse("mck_website:mck_order_item_list_all"))
            else:
                context['form'] = form
                logger.warning(form.errors)
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class OrderItemUpdateView(TemplateView):
    
    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, id=None, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            mode = "edit"
            context['name'] = "Order Item"
            context['page_kwargs'] = seo.get_page_tags("OrderItemList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            context['mode'] = mode
            result, msg, data = api.order_item_retrieve_data(request, id)
            form = forms.OrderItemForm(
                instance=data.get("order_item"),
                mode=mode
            )
            context['form'] = form
            context['data'] = data
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            mode = "edit"
            context['name'] = "Order Item"
            context['page_kwargs'] = seo.get_page_tags("OrderItemList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            result, msg, data = api.order_item_retrieve_data(request, id)
            form = forms.OrderItemForm(
                request.POST,
                instance=data.get("order_item"),
                mode=mode
            )
            if form.is_valid():
                result, msg, data = api.order_item_create_update(request, id, mode)
                order_id = data.get('order_item').order.id if data.get('order_item') else None
                if order_id:
                    return HttpResponseRedirect(reverse("mck_website:mck_order_item_list", args=[order_id]))
                return HttpResponseRedirect(reverse("mck_website:mck_order_item_list_all"))
            else:
                logger.warning(form.errors)
                context['form'] = form
                context['mode'] = mode
                context['data'] = data
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class OrderItemDeleteView(TemplateView):
    """Toggles an OrderItem between Active ('A') and Inactive ('I')."""

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, *args, **kwargs):
        try:
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return JsonResponse(dict(result=False, message="Access denied"), status=403)
            result, message = api.order_item_update_status(request, id)
            return JsonResponse(dict(result=result, message=message))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return JsonResponse(dict(result=False, message="Internal Server Error"), status=500)


# ─────────────────────────────────────────────────────────────────────────────
# ProductReview Views
# ─────────────────────────────────────────────────────────────────────────────

@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class ProductReviewList(TemplateView):
    template_name = "table_data_list.html"

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_kwargs'] = seo.get_page_tags("ProductReviewList")
        has_permission, accountuser = rv.validate_requested_user_function(request)
        if not has_permission:
            return render(request, "access_denied.html", context)
        context['table_data'] = bt.build_product_review_table(request)
        return render(request, self.template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, *args, **kwargs):
        context = dict()
        try:
            context['page_kwargs'] = seo.get_page_tags("ProductReviewList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            table_data = bt.build_product_review_table(request)
            context['table_data'] = table_data
            result, msg, data = api.product_review_load_data(request, table_data)
            return HttpResponse(json.dumps(data))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return HttpResponse(json.dumps(context))


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class ProductReviewUpdateView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, id=None, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            mode = "edit"
            context['name'] = "Product Review"
            context['page_kwargs'] = seo.get_page_tags("ProductReviewList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            context['mode'] = mode
            result, msg, data = api.product_review_retrieve_data(request, id)
            form = forms.ProductReviewUpdateForm(
                instance=data.get("product_review"),
                mode=mode
            )
            context['form'] = form
            context['data'] = data
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            mode = "edit"
            context['name'] = "Product Review"
            context['page_kwargs'] = seo.get_page_tags("ProductReviewList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            result, msg, data = api.product_review_retrieve_data(request, id)
            form = forms.ProductReviewUpdateForm(
                request.POST,
                instance=data.get("product_review"),
                mode=mode
            )
            if form.is_valid():
                result, msg, data = api.product_review_update(request, id, mode)
                return HttpResponseRedirect(reverse("mck_website:mck_product_review_list"))
            else:
                logger.warning(form.errors)
                context['form'] = form
                context['mode'] = mode
                context['data'] = data
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class ProductReviewDeleteView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, *args, **kwargs):
        try:
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return JsonResponse(dict(result=False, message="Access denied"), status=403)
            result, message = api.product_review_update_status(request, id)
            return JsonResponse(dict(result=result, message=message))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return JsonResponse(dict(result=False, message="Internal Server Error"), status=500)


# ─────────────────────────────────────────────────────────────────────────────
# Newsletter Views
# ─────────────────────────────────────────────────────────────────────────────

@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class NewsletterList(TemplateView):
    template_name = "table_data_list.html"

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_kwargs'] = seo.get_page_tags("NewsletterList")
        has_permission, accountuser = rv.validate_requested_user_function(request)
        if not has_permission:
            return render(request, "access_denied.html", context)
        context['table_data'] = bt.build_newsletter_table(request)
        return render(request, self.template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, *args, **kwargs):
        context = dict()
        try:
            context['page_kwargs'] = seo.get_page_tags("NewsletterList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            table_data = bt.build_newsletter_table(request)
            context['table_data'] = table_data
            result, msg, data = api.newsletter_load_data(request, table_data)
            return HttpResponse(json.dumps(data))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return HttpResponse(json.dumps(context))


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class NewsletterDeleteView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, *args, **kwargs):
        try:
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return JsonResponse(dict(result=False, message="Access denied"), status=403)
            result, message = api.newsletter_update_status(request, id)
            return JsonResponse(dict(result=result, message=message))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return JsonResponse(dict(result=False, message="Internal Server Error"), status=500)


# ─────────────────────────────────────────────────────────────────────────────
# ContactUs Views
# ─────────────────────────────────────────────────────────────────────────────

@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class ContactUsList(TemplateView):
    template_name = "table_data_list.html"

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_kwargs'] = seo.get_page_tags("ContactUsList")
        has_permission, accountuser = rv.validate_requested_user_function(request)
        if not has_permission:
            return render(request, "access_denied.html", context)
        context['table_data'] = bt.build_contact_us_table(request)
        return render(request, self.template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, *args, **kwargs):
        context = dict()
        try:
            context['page_kwargs'] = seo.get_page_tags("ContactUsList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            table_data = bt.build_contact_us_table(request)
            context['table_data'] = table_data
            result, msg, data = api.contact_us_load_data(request, table_data)
            return HttpResponse(json.dumps(data))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return HttpResponse(json.dumps(context))


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class ContactUsUpdateView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, id=None, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            mode = "edit"
            context['name'] = "Contact Us"
            context['page_kwargs'] = seo.get_page_tags("ContactUsList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            context['mode'] = mode
            result, msg, data = api.contact_us_retrieve_data(request, id)
            form = forms.ContactUsUpdateForm(
                instance=data.get("contact_us"),
                mode=mode
            )
            context['form'] = form
            context['data'] = data
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            mode = "edit"
            context['name'] = "Contact Us"
            context['page_kwargs'] = seo.get_page_tags("ContactUsList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            result, msg, data = api.contact_us_retrieve_data(request, id)
            form = forms.ContactUsUpdateForm(
                request.POST,
                instance=data.get("contact_us"),
                mode=mode
            )
            if form.is_valid():
                result, msg, data = api.contact_us_update(request, id, mode)
                return HttpResponseRedirect(reverse("mck_website:mck_contact_us_list"))
            else:
                logger.warning(form.errors)
                context['form'] = form
                context['mode'] = mode
                context['data'] = data
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class ContactUsDeleteView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, *args, **kwargs):
        try:
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return JsonResponse(dict(result=False, message="Access denied"), status=403)
            result, message = api.contact_us_update_status(request, id)
            return JsonResponse(dict(result=result, message=message))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return JsonResponse(dict(result=False, message="Internal Server Error"), status=500)


# ─────────────────────────────────────────────────────────────────────────────
# SiteSettings Views (Singleton)
# ─────────────────────────────────────────────────────────────────────────────

@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class SiteSettingsUpdateView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            context['name'] = "Site Settings"
            context['page_kwargs'] = seo.get_page_tags("SiteSettings")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            
            result, msg, data = api.site_settings_retrieve_data(request)
            form = forms.SiteSettingsForm(
                instance=data.get("site_settings")
            )
            context['form'] = form
            context['data'] = data
            context['is_singleton'] = True
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            context['name'] = "Site Settings"
            context['page_kwargs'] = seo.get_page_tags("SiteSettings")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            
            result, msg, data = api.site_settings_retrieve_data(request)
            form = forms.SiteSettingsForm(
                request.POST,
                request.FILES,
                instance=data.get("site_settings")
            )
            if form.is_valid():
                result, msg, data = api.site_settings_update(request)
                return HttpResponseRedirect(reverse("mck_website:mck_site_settings"))
            else:
                logger.warning(form.errors)
                context['form'] = form
                context['data'] = data
                context['is_singleton'] = True
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)


# ─────────────────────────────────────────────────────────────────────────────
# Contact Page View
# ─────────────────────────────────────────────────────────────────────────────

class ContactPageView(TemplateView):
    template_name = "pages/contact-us.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return ajax_contact_submit(request)
        
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message')
        
        if name and email and message:
            try:
                contact = Contact(
                    name=name,
                    email=email,
                    phone=phone,
                    message=message,
                    created_by='0',
                    updated_by='0',
                    datamode='A'
                )
                contact.save()
                messages.success(request, 'Thank you! Your message has been sent successfully.')
                return redirect('mck_website:contact')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
        else:
            messages.error(request, 'Please fill in all required fields.')
        
        return render(request, self.template_name, context)


@require_POST
@csrf_exempt
def ajax_contact_submit(request):
    try:
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message')
        
        if not name or not name.strip():
            return JsonResponse({'success': False, 'message': 'Name is required.'})
        
        if not email or not email.strip():
            return JsonResponse({'success': False, 'message': 'Email is required.'})
        
        if not message or not message.strip():
            return JsonResponse({'success': False, 'message': 'Message is required.'})
        
        contact = Contact(
            name=name.strip(),
            email=email.strip(),
            phone=phone.strip() if phone else '',
            message=message.strip(),
            created_by='0',
            updated_by='0',
            datamode='A'
        )
        contact.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Thank you! Your message has been sent successfully.'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})


# ─────────────────────────────────────────────────────────────────────────────
# User Management Views
# ─────────────────────────────────────────────────────────────────────────────

@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class UserList(TemplateView):
    template_name = "table_data_list.html"

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_kwargs'] = seo.get_page_tags("UserList")
        has_permission, accountuser = rv.validate_requested_user_function(request)
        if not has_permission:
            return render(request, "access_denied.html", context)
        context['table_data'] = bt.build_user_table(request)
        return render(request, self.template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, *args, **kwargs):
        context = dict()
        try:
            context['page_kwargs'] = seo.get_page_tags("UserList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            table_data = bt.build_user_table(request)
            context['table_data'] = table_data
            result, msg, data = api.user_load_data(request, table_data)
            return HttpResponse(json.dumps(data))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return HttpResponse(json.dumps(context))


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class UserCreateView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            context['name'] = "User"
            context['page_kwargs'] = seo.get_page_tags("UserList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            form = forms.UserCreateUpdateForm()
            context['form'] = form
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            context['name'] = "User"
            context['page_kwargs'] = seo.get_page_tags("UserList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            form = forms.UserCreateUpdateForm(request.POST, request.FILES)
            logger.debug(request.POST)
            if form.is_valid():
                result, msg, data = api.user_create_update(request)
                logger.debug(data)
                return HttpResponseRedirect(reverse("mck_website:mck_user_list"))
            else:
                context['form'] = form
                logger.warning(form.errors)
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class UserUpdateView(TemplateView):

    @app_logger.functionlogs(log=LOG_NAME)
    def get(self, request, id=None, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            mode = "edit"
            context['name'] = "User"
            context['page_kwargs'] = seo.get_page_tags("UserList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            context['mode'] = mode
            result, msg, data = api.user_retrieve_data(request, id)
            form = forms.UserCreateUpdateForm(
                instance=data.get("user"),
                mode=mode
            )
            context['form'] = form
            context['data'] = data
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, *args, **kwargs):
        context = dict()
        template_name = "common_cu.html"
        try:
            mode = "edit"
            context['name'] = "User"
            context['page_kwargs'] = seo.get_page_tags("UserList")
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return render(request, "access_denied.html", context)
            result, msg, data = api.user_retrieve_data(request, id)
            form = forms.UserCreateUpdateForm(
                request.POST,
                request.FILES,
                instance=data.get("user"),
                mode=mode
            )
            if form.is_valid():
                result, msg, data = api.user_create_update(request, id, mode)
                return HttpResponseRedirect(reverse("mck_website:mck_user_list"))
            else:
                logger.warning(form.errors)
                context['form'] = form
                context['mode'] = mode
                context['data'] = data
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return render(request, template_name, context)


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class UserDeleteView(TemplateView):
    """Toggles a User between Active ('A') and Inactive ('I')."""

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, *args, **kwargs):
        try:
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return JsonResponse(dict(result=False, message="Access denied"), status=403)
            result, message = api.user_update_status(request, id)
            return JsonResponse(dict(result=result, message=message))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return JsonResponse(dict(result=False, message="Internal Server Error"), status=500)


@method_decorator(login_required(login_url=settings.LOGIN_REDIRECT_URL), name='dispatch')
class UserHardDeleteView(TemplateView):
    """Hard deletes a User (sets datamode='D')."""

    @app_logger.functionlogs(log=LOG_NAME)
    def post(self, request, id=None, *args, **kwargs):
        try:
            has_permission, accountuser = rv.validate_requested_user_function(request)
            if not has_permission:
                return JsonResponse(dict(result=False, message="Access denied"), status=403)
            result, message = api.user_delete(request, id)
            return JsonResponse(dict(result=result, message=message))
        except Exception as e:
            exc_type, exc_obj, exc_traceback = sys.exc_info()
            logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
        return JsonResponse(dict(result=False, message="Internal Server Error"), status=500)