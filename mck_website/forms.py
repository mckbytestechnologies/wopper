import sys
from django import forms
from django.forms.widgets import HiddenInput, ClearableFileInput
from django.utils.html import format_html
from django.utils.encoding import force_str
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder
from crispy_forms.helper import *
from crispy_forms.layout import *
from crispy_forms.bootstrap import *

from mck_website.models import Category, Product
from config import app_gv as gv
from mck_website import models

from mck_auth.models import AccountTypeRole


# ─────────────────────────────────────────────────────────────────────────────
# Custom image widget – shows current image thumbnail + a styled upload button
# ─────────────────────────────────────────────────────────────────────────────
class ImageUploadWidget(ClearableFileInput):
    """
    Renders a Bootstrap-styled file-upload button.
    In edit mode it also shows the current image as a small thumbnail.
    """
    template_name = None  # we override render() directly

    def render(self, name, value, attrs=None, renderer=None):
        # Build the hidden input id so JS can reference it
        input_id = attrs.get('id', f'id_{name}') if attrs else f'id_{name}'

        # Current image preview (only when a value/file already exists)
        preview_html = ''
        if value and hasattr(value, 'url'):
            try:
                preview_html = (
                    f'<div class="mb-2">'
                    f'  <img src="{value.url}" alt="Current image" '
                    f'       style="max-height:120px;max-width:200px;'
                    f'              border-radius:6px;border:1px solid #dee2e6;">'
                    f'  <p class="text-muted small mt-1 mb-0">Current image</p>'
                    f'</div>'
                )
            except Exception:
                pass

        # The actual <input type="file"> – hidden, triggered by the button
        file_input = (
            f'<input type="file" name="{name}" id="{input_id}" '
            f'class="d-none" accept="image/*" '
            f'onchange="updateFileName_{name}(this)">'
        )

        # Styled upload button + filename display
        button_html = (
            f'<div class="d-flex align-items-center gap-2 flex-wrap">'
            f'  <button type="button" class="btn btn-outline-primary btn-sm" '
            f'          onclick="document.getElementById(\'{input_id}\').click()">'
            f'    <i class="bi bi-upload me-1"></i> Choose Image'
            f'  </button>'
            f'  <span id="filename_{name}" class="text-muted small">'
            f'    {"No new file chosen" if value else "No file chosen"}'
            f'  </span>'
            f'</div>'
        )

        # Inline JS to update the filename label when user picks a file
        js = (
            f'<script>'
            f'function updateFileName_{name}(input){{'
            f'  var label = document.getElementById("filename_{name}");'
            f'  label.textContent = input.files.length > 0 '
            f'    ? input.files[0].name : "No file chosen";'
            f'}}'
            f'</script>'
        )

        return format_html(
            '{preview}{file_input}{button}{js}',
            preview=format_html(preview_html),
            file_input=format_html(file_input),
            button=format_html(button_html),
            js=format_html(js),
        )

    def value_from_datadict(self, data, files, name):
        return files.get(name)


# ─────────────────────────────────────────────────────────────────────────────
# Category form
# ─────────────────────────────────────────────────────────────────────────────
class CategoryCreateUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        mode = kwargs.pop('mode', None)
        self.instance_id = kwargs.get('instance') and kwargs['instance'].pk

        super(CategoryCreateUpdateForm, self).__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].label = str(
                self.fields[field_name].label
            ).upper()

            if field_name == 'image':
                # Replace the default widget with our custom one
                self.fields[field_name].widget = ImageUploadWidget()
                self.fields[field_name].required = False
            else:
                self.fields[field_name].widget.attrs[
                    'class'
                ] = "form-control form-control-solid"

        save_button_name = "SAVE"

        self.helper = FormHelper(self)
        self.helper.form_tag = False

        self.helper.layout = Layout(

            Fieldset(
                '',

                Row(
                    Column(Field('name'), css_class='col-md-6'),
                    Column(Field('slug'), css_class='col-md-6'),
                    css_class='row'
                ),

                Row(
                    Column(Field('image'), css_class='col-md-6'),
                    Column(Field('sort_order'), css_class='col-md-6'),
                    css_class='row'
                ),

                Row(
                    Column(Field('description'), css_class='col-md-12'),
                    css_class='row'
                ),

                Row(
                    Column(Field('is_featured'), css_class='col-md-6'),
                    Column(Field('show_on_homepage'), css_class='col-md-6'),
                    css_class='row'
                ),
            ),

            ButtonHolder(
                Div(
                    HTML(
                        '<a class="btn btn-lg btn-secondary me-3" '
                        'href="javascript:void();" '
                        'onclick="history.back()">CANCEL</a>'
                    ),

                    Submit(
                        'create_button',
                        save_button_name,
                        css_class='btn btn-lg btn-primary'
                    ),

                    css_class="d-flex text-right justify-content-end pt-10 col-12"
                ),
                css_class="row col-12 pe-5",
            )
        )

    class Meta:
        model = models.Category

        exclude = [
            'created_on',
            'updated_on',
            'created_by',
            'updated_by',
            'datamode'
        ]


