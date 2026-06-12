from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from multiselectfield import MultiSelectField
from config import app_gv as gv


class FAQCategory(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    created_by = models.CharField(max_length=8)
    updated_by = models.CharField(max_length=8)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=20, default='A', choices=gv.DATAMODE_CHOICES)
    
    class Meta:
        db_table = 'faqcategory'

    def __str__(self):
        return self.name


class Gallery(models.Model):
    
    name = models.CharField(max_length=200)
    location = models.TextField()
    photo = models.ImageField(upload_to='gallery_photos/', blank=True, null=True)
    created_by = models.CharField(max_length=8)
    updated_by = models.CharField(max_length=8)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=20, default='A', choices=gv.DATAMODE_CHOICES)
    
    class Meta:
        db_table = 'gallery_M'

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=20)
    message = models.TextField(blank=True, null=True)
    created_by = models.CharField(max_length=8)
    updated_by = models.CharField(max_length=8)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=20, default='A', choices=gv.DATAMODE_CHOICES)
    
    class Meta:
        db_table = 'contact'

    def __str__(self):
        return self.name


class Area(models.Model):
    # county = models.ForeignKey(County, on_delete=models.CASCADE,)
    name = models.CharField(max_length=200)
    short_description = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField()
    tag = MultiSelectField(choices=gv.TAG_CHOICES, blank=True)
    link = models.URLField(blank=True, null=True)
    created_by = models.CharField(max_length=8)
    updated_by = models.CharField(max_length=8)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=20, default='A', choices=gv.DATAMODE_CHOICES)

    class Meta:
        db_table = 'area'

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    name = models.CharField(max_length=200)
    short_description = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    photo = models.ImageField(upload_to="testimonials/", blank=True, null=True , help_text="Upload image with 1:1 aspect ratio(100px x 100px) ")
    tags = models.CharField(max_length=255, blank=True, null=True)
    star = models.IntegerField(default=5)
    created_by = models.CharField(max_length=8)
    updated_by = models.CharField(max_length=8)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=20, default='A', choices=gv.DATAMODE_CHOICES)

    class Meta:
        db_table = 'testimonial'

    def __str__(self):
        return f"{self.name} - {self.area.name}"


import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

PLAN_CHOICES = [
    ('THREE_MONTH', '3 Months'),
    ('SIX_MONTH',   '6 Months'),
    ('ONE_YEAR',    '1 Year'),
]

STATUS_CHOICES = [
    ('PENDING',  'Pending Review'),
    ('APPROVED', 'Approved'),
    ('REJECTED', 'Rejected'),
]


class UPIPaymentRequest(models.Model):
    id            = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user          = models.ForeignKey(User, on_delete=models.CASCADE, related_name='upi_payments')
    plan          = models.CharField(max_length=20, choices=PLAN_CHOICES)
    amount        = models.DecimalField(max_digits=8, decimal_places=2)
    utr_number    = models.CharField(max_length=50, blank=True,
                                     help_text="UTR / Transaction reference number (optional)")
    screenshot    = models.ImageField(upload_to='upi_screenshots/%Y/%m/')
    status        = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    admin_note    = models.TextField(blank=True)
    submitted_at  = models.DateTimeField(auto_now_add=True)
    reviewed_at   = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name        = 'UPI Payment Request'
        verbose_name_plural = 'UPI Payment Requests'

    def __str__(self):
        return f"{self.user} | {self.plan} | {self.status} | {self.submitted_at:%d %b %Y}"

    @property
    def plan_label(self):
        return dict(PLAN_CHOICES).get(self.plan, self.plan)

    @property
    def amount_display(self):
        return f"₹{self.amount:,.0f}"