# ─────────────────────────────────────────────────────────────────────────────
# Product form
# ─────────────────────────────────────────────────────────────────────────────
class ProductCreateUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        mode = kwargs.pop('mode', None)

        super(ProductCreateUpdateForm, self).__init__(*args, **kwargs)

        # Keep a reference to the current instance pk so we can exclude it
        # from the SKU uniqueness check below.
        self._instance_pk = self.instance.pk if self.instance else None

        for field_name in self.fields:
            self.fields[field_name].label = str(
                self.fields[field_name].label
            ).upper()

            if field_name == 'image':
                self.fields[field_name].widget = ImageUploadWidget()
                self.fields[field_name].required = False
            else:
                self.fields[field_name].widget.attrs[
                    'class'
                ] = "form-control form-control-solid"

        save_button_name = "SAVE"

        self.helper = FormHelper(self)
        self.helper.form_tag = False

        self.helper.layout = Layout(

            Fieldset(
                '',

                Row(
                    Column(Field('category'), css_class='col-md-6'),
                    Column(Field('name'), css_class='col-md-6'),
                    css_class='row'
                ),

                Row(
                    Column(Field('slug'), css_class='col-md-6'),
                    Column(Field('sku'), css_class='col-md-6'),
                    css_class='row'
                ),

                Row(
                    Column(Field('image'), css_class='col-md-6'),
                    Column(Field('stock'), css_class='col-md-6'),
                    css_class='row'
                ),

                Row(
                    Column(Field('price'), css_class='col-md-6'),
                    Column(Field('sale_price'), css_class='col-md-6'),
                    css_class='row'
                ),

                Row(
                    Column(Field('short_description'),
                           css_class='col-md-12'),
                    css_class='row'
                ),

                Row(
                    Column(Field('description'),
                           css_class='col-md-12'),
                    css_class='row'
                ),

                Row(
                    Column(Field('is_featured'),
                           css_class='col-md-4'),

                    Column(Field('is_best_seller'),
                           css_class='col-md-4'),

                    Column(Field('is_flash_sale'),
                           css_class='col-md-4'),

                    css_class='row'
                ),

                Row(
                    Column(Field('is_new_arrival'),
                           css_class='col-md-4'),

                    Column(Field('is_trending'),
                           css_class='col-md-4'),

                    Column(Field('is_top_rated'),
                           css_class='col-md-4'),

                    css_class='row'
                ),

                Row(
                    Column(Field('is_active'),
                           css_class='col-md-6'),
                    css_class='row'
                ),
            ),

            ButtonHolder(
                Div(
                    HTML(
                        '<a class="btn btn-lg btn-secondary me-3" '
                        'href="javascript:void();" '
                        'onclick="history.back()">CANCEL</a>'
                    ),

                    Submit(
                        'create_button',
                        save_button_name,
                        css_class='btn btn-lg btn-primary'
                    ),

                    css_class="d-flex text-right justify-content-end pt-10 col-12"
                ),
                css_class="row col-12 pe-5",
            )
        )

    # ── SKU uniqueness: exclude the current record when editing ──────────────
    def clean_sku(self):
        sku = self.cleaned_data.get('sku')
        if not sku:
            return sku

        qs = models.Product.objects.filter(sku=sku)

        # On edit: exclude the record being updated so it doesn't clash
        # with itself.
        if self._instance_pk:
            qs = qs.exclude(pk=self._instance_pk)

        if qs.exists():
            raise forms.ValidationError(
                "A product with this SKU already exists. Please use a unique SKU."
            )
        return sku

    class Meta:
        model = models.Product

        exclude = [
            'created_on',
            'updated_on',
            'created_by',
            'updated_by',
            'datamode'
        ]
# ─────────────────────────────────────────────────────────────────────────────
# ADD THESE CLASSES to your existing forms.py
#
# IMPORTANT: The ImageUploadWidget defined earlier in forms.py is NOT used
# for these forms. Instead we use HTML() blocks inside the crispy layout so
# crispy never tries to render the file widget itself (which causes "---").
# The hidden <input type="file"> is wired up purely in HTML/JS.
# ─────────────────────────────────────────────────────────────────────────────
def _image_upload_block(field_name, label, accept="image/*"):
    """
    Returns a crispy HTML() block that renders a fully self-contained
    upload button for `field_name`.  Works for both image and video fields.

    • On create  – shows "No file chosen"
    • On edit    – shows a thumbnail (images) or filename chip (video/file)
                   pulled from the Django template variable {{ form.<field>.value }}
    """
    icon = "bi-film" if accept != "image/*" else "bi-image"
    media_type = "video" if accept != "image/*" else "image"
    
    # JavaScript for image preview (without backslashes in f-string expression)
    js_preview = ''
    if media_type == "image":
        js_preview = '''
      // show inline preview for images
      if (input.files.length) { 
        var r=new FileReader(); 
        r.onload=function(e){ 
          var p=document.getElementById('current_''' + field_name + ''''); 
          if(!p){
            p=document.createElement('div');
            p.id='current_''' + field_name + '''';
            document.getElementById('wrapper_''' + field_name + '''').insertBefore(p,document.getElementById('id_''' + field_name + ''''));
          } 
          p.innerHTML='<img src="'+e.target.result+'" style="max-height:110px;max-width:200px;border-radius:6px;border:1px solid #dee2e6;margin-bottom:4px;"><p class="text-muted small mb-0">New file</p>'; 
        }; 
        r.readAsDataURL(input.files[0]); 
      }
        '''
    
    # Handle the preview for existing files
    if media_type == "video":
        preview_tag = '<video src="{{ MEDIA_URL }}{{ form.' + field_name + '.value }}" controls style="max-height:110px;max-width:220px;border-radius:6px;border:1px solid #dee2e6;"></video>'
    else:
        preview_tag = '<img src="{{ MEDIA_URL }}{{ form.' + field_name + '.value }}" alt="current" style="max-height:110px;max-width:200px;border-radius:6px;border:1px solid #dee2e6;">'

    html = f"""
        <div class="mb-4" id="wrapper_{field_name}">
        <label class="form-label fw-semibold text-uppercase small mb-2">{label}</label>

        {{# existing file preview – only rendered when editing #}}
        {{% if form.{field_name}.value %}}
            <div class="mb-2" id="current_{field_name}">
            {preview_tag}
            <p class="text-muted small mt-1 mb-0">Current file</p>
            </div>
        {{% endif %}}

        {{# hidden real file input #}}
        <input type="file"
                name="{field_name}"
                id="id_{field_name}"
                accept="{accept}"
                class="d-none"
                onchange="fileChosen_{field_name}(this)">

        {{# styled button + filename label #}}
        <div class="d-flex align-items-center gap-3 flex-wrap">
            <button type="button"
                    class="btn btn-outline-primary"
                    style="min-width:160px;"
                    onclick="document.getElementById('id_{field_name}').click()">
            <i class="bi {icon} me-2"></i>
            {"Upload Video" if media_type == "video" else "Upload Image"}
            </button>
            <span id="fname_{field_name}" class="text-muted small">No file chosen</span>
        </div>

        <script>
            function fileChosen_{field_name}(input) {{
            var el = document.getElementById('fname_{field_name}');
            el.textContent = input.files.length ? input.files[0].name : 'No file chosen';
            {js_preview}
            }}
        </script>
        </div>
        """
    return HTML(html)
# ─────────────────────────────────────────────────────────────────────────────
# HomePageVideo
# ─────────────────────────────────────────────────────────────────────────────

class HomePageVideoCreateUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        mode = kwargs.pop('mode', None)

        super(HomePageVideoCreateUpdateForm, self).__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].label = str(
                self.fields[field_name].label
            ).upper()

            if field_name in ('thumbnail_image', 'video'):
                # Make these not required so form.is_valid() passes on edit
                # when the user hasn't re-uploaded.
                self.fields[field_name].required = False
                # Keep a plain FileInput so Django can still read the POSTed
                # file; it just won't be rendered by crispy (we use HTML() below).
                self.fields[field_name].widget = forms.FileInput(
                    attrs={'class': 'd-none'}
                )
            else:
                self.fields[field_name].widget.attrs[
                    'class'
                ] = "form-control form-control-solid"

        self.helper = FormHelper(self)
        self.helper.form_tag = False

        self.helper.layout = Layout(

            Fieldset(
                '',

                Row(
                    Column(Field('title'),      css_class='col-md-6'),
                    Column(Field('cat_button'), css_class='col-md-6'),
                    css_class='row'
                ),

                Row(
                    Column(Field('sort_order'), css_class='col-md-4'),
                    css_class='row'
                ),

                # ── File upload blocks rendered as raw HTML ──────────────
                Row(
                    Column(
                        _image_upload_block('thumbnail_image', 'Thumbnail Image', accept='image/*'),
                        css_class='col-md-6'
                    ),
                    Column(
                        _image_upload_block('video', 'Video File', accept='video/*'),
                        css_class='col-md-6'
                    ),
                    css_class='row mt-2'
                ),
            ),

            ButtonHolder(
                Div(
                    HTML(
                        '<a class="btn btn-lg btn-secondary me-3" '
                        'href="javascript:void();" '
                        'onclick="history.back()">CANCEL</a>'
                    ),
                    Submit(
                        'create_button', 'SAVE',
                        css_class='btn btn-lg btn-primary'
                    ),
                    css_class="d-flex text-right justify-content-end pt-10 col-12"
                ),
                css_class="row col-12 pe-5",
            )
        )

    class Meta:
        model = models.HomePageVideo
        exclude = [
            'created_on', 'updated_on',
            'created_by', 'updated_by',
            'datamode',
        ]


# ─────────────────────────────────────────────────────────────────────────────
# HeroBanner
# ─────────────────────────────────────────────────────────────────────────────

class HeroBannerCreateUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        mode = kwargs.pop('mode', None)

        super(HeroBannerCreateUpdateForm, self).__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].label = str(
                self.fields[field_name].label
            ).upper()

            if field_name in ('desktop_image', 'mobile_image'):
                self.fields[field_name].required = False
                self.fields[field_name].widget = forms.FileInput(
                    attrs={'class': 'd-none'}
                )
            else:
                self.fields[field_name].widget.attrs[
                    'class'
                ] = "form-control form-control-solid"

        self.helper = FormHelper(self)
        self.helper.form_tag = False

        self.helper.layout = Layout(

            Fieldset(
                '',

                Row(
                    Column(Field('title'),      css_class='col-md-6'),
                    Column(Field('sort_order'), css_class='col-md-3'),
                    Column(Field('is_active'),  css_class='col-md-3'),
                    css_class='row'
                ),

                # ── Image upload blocks rendered as raw HTML ─────────────
                Row(
                    Column(
                        _image_upload_block('desktop_image', 'Desktop Image (1920×600 recommended)', accept='image/*'),
                        css_class='col-md-6'
                    ),
                    Column(
                        _image_upload_block('mobile_image', 'Mobile Image (768×400 recommended)', accept='image/*'),
                        css_class='col-md-6'
                    ),
                    css_class='row mt-2'
                ),
            ),

            ButtonHolder(
                Div(
                    HTML(
                        '<a class="btn btn-lg btn-secondary me-3" '
                        'href="javascript:void();" '
                        'onclick="history.back()">CANCEL</a>'
                    ),
                    Submit(
                        'create_button', 'SAVE',
                        css_class='btn btn-lg btn-primary'
                    ),
                    css_class="d-flex text-right justify-content-end pt-10 col-12"
                ),
                css_class="row col-12 pe-5",
            )
        )

    class Meta:
        model = models.HeroBanner
        exclude = [
            'created_on', 'updated_on',
            'created_by', 'updated_by',
            'datamode',
        ]


# ─────────────────────────────────────────────────────────────────────────────
# ADD THESE CLASSES to your existing forms.py
# Requires: ImageUploadWidget and _image_upload_block already defined above
# ─────────────────────────────────────────────────────────────────────────────


# ══════════════════════════════════════════════════════════════════════════════
# Customer
# ══════════════════════════════════════════════════════════════════════════════

class CustomerCreateUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        mode = kwargs.pop('mode', None)
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].label = str(self.fields[field_name].label).upper()
            if field_name == 'profile_image':
                self.fields[field_name].widget = forms.FileInput(attrs={'class': 'd-none'})
                self.fields[field_name].required = False
            else:
                self.fields[field_name].widget.attrs['class'] = 'form-control form-control-solid'

        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset('',
                Row(
                    Column(Field('first_name'), css_class='col-md-4'),
                    Column(Field('last_name'),  css_class='col-md-4'),
                    Column(Field('gender'),     css_class='col-md-4'),
                    css_class='row'
                ),
                Row(
                    Column(Field('email'),         css_class='col-md-4'),
                    Column(Field('phone'),         css_class='col-md-4'),
                    Column(Field('date_of_birth'), css_class='col-md-4'),
                    css_class='row'
                ),
                Row(
                    Column(Field('is_verified'),   css_class='col-md-3'),
                    Column(Field('is_subscribed'), css_class='col-md-3'),
                    css_class='row'
                ),
                Row(
                    Column(
                        _image_upload_block('profile_image', 'Profile Image', accept='image/*'),
                        css_class='col-md-6'
                    ),
                    css_class='row mt-2'
                ),
            ),
            ButtonHolder(
                Div(
                    HTML('<a class="btn btn-lg btn-secondary me-3" href="javascript:void();" onclick="history.back()">CANCEL</a>'),
                    Submit('create_button', 'SAVE', css_class='btn btn-lg btn-primary'),
                    css_class='d-flex text-right justify-content-end pt-10 col-12'
                ),
                css_class='row col-12 pe-5',
            )
        )

    class Meta:
        model = models.Customer
        exclude = ['created_on', 'updated_on', 'created_by', 'updated_by', 'datamode']


# ══════════════════════════════════════════════════════════════════════════════
# Address
# ══════════════════════════════════════════════════════════════════════════════

class AddressCreateUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        mode = kwargs.pop('mode', None)
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].label = str(self.fields[field_name].label).upper()
            self.fields[field_name].widget.attrs['class'] = 'form-control form-control-solid'

        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset('',
                Row(
                    Column(Field('customer'),     css_class='col-md-4'),
                    Column(Field('address_type'), css_class='col-md-4'),
                    Column(Field('is_default'),   css_class='col-md-4'),
                    css_class='row'
                ),
                Row(
                    Column(Field('full_name'), css_class='col-md-6'),
                    Column(Field('phone'),     css_class='col-md-6'),
                    css_class='row'
                ),
                Row(
                    Column(Field('address_line1'), css_class='col-md-6'),
                    Column(Field('address_line2'), css_class='col-md-6'),
                    css_class='row'
                ),
                Row(
                    Column(Field('city'),    css_class='col-md-3'),
                    Column(Field('state'),   css_class='col-md-3'),
                    Column(Field('pincode'), css_class='col-md-3'),
                    Column(Field('country'), css_class='col-md-3'),
                    css_class='row'
                ),
            ),
            ButtonHolder(
                Div(
                    HTML('<a class="btn btn-lg btn-secondary me-3" href="javascript:void();" onclick="history.back()">CANCEL</a>'),
                    Submit('create_button', 'SAVE', css_class='btn btn-lg btn-primary'),
                    css_class='d-flex text-right justify-content-end pt-10 col-12'
                ),
                css_class='row col-12 pe-5',
            )
        )

    class Meta:
        model = models.Address
        exclude = ['created_on', 'updated_on', 'created_by', 'updated_by', 'datamode']


# ══════════════════════════════════════════════════════════════════════════════
# Coupon
# ══════════════════════════════════════════════════════════════════════════════

class CouponCreateUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        mode = kwargs.pop('mode', None)
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].label = str(self.fields[field_name].label).upper()
            self.fields[field_name].widget.attrs['class'] = 'form-control form-control-solid'

        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset('',
                Row(
                    Column(Field('code'),          css_class='col-md-4'),
                    Column(Field('discount_type'), css_class='col-md-4'),
                    Column(Field('discount_value'),css_class='col-md-4'),
                    css_class='row'
                ),
                Row(
                    Column(Field('minimum_order_amount'),    css_class='col-md-4'),
                    Column(Field('maximum_discount_amount'), css_class='col-md-4'),
                    Column(Field('per_user_limit'),          css_class='col-md-4'),
                    css_class='row'
                ),
                Row(
                    Column(Field('usage_limit'), css_class='col-md-4'),
                    Column(Field('valid_from'),  css_class='col-md-4'),
                    Column(Field('valid_until'), css_class='col-md-4'),
                    css_class='row'
                ),
                Row(
                    Column(Field('description'), css_class='col-md-9'),
                    Column(Field('is_active'),   css_class='col-md-3'),
                    css_class='row'
                ),
            ),
            ButtonHolder(
                Div(
                    HTML('<a class="btn btn-lg btn-secondary me-3" href="javascript:void();" onclick="history.back()">CANCEL</a>'),
                    Submit('create_button', 'SAVE', css_class='btn btn-lg btn-primary'),
                    css_class='d-flex text-right justify-content-end pt-10 col-12'
                ),
                css_class='row col-12 pe-5',
            )
        )

    class Meta:
        model = models.Coupon
        exclude = ['created_on', 'updated_on', 'created_by', 'updated_by', 'datamode', 'usage_count']


# ══════════════════════════════════════════════════════════════════════════════
# PaymentGateway
# ══════════════════════════════════════════════════════════════════════════════

class PaymentGatewayCreateUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        mode = kwargs.pop('mode', None)
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].label = str(self.fields[field_name].label).upper()
            if field_name == 'logo':
                self.fields[field_name].widget = forms.FileInput(attrs={'class': 'd-none'})
                self.fields[field_name].required = False
            else:
                self.fields[field_name].widget.attrs['class'] = 'form-control form-control-solid'

        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset('',
                Row(
                    Column(Field('name'),       css_class='col-md-4'),
                    Column(Field('code'),       css_class='col-md-4'),
                    Column(Field('sort_order'), css_class='col-md-2'),
                    Column(Field('is_active'),  css_class='col-md-2'),
                    css_class='row'
                ),
                Row(
                    Column(Field('description'), css_class='col-md-8'),
                    css_class='row'
                ),
                Row(
                    Column(Field('config_json'), css_class='col-md-12'),
                    css_class='row'
                ),
                Row(
                    Column(
                        _image_upload_block('logo', 'Gateway Logo', accept='image/*'),
                        css_class='col-md-6'
                    ),
                    css_class='row mt-2'
                ),
            ),
            ButtonHolder(
                Div(
                    HTML('<a class="btn btn-lg btn-secondary me-3" href="javascript:void();" onclick="history.back()">CANCEL</a>'),
                    Submit('create_button', 'SAVE', css_class='btn btn-lg btn-primary'),
                    css_class='d-flex text-right justify-content-end pt-10 col-12'
                ),
                css_class='row col-12 pe-5',
            )
        )

    class Meta:
        model = models.PaymentGateway
        exclude = ['created_on', 'updated_on', 'created_by', 'updated_by', 'datamode']


# ══════════════════════════════════════════════════════════════════════════════
# Cart
# ══════════════════════════════════════════════════════════════════════════════

class CartCreateUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        mode = kwargs.pop('mode', None)
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].label = str(self.fields[field_name].label).upper()
            self.fields[field_name].widget.attrs['class'] = 'form-control form-control-solid'

        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset('',
                Row(
                    Column(Field('customer'),    css_class='col-md-5'),
                    Column(Field('coupon'),      css_class='col-md-4'),
                    Column(Field('session_key'), css_class='col-md-3'),
                    css_class='row'
                ),
            ),
            ButtonHolder(
                Div(
                    HTML('<a class="btn btn-lg btn-secondary me-3" href="javascript:void();" onclick="history.back()">CANCEL</a>'),
                    Submit('create_button', 'SAVE', css_class='btn btn-lg btn-primary'),
                    css_class='d-flex text-right justify-content-end pt-10 col-12'
                ),
                css_class='row col-12 pe-5',
            )
        )

    class Meta:
        model = models.Cart
        exclude = ['created_on', 'updated_on', 'created_by', 'updated_by', 'datamode']


# ══════════════════════════════════════════════════════════════════════════════
# CartItem
# ══════════════════════════════════════════════════════════════════════════════

class CartItemCreateUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        mode = kwargs.pop('mode', None)
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].label = str(self.fields[field_name].label).upper()
            self.fields[field_name].widget.attrs['class'] = 'form-control form-control-solid'

        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset('',
                Row(
                    Column(Field('cart'),     css_class='col-md-4'),
                    Column(Field('product'),  css_class='col-md-4'),
                    Column(Field('quantity'), css_class='col-md-2'),
                    Column(Field('price'),    css_class='col-md-2'),
                    css_class='row'
                ),
            ),
            ButtonHolder(
                Div(
                    HTML('<a class="btn btn-lg btn-secondary me-3" href="javascript:void();" onclick="history.back()">CANCEL</a>'),
                    Submit('create_button', 'SAVE', css_class='btn btn-lg btn-primary'),
                    css_class='d-flex text-right justify-content-end pt-10 col-12'
                ),
                css_class='row col-12 pe-5',
            )
        )

    class Meta:
        model = models.CartItem
        exclude = ['created_on', 'updated_on', 'created_by', 'updated_by', 'datamode']


# ══════════════════════════════════════════════════════════════════════════════
# Wishlist
# ══════════════════════════════════════════════════════════════════════════════

class WishlistCreateUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        mode = kwargs.pop('mode', None)
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].label = str(self.fields[field_name].label).upper()
            self.fields[field_name].widget.attrs['class'] = 'form-control form-control-solid'

        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset('',
                Row(
                    Column(Field('customer'), css_class='col-md-6'),
                    Column(Field('product'),  css_class='col-md-6'),
                    css_class='row'
                ),
            ),
            ButtonHolder(
                Div(
                    HTML('<a class="btn btn-lg btn-secondary me-3" href="javascript:void();" onclick="history.back()">CANCEL</a>'),
                    Submit('create_button', 'SAVE', css_class='btn btn-lg btn-primary'),
                    css_class='d-flex text-right justify-content-end pt-10 col-12'
                ),
                css_class='row col-12 pe-5',
            )
        )

    class Meta:
        model = models.Wishlist
        exclude = ['created_on', 'updated_on', 'created_by', 'updated_by', 'datamode']


# ══════════════════════════════════════════════════════════════════════════════
# Order
# ══════════════════════════════════════════════════════════════════════════════

class OrderCreateUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        mode = kwargs.pop('mode', None)
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].label = str(self.fields[field_name].label).upper()
            self.fields[field_name].widget.attrs['class'] = 'form-control form-control-solid'

        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset('',
                Row(
                    Column(Field('customer'),     css_class='col-md-4'),
                    Column(Field('order_number'), css_class='col-md-4'),
                    Column(Field('status'),       css_class='col-md-4'),
                    css_class='row'
                ),
                Row(
                    Column(Field('coupon'), css_class='col-md-4'),
                    css_class='row'
                ),
                HTML('<hr><p class="fw-bold text-uppercase small text-muted mt-2">Shipping Address</p>'),
                Row(
                    Column(Field('shipping_full_name'), css_class='col-md-6'),
                    Column(Field('shipping_phone'),     css_class='col-md-6'),
                    css_class='row'
                ),
                Row(
                    Column(Field('shipping_address_line1'), css_class='col-md-6'),
                    Column(Field('shipping_address_line2'), css_class='col-md-6'),
                    css_class='row'
                ),
                Row(
                    Column(Field('shipping_city'),    css_class='col-md-3'),
                    Column(Field('shipping_state'),   css_class='col-md-3'),
                    Column(Field('shipping_pincode'), css_class='col-md-3'),
                    Column(Field('shipping_country'), css_class='col-md-3'),
                    css_class='row'
                ),
                HTML('<hr><p class="fw-bold text-uppercase small text-muted mt-2">Amounts</p>'),
                Row(
                    Column(Field('subtotal'),        css_class='col-md-3'),
                    Column(Field('discount_amount'), css_class='col-md-3'),
                    Column(Field('shipping_charge'), css_class='col-md-3'),
                    Column(Field('tax_amount'),      css_class='col-md-3'),
                    css_class='row'
                ),
                Row(
                    Column(Field('total_amount'), css_class='col-md-3'),
                    Column(Field('delivered_on'), css_class='col-md-3'),
                    css_class='row'
                ),
                Row(
                    Column(Field('notes'), css_class='col-md-12'),
                    css_class='row'
                ),
            ),
            ButtonHolder(
                Div(
                    HTML('<a class="btn btn-lg btn-secondary me-3" href="javascript:void();" onclick="history.back()">CANCEL</a>'),
                    Submit('create_button', 'SAVE', css_class='btn btn-lg btn-primary'),
                    css_class='d-flex text-right justify-content-end pt-10 col-12'
                ),
                css_class='row col-12 pe-5',
            )
        )

    class Meta:
        model = models.Order
        exclude = ['created_on', 'updated_on', 'created_by', 'updated_by', 'datamode']


# ══════════════════════════════════════════════════════════════════════════════
# OrderItem
# ══════════════════════════════════════════════════════════════════════════════

class OrderItemCreateUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        mode = kwargs.pop('mode', None)
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].label = str(self.fields[field_name].label).upper()
            self.fields[field_name].widget.attrs['class'] = 'form-control form-control-solid'

        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset('',
                Row(
                    Column(Field('order'),        css_class='col-md-4'),
                    Column(Field('product'),      css_class='col-md-4'),
                    Column(Field('quantity'),     css_class='col-md-2'),
                    Column(Field('unit_price'),   css_class='col-md-2'),
                    css_class='row'
                ),
                Row(
                    Column(Field('product_name'),  css_class='col-md-4'),
                    Column(Field('product_sku'),   css_class='col-md-4'),
                    Column(Field('total_price'),   css_class='col-md-2'),
                    css_class='row'
                ),
                Row(
                    Column(Field('product_image'), css_class='col-md-6'),
                    css_class='row'
                ),
            ),
            ButtonHolder(
                Div(
                    HTML('<a class="btn btn-lg btn-secondary me-3" href="javascript:void();" onclick="history.back()">CANCEL</a>'),
                    Submit('create_button', 'SAVE', css_class='btn btn-lg btn-primary'),
                    css_class='d-flex text-right justify-content-end pt-10 col-12'
                ),
                css_class='row col-12 pe-5',
            )
        )

    class Meta:
        model = models.OrderItem
        exclude = ['created_on', 'updated_on', 'created_by', 'updated_by', 'datamode']


# ══════════════════════════════════════════════════════════════════════════════
# Payment
# ══════════════════════════════════════════════════════════════════════════════

class PaymentCreateUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        mode = kwargs.pop('mode', None)
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].label = str(self.fields[field_name].label).upper()
            self.fields[field_name].widget.attrs['class'] = 'form-control form-control-solid'

        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset('',
                Row(
                    Column(Field('order'),           css_class='col-md-4'),
                    Column(Field('payment_gateway'), css_class='col-md-4'),
                    Column(Field('status'),          css_class='col-md-4'),
                    css_class='row'
                ),
                Row(
                    Column(Field('transaction_id'),   css_class='col-md-4'),
                    Column(Field('gateway_order_id'), css_class='col-md-4'),
                    Column(Field('amount'),           css_class='col-md-2'),
                    Column(Field('currency'),         css_class='col-md-2'),
                    css_class='row'
                ),
                Row(
                    Column(Field('paid_on'),          css_class='col-md-4'),
                    css_class='row'
                ),
                Row(
                    Column(Field('gateway_response'), css_class='col-md-12'),
                    css_class='row'
                ),
            ),
            ButtonHolder(
                Div(
                    HTML('<a class="btn btn-lg btn-secondary me-3" href="javascript:void();" onclick="history.back()">CANCEL</a>'),
                    Submit('create_button', 'SAVE', css_class='btn btn-lg btn-primary'),
                    css_class='d-flex text-right justify-content-end pt-10 col-12'
                ),
                css_class='row col-12 pe-5',
            )
        )

    class Meta:
        model = models.Payment
        exclude = ['created_on', 'updated_on', 'created_by', 'updated_by', 'datamode']


# ══════════════════════════════════════════════════════════════════════════════
# ProductReview
# ══════════════════════════════════════════════════════════════════════════════

class ProductReviewCreateUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        mode = kwargs.pop('mode', None)
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].label = str(self.fields[field_name].label).upper()
            self.fields[field_name].widget.attrs['class'] = 'form-control form-control-solid'

        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset('',
                Row(
                    Column(Field('product'),    css_class='col-md-4'),
                    Column(Field('customer'),   css_class='col-md-4'),
                    Column(Field('order_item'), css_class='col-md-4'),
                    css_class='row'
                ),
                Row(
                    Column(Field('rating'),      css_class='col-md-3'),
                    Column(Field('title'),       css_class='col-md-6'),
                    Column(Field('is_approved'), css_class='col-md-3'),
                    css_class='row'
                ),
                Row(
                    Column(Field('body'), css_class='col-md-12'),
                    css_class='row'
                ),
            ),
            ButtonHolder(
                Div(
                    HTML('<a class="btn btn-lg btn-secondary me-3" href="javascript:void();" onclick="history.back()">CANCEL</a>'),
                    Submit('create_button', 'SAVE', css_class='btn btn-lg btn-primary'),
                    css_class='d-flex text-right justify-content-end pt-10 col-12'
                ),
                css_class='row col-12 pe-5',
            )
        )

    class Meta:
        model = models.ProductReview
        exclude = ['created_on', 'updated_on', 'created_by', 'updated_by', 'datamode']


# ══════════════════════════════════════════════════════════════════════════════
# Newsletter
# ══════════════════════════════════════════════════════════════════════════════

class NewsletterCreateUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        mode = kwargs.pop('mode', None)
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].label = str(self.fields[field_name].label).upper()
            self.fields[field_name].widget.attrs['class'] = 'form-control form-control-solid'

        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset('',
                Row(
                    Column(Field('email'),     css_class='col-md-6'),
                    Column(Field('is_active'), css_class='col-md-3'),
                    css_class='row'
                ),
            ),
            ButtonHolder(
                Div(
                    HTML('<a class="btn btn-lg btn-secondary me-3" href="javascript:void();" onclick="history.back()">CANCEL</a>'),
                    Submit('create_button', 'SAVE', css_class='btn btn-lg btn-primary'),
                    css_class='d-flex text-right justify-content-end pt-10 col-12'
                ),
                css_class='row col-12 pe-5',
            )
        )

    class Meta:
        model = models.Newsletter
        exclude = ['created_on', 'updated_on', 'created_by', 'updated_by', 'datamode', 'subscribed_on']


# ══════════════════════════════════════════════════════════════════════════════
# ContactUs
# ══════════════════════════════════════════════════════════════════════════════

class ContactUsCreateUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        mode = kwargs.pop('mode', None)
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].label = str(self.fields[field_name].label).upper()
            self.fields[field_name].widget.attrs['class'] = 'form-control form-control-solid'

        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset('',
                Row(
                    Column(Field('name'),    css_class='col-md-4'),
                    Column(Field('email'),   css_class='col-md-4'),
                    Column(Field('phone'),   css_class='col-md-4'),
                    css_class='row'
                ),
                Row(
                    Column(Field('subject'), css_class='col-md-8'),
                    Column(Field('status'),  css_class='col-md-4'),
                    css_class='row'
                ),
                Row(
                    Column(Field('message'),     css_class='col-md-12'),
                    css_class='row'
                ),
                Row(
                    Column(Field('admin_notes'), css_class='col-md-12'),
                    css_class='row'
                ),
                Row(
                    Column(Field('replied_on'), css_class='col-md-4'),
                    css_class='row'
                ),
            ),
            ButtonHolder(
                Div(
                    HTML('<a class="btn btn-lg btn-secondary me-3" href="javascript:void();" onclick="history.back()">CANCEL</a>'),
                    Submit('create_button', 'SAVE', css_class='btn btn-lg btn-primary'),
                    css_class='d-flex text-right justify-content-end pt-10 col-12'
                ),
                css_class='row col-12 pe-5',
            )
        )

    class Meta:
        model = models.ContactUs
        exclude = ['created_on', 'updated_on', 'created_by', 'updated_by', 'datamode']


# ══════════════════════════════════════════════════════════════════════════════
# SiteSettings  (singleton – no create, just edit)
# ══════════════════════════════════════════════════════════════════════════════

class SiteSettingsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        mode = kwargs.pop('mode', None)
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].label = str(self.fields[field_name].label).upper()
            if field_name in ('site_logo', 'site_favicon'):
                self.fields[field_name].widget = forms.FileInput(attrs={'class': 'd-none'})
                self.fields[field_name].required = False
            else:
                self.fields[field_name].widget.attrs['class'] = 'form-control form-control-solid'

        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset('',
                HTML('<p class="fw-bold text-uppercase small text-muted">General</p>'),
                Row(
                    Column(Field('site_name'),    css_class='col-md-4'),
                    Column(Field('site_tagline'), css_class='col-md-4'),
                    Column(Field('site_email'),   css_class='col-md-4'),
                    css_class='row'
                ),
                Row(
                    Column(Field('site_phone'),     css_class='col-md-4'),
                    Column(Field('site_phone_alt'), css_class='col-md-4'),
                    css_class='row'
                ),
                Row(
                    Column(Field('site_address'), css_class='col-md-12'),
                    css_class='row'
                ),
                Row(
                    Column(
                        _image_upload_block('site_logo', 'Site Logo', accept='image/*'),
                        css_class='col-md-6'
                    ),
                    Column(
                        _image_upload_block('site_favicon', 'Favicon', accept='image/*'),
                        css_class='col-md-6'
                    ),
                    css_class='row mt-2'
                ),
                HTML('<hr><p class="fw-bold text-uppercase small text-muted mt-2">Social Media</p>'),
                Row(
                    Column(Field('facebook_url'),  css_class='col-md-4'),
                    Column(Field('instagram_url'), css_class='col-md-4'),
                    Column(Field('twitter_url'),   css_class='col-md-4'),
                    css_class='row'
                ),
                Row(
                    Column(Field('youtube_url'),  css_class='col-md-4'),
                    Column(Field('linkedin_url'), css_class='col-md-4'),
                    css_class='row'
                ),
                HTML('<hr><p class="fw-bold text-uppercase small text-muted mt-2">SEO</p>'),
                Row(
                    Column(Field('meta_title'),          css_class='col-md-6'),
                    Column(Field('google_analytics_id'), css_class='col-md-6'),
                    css_class='row'
                ),
                Row(
                    Column(Field('meta_description'), css_class='col-md-6'),
                    Column(Field('meta_keywords'),    css_class='col-md-6'),
                    css_class='row'
                ),
                HTML('<hr><p class="fw-bold text-uppercase small text-muted mt-2">Commerce</p>'),
                Row(
                    Column(Field('currency_code'),        css_class='col-md-3'),
                    Column(Field('currency_symbol'),      css_class='col-md-3'),
                    Column(Field('free_shipping_above'),  css_class='col-md-3'),
                    Column(Field('tax_percentage'),       css_class='col-md-3'),
                    css_class='row'
                ),
                HTML('<hr><p class="fw-bold text-uppercase small text-muted mt-2">Policies</p>'),
                Row(
                    Column(Field('privacy_policy'),   css_class='col-md-6'),
                    Column(Field('terms_conditions'), css_class='col-md-6'),
                    css_class='row'
                ),
                Row(
                    Column(Field('return_policy'),   css_class='col-md-6'),
                    Column(Field('shipping_policy'), css_class='col-md-6'),
                    css_class='row'
                ),
            ),
            ButtonHolder(
                Div(
                    Submit('create_button', 'SAVE SETTINGS', css_class='btn btn-lg btn-primary'),
                    css_class='d-flex text-right justify-content-end pt-10 col-12'
                ),
                css_class='row col-12 pe-5',
            )
        )

    class Meta:
        model = models.SiteSettings
        exclude = ['created_on', 'updated_on', 'created_by', 'updated_by']