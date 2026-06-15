import sys
import datetime
from django.urls import reverse
from django.db.models import F
from django.db.models import Sum
from config import app_utils
from config import app_logger
from config import settings
from mck_auth.models import *

log_name = "app"
logger = app_logger.createLogger(log_name)




@app_logger.functionlogs(log=log_name)
def build_role_table(request):
    table_data = dict()
    try:
        table_data = dict()
        table_data['title'] = "Role"
        table_data['sub_title'] = "Role"
        table_data['load_url'] = reverse('mck_auth:mck_role_list')
        table_data['create_url'] = reverse('mck_auth:mck_role_create')
        table_data['delete_url'] = reverse('mck_auth:mck_role_delete', args=[0])
        table_data["columns"] = list()
        
        table_data["columns"].append(dict(display_name="Name",
                                        can_show=True,
                                        class_name="",
                                        column_name="name",
                                        search_key="name"))

        table_data["columns"].append(dict(display_name="Permissions",
                                        can_show=True,
                                        class_name="",
                                        column_name="permissions",
                                        search_key=""))

        table_data["columns"].append(dict(display_name="Status",
                                        can_show=True,
                                        class_name="",
                                        column_name="datamode",
                                        search_key="datamode"))

    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return table_data





@app_logger.functionlogs(log=log_name)
def build_banner_table(request):
    table_data = dict()
    try:
        table_data = dict()
        table_data['title'] = "Banner"
        table_data['sub_title'] = "Banner"
        table_data['load_url'] = reverse('mck_master:mck_banner_list')
        table_data['create_url'] = reverse('mck_master:mck_banner_create')
        table_data['delete_url'] = reverse('mck_master:mck_banner_delete', args=[0])
        table_data["columns"] = list()
        
        table_data["columns"].append(dict(display_name="Name",
                                        can_show=True,
                                        class_name="",
                                        column_name="name",
                                        search_key="name"))

        table_data["columns"].append(dict(display_name="Status",
                                        can_show=True,
                                        class_name="",
                                        column_name="datamode",
                                        search_key="datamode"))

    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return table_data



@app_logger.functionlogs(log=log_name)
def build_gallery_table(request):
    table_data = dict()
    try:
        table_data = dict()
        table_data['title'] = "Gallery"
        table_data['sub_title'] = "Gallery"
        table_data['load_url'] = reverse('mck_master:mck_gallery_list')
        table_data['create_url'] = reverse('mck_master:mck_gallery_create')
        table_data['delete_url'] = reverse('mck_master:mck_gallery_delete', args=[0])
        table_data["columns"] = list()
        
        table_data["columns"].append(dict(display_name="Name",
                                        can_show=True,
                                        class_name="",
                                        column_name="name",
                                        search_key="name"))

        table_data["columns"].append(dict(display_name="Status",
                                        can_show=True,
                                        class_name="",
                                        column_name="datamode",
                                        search_key="datamode"))

    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return table_data


@app_logger.functionlogs(log=log_name)
def build_sub_category_table(request):
    table_data = dict()
    try:
        table_data = dict()
        table_data['title'] = "SubCategory"
        table_data['sub_title'] = "SubCategory"
        table_data['load_url'] = reverse('mck_master:mck_sub_category_list')
        table_data['create_url'] = reverse('mck_master:mck_sub_category_create')
        table_data['delete_url'] = reverse('mck_master:mck_sub_category_delete', args=[0])
        table_data["columns"] = list()
        
        table_data["columns"].append(dict(display_name="Category",
                                        can_show=True,
                                        class_name="",
                                        column_name="category",
                                        search_key="category"))

        table_data["columns"].append(dict(display_name="Name",
                                        can_show=True,
                                        class_name="",
                                        column_name="name",
                                        search_key="name"))

        table_data["columns"].append(dict(display_name="Status",
                                        can_show=True,
                                        class_name="",
                                        column_name="datamode",
                                        search_key="datamode"))

    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return table_data


@app_logger.functionlogs(log=log_name)
def build_support_page_content_table(request):
    table_data = dict()
    try:
        table_data = dict()
        table_data['title'] = "Support Page Content"
        table_data['sub_title'] = "Support Page Content"
        table_data['load_url'] = reverse('mck_master:mck_support_page_content_list')
        table_data['create_url'] = reverse('mck_master:mck_support_page_content_create')
        table_data['delete_url'] = reverse('mck_master:mck_support_page_content_delete', args=[0])
        table_data["columns"] = list()
        table_data["columns"].append(dict(display_name="Support Key",
                                        can_show=True,
                                        class_name="",
                                        column_name="support_key",
                                        search_key="support_key"))
        table_data["columns"].append(dict(display_name="Support Value",
                                        can_show=True,
                                        class_name="",
                                        column_name="support_value",
                                        search_key="support_value"))
        table_data["columns"].append(dict(display_name="Support Description",
                                        can_show=False,
                                        class_name="",
                                        column_name="support_description",
                                        search_key="support_description"))
        table_data["columns"].append(dict(display_name="Content Type",
                                        can_show=False,
                                        class_name="",
                                        column_name="content_type",
                                        search_key="content_type"))
        table_data["columns"].append(dict(display_name="Status",
                                        can_show=True,
                                        class_name="",
                                        column_name="datamode",
                                        search_key="datamode"))

    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return table_data


@app_logger.functionlogs(log=log_name)
def build_enquiry_table(request):
    table_data = dict()
    try:
        table_data = dict()
        table_data['title'] = "Enquiry"
        table_data['sub_title'] = "Enquiry"
        table_data['load_url'] = reverse('mck_lead_management:mck_enquiry_list')
        table_data['create_url'] = None
        table_data['delete_url'] = reverse('mck_lead_management:mck_enquiry_delete', args=[0])
        table_data["columns"] = list()

        table_data["columns"].append(dict(display_name="Name",
                                        can_show=True,
                                        class_name="",
                                        column_name="name",
                                        search_key="name"))

        table_data["columns"].append(dict(display_name="Mobile Number",
                                        can_show=True,
                                        class_name="",
                                        column_name="mobile_number",
                                        search_key="mobile_number"))
        
        table_data["columns"].append(dict(display_name="Email",
                                        can_show=True,
                                        class_name="",
                                        column_name="email",
                                        search_key="email"))
        
        table_data["columns"].append(dict(display_name="Permit",
                                        can_show=True,
                                        class_name="",
                                        column_name="permit",
                                        search_key="permit"))
        
        table_data["columns"].append(dict(display_name="Inspection Type",
                                        can_show=True,
                                        class_name="",
                                        column_name="inspection_type",
                                        search_key="inspection_type"))

        table_data["columns"].append(dict(display_name="Address",
                                        can_show=True,
                                        class_name="",
                                        column_name="address",
                                        search_key="address"))
        
        table_data["columns"].append(dict(display_name="Inspection Date",
                                        can_show=True,
                                        class_name="",
                                        column_name="selected_date",
                                        search_key="selected_date"))
        
        table_data["columns"].append(dict(display_name="Inspection Time",
                                        can_show=True,
                                        class_name="",
                                        column_name="selected_time",
                                        search_key="selected_time"))
        
        table_data["columns"].append(dict(display_name="Message",
                                        can_show=True,
                                        class_name="",
                                        column_name="message",
                                        search_key="message"))
        
        table_data["columns"].append(dict(display_name="Enquiry From",
                                        can_show=True,
                                        class_name="",
                                        column_name="enquiry_from",
                                        search_key="enquiry_from"))

        table_data["columns"].append(dict(display_name="Status",
                                        can_show=True,
                                        class_name="",
                                        column_name="datamode",
                                        search_key="datamode"))

    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return table_data


@app_logger.functionlogs(log=log_name)
def build_state_table(request):
    table_data = dict()
    try:
        table_data['title'] = "State"
        table_data['sub_title'] = "State Management"
        table_data['load_url'] = reverse('mck_master:mck_state_list')   
        table_data['create_url'] = reverse('mck_master:mck_state_create')  # Adjust URL name as necessary
        table_data['delete_url'] = reverse('mck_master:mck_state_delete', args=[0])  # Adjust URL name as necessary
        table_data["columns"] = list()
        
        table_data["columns"].append(dict(display_name=" name",
                                          can_show=True,
                                          class_name="",
                                          column_name="name",
                                          search_key="name"))
                                          
        table_data["columns"].append(dict(display_name=" Code",
                                          can_show=True,
                                          class_name="",
                                          column_name="code",
                                          search_key="code"))  # Assuming you have a 'code' field in State model

        table_data["columns"].append(dict(display_name="country",
                                          can_show=True,
                                          class_name="",
                                          column_name="country",
                                          search_key="country"))  # Assuming you have a 'description' field

        table_data["columns"].append(dict(display_name="Status",
                                          can_show=True,
                                          class_name="",
                                          column_name="datamode",
                                          search_key="datamode"))

    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    
    return table_data


@app_logger.functionlogs(log=logger.name)
def build_city_table(request):
    table_data = dict()
    try:
        table_data['title'] = "City"
        table_data['sub_title'] = "City Management"
        table_data['load_url'] = reverse('mck_master:mck_city_list')
        table_data['create_url'] = reverse('mck_master:mck_city_create')
        table_data['delete_url'] = reverse('mck_master:mck_city_delete', args=[0])
        table_data["columns"] = list()

        table_data["columns"].append(dict(display_name="Name",
                                          can_show=True,
                                          class_name="",
                                          column_name="name",
                                          search_key="name"))

        table_data["columns"].append(dict(display_name="Code",
                                          can_show=True,
                                          class_name="",
                                          column_name="code",
                                          search_key="code"))

        table_data["columns"].append(dict(display_name="State",
                                          can_show=True,
                                          class_name="",
                                          column_name="state",
                                          search_key="state"))
        
        table_data["columns"].append(dict(display_name="Status",
                                          can_show=True,
                                          class_name="",
                                          column_name="datamode",
                                          search_key="datamode"))

    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))

    return table_data



@app_logger.functionlogs(log=log_name)
def build_offer_table(request):
    table_data = dict()
    try:
        table_data = dict()
        table_data['title'] = "offer"
        table_data['sub_title'] = "offer"
        table_data['load_url'] = reverse('mck_master:mck_offer_list')
        table_data['create_url'] = reverse('mck_master:mck_offer_create')
        table_data['delete_url'] = reverse('mck_master:mck_offer_delete', args=[0])
        table_data["columns"] = list()

        table_data["columns"].append(dict(display_name="Name",
                                        can_show=True,
                                        class_name="",
                                        column_name="name",
                                        search_key="name"))

        table_data["columns"].append(dict(display_name="Status",
                                        can_show=True,
                                        class_name="",
                                        column_name="datamode",
                                        search_key="datamode"))

    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return table_data


@app_logger.functionlogs(log=log_name)
def build_client_feedback_table(request):
    table_data = dict()
    try:
        table_data = dict()
        table_data['title'] = "client feedback"
        table_data['sub_title'] = "client feedback"
        table_data['load_url'] = reverse('mck_master:mck_client_feedback_list')  # URL for loading the table data
        table_data['create_url'] = reverse('mck_master:mck_client_feedback_create')  # URL for creating new feedback
        table_data['delete_url'] = reverse('mck_master:mck_client_feedback_delete', args=[0])  # URL for deleting feedback
        table_data["columns"] = list()

        table_data["columns"].append(dict(display_name=" Name",  # Name of the client giving feedback
                                          can_show=True,
                                          class_name="",
                                          column_name="name",
                                          search_key="name"))

        table_data["columns"].append(dict(display_name="Feedback",  # Feedback content
                                          can_show=True,
                                          class_name="",
                                          column_name="feedback",
                                          search_key="feedback"))
        
        table_data["columns"].append(dict(display_name="Place",  # Name of the client giving feedback
                                          can_show=True,
                                          class_name="",
                                          column_name="place",
                                          search_key="place"))

        table_data["columns"].append(dict(display_name="Status",  # Status of the feedback (Active/Inactive)
                                          can_show=True,
                                          class_name="",
                                          column_name="datamode",
                                          search_key="datamode"))

    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return table_data




@app_logger.functionlogs(log=log_name)
def build_faq_category_table(request):
    table_data = dict()
    try:
        table_data['title'] = "FAQCategory"
        table_data['sub_title'] = "FAQCategory Management"
        table_data['load_url'] = reverse('svm_admin_console:mck_faq_category_list')  
        table_data['create_url'] = reverse('svm_admin_console:mck_faq_category_create')  
        table_data['delete_url'] = reverse('svm_admin_console:mck_faq_category_delete', args=[0,])  
        table_data["columns"] = list()

        table_data["columns"].append(dict(display_name="Name",  
                                          can_show=True,
                                          class_name="",
                                          column_name="name",
                                          search_key="name"))  

 

        table_data["columns"].append(dict(display_name="Status",  
                                          can_show=True,
                                          class_name="",
                                          column_name="datamode",
                                          search_key="datamode"))

    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return table_data



@app_logger.functionlogs(log=log_name)
def build_gallery_table(request):
    table_data = dict()
    try:
        table_data['title'] = "Gallery"
        table_data['sub_title'] = "Gallery Management"
        table_data['load_url'] = reverse('svm_admin_console:mck_gallery_list')  
        table_data['create_url'] = reverse('svm_admin_console:mck_gallery_create')  
        table_data['delete_url'] = reverse('svm_admin_console:mck_gallery_delete', args=[0,])  
        table_data["columns"] = list()

        table_data["columns"].append(dict(display_name="Name",  
                                          can_show=True,
                                          class_name="",
                                          column_name="name",
                                          search_key="name"))  
        
        table_data["columns"].append(dict(display_name="Location",  
                                          can_show=True,
                                          class_name="",
                                          column_name="location",
                                          search_key="location")) 
        

        table_data["columns"].append(dict(display_name="Status",  
                                          can_show=True,
                                          class_name="",
                                          column_name="datamode",
                                          search_key="datamode"))

    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return table_data



@app_logger.functionlogs(log=log_name)
def build_contact_table(request):
    table_data = dict()
    try:
        table_data['title'] = "Contact"
        table_data['sub_title'] = "Contact Management"
        table_data['load_url'] = reverse('svm_admin_console:mck_contact_list')
        table_data['hide_action'] = True
        table_data["columns"] = list()

        table_data["columns"].append(dict(
            display_name="Name",
            can_show=True,
            class_name="",
            column_name="name",
            search_key="name"
        ))

        table_data["columns"].append(dict(
            display_name="Email",
            can_show=True,
            class_name="",
            column_name="email",
            search_key="email"
        ))

        table_data["columns"].append(dict(
            display_name="Phone",
            can_show=True,
            class_name="",
            column_name="phone",
            search_key="phone"
        ))

        table_data["columns"].append(dict(
            display_name="Message",
            can_show=True,
            class_name="",
            column_name="message",
            search_key="message"
        ))

        table_data["columns"].append(dict(
            display_name="Status",
            can_show=True,
            class_name="text-center",
            column_name="datamode",
            search_key="datamode"
        ))

    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return table_data



@app_logger.functionlogs(log=log_name)
def build_testimonial_table(request):
    table_data = dict()
    try:
        table_data['title'] = "Testimonial"
        table_data['sub_title'] = "Testimonial Management"
        table_data['load_url'] = reverse('svm_admin_console:mck_testimonial_list')  
        table_data['create_url'] = reverse('svm_admin_console:mck_testimonial_create')  
        table_data['delete_url'] = reverse('svm_admin_console:mck_testimonial_delete', args=[0,])  
        table_data["columns"] = list()
  
        
        table_data["columns"].append(dict(display_name="Name",  
                                          can_show=True,
                                          class_name="",
                                          column_name="name",
                                          search_key="name")) 
        
        table_data["columns"].append(dict(display_name=" Description",  
                                          can_show=True,
                                          class_name="",
                                          column_name="description",
                                          search_key="description")) 
        
        table_data["columns"].append(dict(display_name="Star",  
                                          can_show=True,
                                          class_name="",
                                          column_name="star",
                                          search_key="star")) 

        table_data["columns"].append(dict(display_name="Status",  
                                          can_show=True,
                                          class_name="",
                                          column_name="datamode",
                                          search_key="datamode"))

    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return table_data



@app_logger.functionlogs(log=log_name)
def build_county_table(request):
    table_data = dict()
    try:
        table_data['title'] = "County"
        table_data['sub_title'] = "County Management"
        table_data['load_url'] = reverse('svm_admin_console:mck_county_list')  
        table_data['create_url'] = reverse('svm_admin_console:mck_county_create')  
        table_data['delete_url'] = reverse('svm_admin_console:mck_county_delete', args=[0,])  
        table_data["columns"] = list()

        table_data["columns"].append(dict(display_name="Name",  
                                          can_show=True,
                                          class_name="",
                                          column_name="name",
                                          search_key="name"))  

 

        table_data["columns"].append(dict(display_name="Status",  
                                          can_show=True,
                                          class_name="",
                                          column_name="datamode",
                                          search_key="datamode"))

    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return table_data


@app_logger.functionlogs(log=log_name)
def build_teams_table(request):
    table_data = dict()
    try:
        table_data['title'] = "Teams"
        table_data['sub_title'] = "Teams Management"
        table_data['load_url'] = reverse('svm_admin_console:mck_team_list')  
        table_data['create_url'] = reverse('svm_admin_console:mck_team_create')  
        table_data['delete_url'] = reverse('svm_admin_console:mck_team_delete', args=[0,])  
        table_data["columns"] = list()
        

        table_data["columns"].append(dict(display_name="Name",  
                                          can_show=True,
                                          class_name="",
                                          column_name="name",
                                          search_key="name"))
        
        table_data["columns"].append(dict(display_name="designation",  
                                          can_show=True,
                                          class_name="",
                                          column_name="designation",
                                          search_key="designation")) 
         
        table_data["columns"].append(dict(display_name="description",  
                                          can_show=True,
                                          class_name="",
                                          column_name="description",
                                          search_key="description"))  

        table_data["columns"].append(dict(display_name="Status",  
                                          can_show=True,
                                          class_name="",
                                          column_name="datamode",
                                          search_key="datamode"))

    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return table_data




@app_logger.functionlogs(log=log_name)
def build_profile_table(request):
    table_data = dict()
    try:
        table_data['title'] = "Profile"
        table_data['sub_title'] = "Profile"
        table_data['load_url'] = reverse('mck_master:mck_profile_list')
        table_data['create_url'] = reverse('mck_master:mck_profile_create')
        table_data['delete_url'] = reverse('mck_master:mck_profile_delete', args=[0])
        table_data["columns"] = list()

        table_data["columns"].append(dict(
            display_name="Name",
            can_show=True,
            class_name="",
            column_name="full_name",
            search_key="full_name"
        ))

        table_data["columns"].append(dict(
            display_name="Gender",
            can_show=True,
            class_name="",
            column_name="gender",
            search_key="gender"
        ))

        table_data["columns"].append(dict(
            display_name="Phone",
            can_show=True,
            class_name="",
            column_name="phone",
            search_key="phone"
        ))

        # UNCOMMENT AND UPDATE THESE COLUMNS
        table_data["columns"].append(dict(
            display_name="Payment Status",
            can_show=True,
            class_name="",
            column_name="payment_status",   
            search_key="payment_status",
            render_function="renderPaymentStatus"  # Custom render function
        ))

        table_data["columns"].append(dict(
            display_name="Amount Paid",
            can_show=True,
            class_name="",
            column_name="payment_amount",  
            search_key="payment_amount",
            render_function="renderPaymentAmount"  # Custom render function
        ))

        # Add registration status column
        table_data["columns"].append(dict(
            display_name="Registration",
            can_show=True,
            class_name="",
            column_name="registration_status",
            search_key="registration_status",
            render_function="renderRegistrationStatus"
        ))

        table_data["columns"].append(dict(
            display_name="Status",
            can_show=True,
            class_name="",
            column_name="datamode",
            search_key="datamode"
        ))

    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return table_data

@app_logger.functionlogs(log=log_name)
def build_category_table(request):
    table_data = dict()

    try:
        table_data['title'] = "Category"
        table_data['sub_title'] = "Category"

        table_data['load_url'] = reverse(
            'mck_website:mck_category_list'
        )

        table_data['create_url'] = reverse(
            'mck_website:mck_category_create'
        )

        table_data['delete_url'] = reverse(
            'mck_website:mck_category_delete',
            args=[0]
        )

        table_data["columns"] = []

        table_data["columns"].append(
            dict(
                display_name="Name",
                can_show=True,
                class_name="",
                column_name="name",
                search_key="name"
            )
        )

        table_data["columns"].append(
            dict(
                display_name="Slug",
                can_show=True,
                class_name="",
                column_name="slug",
                search_key="slug"
            )
        )

        table_data["columns"].append(
            dict(
                display_name="Status",
                can_show=True,
                class_name="",
                column_name="datamode",
                search_key="datamode"
            )
        )

    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()

        logger.error(
            'Error at %s:%s' %
            (exc_traceback.tb_lineno, e)
        )

    return table_data


@app_logger.functionlogs(log=log_name)
def build_product_table(request):
    table_data = dict()

    try:
        table_data['title'] = "Product"
        table_data['sub_title'] = "Product"

        table_data['load_url'] = reverse(
            'mck_website:mck_product_list'
        )

        table_data['create_url'] = reverse(
            'mck_website:mck_product_create'
        )

        table_data['delete_url'] = reverse(
            'mck_website:mck_product_delete',
            args=[0]
        )

        table_data["columns"] = []

        table_data["columns"].append(
            dict(
                display_name="Category",
                can_show=True,
                class_name="",
                column_name="category",
                search_key="category"
            )
        )

        table_data["columns"].append(
            dict(
                display_name="Name",
                can_show=True,
                class_name="",
                column_name="name",
                search_key="name"
            )
        )

        table_data["columns"].append(
            dict(
                display_name="SKU",
                can_show=True,
                class_name="",
                column_name="sku",
                search_key="sku"
            )
        )

        table_data["columns"].append(
            dict(
                display_name="Price",
                can_show=True,
                class_name="",
                column_name="price",
                search_key="price"
            )
        )

        table_data["columns"].append(
            dict(
                display_name="Stock",
                can_show=True,
                class_name="",
                column_name="stock",
                search_key="stock"
            )
        )

        table_data["columns"].append(dict(display_name="Status",
                                        can_show=True,
                                        class_name="",
                                        column_name="datamode",
                                        search_key="datamode"))

    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()

        logger.error(
            'Error at %s:%s' %
            (exc_traceback.tb_lineno, e)
        )

    return table_data


@app_logger.functionlogs(log=log_name)
def build_homepage_video_table(request):
    table_data = dict()
    try:
        table_data['title']     = "Homepage Video"
        table_data['sub_title'] = "Homepage Video"
 
        table_data['load_url'] = reverse('mck_website:mck_homepage_video_list')
        table_data['create_url'] = reverse('mck_website:mck_homepage_video_create')
        table_data['delete_url'] = reverse('mck_website:mck_homepage_video_delete', args=[0])
 
        table_data["columns"] = []
 
        table_data["columns"].append(dict(
            display_name="Title",    can_show=True,
            class_name="",           column_name="title",
            search_key="title"
        ))
        table_data["columns"].append(dict(
            display_name="Cat Button", can_show=True,
            class_name="",             column_name="cat_button",
            search_key="cat_button"
        ))
        table_data["columns"].append(dict(
            display_name="Sort Order", can_show=True,
            class_name="",             column_name="sort_order",
            search_key="sort_order"
        ))
        table_data["columns"].append(dict(
            display_name="Status", can_show=True,
            class_name="",         column_name="datamode",
            search_key="datamode"
        ))
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return table_data
 
 
@app_logger.functionlogs(log=log_name)
def build_hero_banner_table(request):
    table_data = dict()
    try:
        table_data['title']     = "Hero Banner"
        table_data['sub_title'] = "Hero Banner"
 
        table_data['load_url'] = reverse('mck_website:mck_hero_banner_list')
        table_data['create_url'] = reverse('mck_website:mck_hero_banner_create')
        table_data['delete_url'] = reverse('mck_website:mck_hero_banner_delete', args=[0])
 
        table_data["columns"] = []
 
        table_data["columns"].append(dict(
            display_name="Title",      can_show=True,
            class_name="",             column_name="title",
            search_key="title"
        ))
        table_data["columns"].append(dict(
            display_name="Sort Order", can_show=True,
            class_name="",             column_name="sort_order",
            search_key="sort_order"
        ))
        table_data["columns"].append(dict(
            display_name="Active",     can_show=True,
            class_name="",             column_name="is_active",
            search_key="is_active"
        ))
        table_data["columns"].append(dict(
            display_name="Status",     can_show=True,
            class_name="",             column_name="datamode",
            search_key="datamode"
        ))
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return table_data

# ─────────────────────────────────────────────────────────────────────────────
# Customer Table Builder
# ─────────────────────────────────────────────────────────────────────────────

@app_logger.functionlogs(log=log_name)
def build_customer_table(request):
    table_data = dict()
    try:
        table_data['title'] = "Customer"
        table_data['sub_title'] = "Customer Management"

        table_data['load_url'] = reverse('mck_website:mck_customer_list')
        table_data['create_url'] = reverse('mck_website:mck_customer_create')
        table_data['delete_url'] = reverse('mck_website:mck_customer_delete', args=[0])

        table_data["columns"] = []

        table_data["columns"].append(dict(
            display_name="First Name", can_show=True,
            class_name="", column_name="first_name",
            search_key="first_name"
        ))
        table_data["columns"].append(dict(
            display_name="Last Name", can_show=True,
            class_name="", column_name="last_name",
            search_key="last_name"
        ))
        table_data["columns"].append(dict(
            display_name="Email", can_show=True,
            class_name="", column_name="email",
            search_key="email"
        ))
        table_data["columns"].append(dict(
            display_name="Phone", can_show=True,
            class_name="", column_name="phone",
            search_key="phone"
        ))
        table_data["columns"].append(dict(
            display_name="Gender", can_show=True,
            class_name="", column_name="gender",
            search_key="gender"
        ))
        table_data["columns"].append(dict(
            display_name="Verified", can_show=True,
            class_name="", column_name="is_verified",
            search_key="is_verified"
        ))
        table_data["columns"].append(dict(
            display_name="Subscribed", can_show=True,
            class_name="", column_name="is_subscribed",
            search_key="is_subscribed"
        ))
        table_data["columns"].append(dict(
            display_name="Created On", can_show=True,
            class_name="", column_name="created_on",
            search_key="created_on"
        ))
        table_data["columns"].append(dict(
            display_name="Status", can_show=True,
            class_name="", column_name="datamode",
            search_key="datamode"
        ))
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return table_data


# ─────────────────────────────────────────────────────────────────────────────
# Address Table Builder
# ─────────────────────────────────────────────────────────────────────────────

@app_logger.functionlogs(log=log_name)
def build_address_table(request):
    table_data = dict()
    try:
        table_data['title'] = "Address"
        table_data['sub_title'] = "Address Management"

        table_data['load_url'] = reverse('mck_website:mck_address_list')
        table_data['create_url'] = reverse('mck_website:mck_address_create')
        table_data['delete_url'] = reverse('mck_website:mck_address_delete', args=[0])

        table_data["columns"] = []

        table_data["columns"].append(dict(
            display_name="Customer", can_show=True,
            class_name="", column_name="user",
            search_key="customer__first_name"
        ))
        table_data["columns"].append(dict(
            display_name="Full Name", can_show=True,
            class_name="", column_name="full_name",
            search_key="full_name"
        ))
        table_data["columns"].append(dict(
            display_name="Phone", can_show=True,
            class_name="", column_name="phone",
            search_key="phone"
        ))
        table_data["columns"].append(dict(
            display_name="Address Type", can_show=True,
            class_name="", column_name="address_type",
            search_key="address_type"
        ))
        table_data["columns"].append(dict(
            display_name="City", can_show=True,
            class_name="", column_name="city",
            search_key="city"
        ))
        table_data["columns"].append(dict(
            display_name="State", can_show=True,
            class_name="", column_name="state",
            search_key="state"
        ))
        table_data["columns"].append(dict(
            display_name="Pincode", can_show=True,
            class_name="", column_name="pincode",
            search_key="pincode"
        ))
        table_data["columns"].append(dict(
            display_name="Default", can_show=True,
            class_name="", column_name="is_default",
            search_key="is_default"
        ))
        table_data["columns"].append(dict(
            display_name="Created On", can_show=True,
            class_name="", column_name="created_on",
            search_key="created_on"
        ))
        table_data["columns"].append(dict(
            display_name="Status", can_show=True,
            class_name="", column_name="datamode",
            search_key="datamode"
        ))
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return table_data


# ─────────────────────────────────────────────────────────────────────────────
# Coupon Table Builder
# ─────────────────────────────────────────────────────────────────────────────

@app_logger.functionlogs(log=log_name)
def build_coupon_table(request):
    table_data = dict()
    try:
        table_data['title'] = "Coupon"
        table_data['sub_title'] = "Coupon Management"

        table_data['load_url'] = reverse('mck_website:mck_coupon_list')
        table_data['create_url'] = reverse('mck_website:mck_coupon_create')
        table_data['delete_url'] = reverse('mck_website:mck_coupon_delete', args=[0])

        table_data["columns"] = []

        table_data["columns"].append(dict(
            display_name="Code", can_show=True,
            class_name="", column_name="code",
            search_key="code"
        ))
        table_data["columns"].append(dict(
            display_name="Discount Type", can_show=True,
            class_name="", column_name="discount_type",
            search_key="discount_type"
        ))
        table_data["columns"].append(dict(
            display_name="Discount Value", can_show=True,
            class_name="", column_name="discount_value",
            search_key="discount_value"
        ))
        table_data["columns"].append(dict(
            display_name="Min Order Amount", can_show=True,
            class_name="", column_name="minimum_order_amount",
            search_key="minimum_order_amount"
        ))
        table_data["columns"].append(dict(
            display_name="Usage Count", can_show=True,
            class_name="", column_name="usage_count",
            search_key="usage_count"
        ))
        table_data["columns"].append(dict(
            display_name="Valid From", can_show=True,
            class_name="", column_name="valid_from",
            search_key="valid_from"
        ))
        table_data["columns"].append(dict(
            display_name="Valid Until", can_show=True,
            class_name="", column_name="valid_until",
            search_key="valid_until"
        ))
        table_data["columns"].append(dict(
            display_name="Active", can_show=True,
            class_name="", column_name="is_active",
            search_key="is_active"
        ))
        table_data["columns"].append(dict(
            display_name="Created On", can_show=True,
            class_name="", column_name="created_on",
            search_key="created_on"
        ))
        table_data["columns"].append(dict(
            display_name="Status", can_show=True,
            class_name="", column_name="datamode",
            search_key="datamode"
        ))
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return table_data


# ─────────────────────────────────────────────────────────────────────────────
# PaymentGateway Table Builder
# ─────────────────────────────────────────────────────────────────────────────

@app_logger.functionlogs(log=log_name)
def build_payment_gateway_table(request):
    table_data = dict()
    try:
        table_data['title'] = "Payment Gateway"
        table_data['sub_title'] = "Payment Gateway Management"

        table_data['load_url'] = reverse('mck_website:mck_payment_gateway_list')
        table_data['create_url'] = reverse('mck_website:mck_payment_gateway_create')
        table_data['delete_url'] = reverse('mck_website:mck_payment_gateway_delete', args=[0])

        table_data["columns"] = []

        table_data["columns"].append(dict(
            display_name="Name", can_show=True,
            class_name="", column_name="name",
            search_key="name"
        ))
        table_data["columns"].append(dict(
            display_name="Code", can_show=True,
            class_name="", column_name="code",
            search_key="code"
        ))
        table_data["columns"].append(dict(
            display_name="Description", can_show=True,
            class_name="", column_name="description",
            search_key="description"
        ))
        table_data["columns"].append(dict(
            display_name="Sort Order", can_show=True,
            class_name="", column_name="sort_order",
            search_key="sort_order"
        ))
        table_data["columns"].append(dict(
            display_name="Active", can_show=True,
            class_name="", column_name="is_active",
            search_key="is_active"
        ))
        table_data["columns"].append(dict(
            display_name="Created On", can_show=True,
            class_name="", column_name="created_on",
            search_key="created_on"
        ))
        table_data["columns"].append(dict(
            display_name="Status", can_show=True,
            class_name="", column_name="datamode",
            search_key="datamode"
        ))
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return table_data


# ─────────────────────────────────────────────────────────────────────────────
# Cart Table Builder
# ─────────────────────────────────────────────────────────────────────────────

@app_logger.functionlogs(log=log_name)
def build_cart_table(request):
    table_data = dict()
    try:
        table_data['title'] = "Cart"
        table_data['sub_title'] = "Cart Management"

        table_data['load_url'] = reverse('mck_website:mck_cart_list')
        table_data['create_url'] = None
        table_data['delete_url'] = reverse('mck_website:mck_cart_delete', args=[0])

        table_data["columns"] = []

        table_data["columns"].append(dict(
            display_name="Customer", can_show=True,
            class_name="", column_name="customer",
            search_key="customer__first_name"
        ))
        table_data["columns"].append(dict(
            display_name="Session Key", can_show=True,
            class_name="", column_name="session_key",
            search_key="session_key"
        ))
        table_data["columns"].append(dict(
            display_name="Items Count", can_show=True,
            class_name="", column_name="items_count",
            search_key="items_count"
        ))
        table_data["columns"].append(dict(
            display_name="Total Amount", can_show=True,
            class_name="", column_name="total_amount",
            search_key="total_amount"
        ))
        table_data["columns"].append(dict(
            display_name="Coupon", can_show=True,
            class_name="", column_name="coupon",
            search_key="coupon__code"
        ))
        table_data["columns"].append(dict(
            display_name="Updated On", can_show=True,
            class_name="", column_name="updated_on",
            search_key="updated_on"
        ))
        table_data["columns"].append(dict(
            display_name="Status", can_show=True,
            class_name="", column_name="datamode",
            search_key="datamode"
        ))
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return table_data


# ─────────────────────────────────────────────────────────────────────────────
# Order Table Builder
# ─────────────────────────────────────────────────────────────────────────────

@app_logger.functionlogs(log=log_name)
def build_order_table(request):
    table_data = dict()
    try:
        table_data['title'] = "Order"
        table_data['sub_title'] = "Order Management"

        table_data['load_url'] = reverse('mck_website:mck_order_list')
        table_data['create_url'] = None
        table_data['delete_url'] = reverse('mck_website:mck_order_delete', args=[0])

        table_data["columns"] = []

        table_data["columns"].append(dict(
            display_name="Order Number", can_show=True,
            class_name="", column_name="order_number",
            search_key="order_number"
        ))
        table_data["columns"].append(dict(
            display_name="Customer", can_show=True,
            class_name="", column_name="customer",
            search_key="customer__first_name"
        ))
        table_data["columns"].append(dict(
            display_name="Status", can_show=True,
            class_name="", column_name="status",
            search_key="status"
        ))
        table_data["columns"].append(dict(
            display_name="Total Amount", can_show=True,
            class_name="", column_name="total_amount",
            search_key="total_amount"
        ))
        table_data["columns"].append(dict(
            display_name="Items Count", can_show=True,
            class_name="", column_name="items_count",
            search_key="items_count"
        ))
        table_data["columns"].append(dict(
            display_name="Created On", can_show=True,
            class_name="", column_name="created_on",
            search_key="created_on"
        ))
        table_data["columns"].append(dict(
            display_name="Status", can_show=True,
            class_name="", column_name="datamode",
            search_key="datamode"
        ))
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return table_data


# ─────────────────────────────────────────────────────────────────────────────
# ProductReview Table Builder
# ─────────────────────────────────────────────────────────────────────────────

@app_logger.functionlogs(log=log_name)
def build_product_review_table(request):
    table_data = dict()
    try:
        table_data['title'] = "Product Review"
        table_data['sub_title'] = "Product Review Management"

        table_data['load_url'] = reverse('mck_website:mck_product_review_list')
        table_data['create_url'] = None
        table_data['delete_url'] = reverse('mck_website:mck_product_review_delete', args=[0])

        table_data["columns"] = []

        table_data["columns"].append(dict(
            display_name="Product", can_show=True,
            class_name="", column_name="product",
            search_key="product__name"
        ))
        table_data["columns"].append(dict(
            display_name="Customer", can_show=True,
            class_name="", column_name="customer",
            search_key="customer__first_name"
        ))
        table_data["columns"].append(dict(
            display_name="Rating", can_show=True,
            class_name="", column_name="rating",
            search_key="rating"
        ))
        table_data["columns"].append(dict(
            display_name="Title", can_show=True,
            class_name="", column_name="title",
            search_key="title"
        ))
        table_data["columns"].append(dict(
            display_name="Body", can_show=True,
            class_name="", column_name="body",
            search_key="body"
        ))
        table_data["columns"].append(dict(
            display_name="Approved", can_show=True,
            class_name="", column_name="is_approved",
            search_key="is_approved"
        ))
        table_data["columns"].append(dict(
            display_name="Created On", can_show=True,
            class_name="", column_name="created_on",
            search_key="created_on"
        ))
        table_data["columns"].append(dict(
            display_name="Status", can_show=True,
            class_name="", column_name="datamode",
            search_key="datamode"
        ))
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return table_data


# ─────────────────────────────────────────────────────────────────────────────
# Newsletter Table Builder
# ─────────────────────────────────────────────────────────────────────────────

@app_logger.functionlogs(log=log_name)
def build_newsletter_table(request):
    table_data = dict()
    try:
        table_data['title'] = "Newsletter"
        table_data['sub_title'] = "Newsletter Management"

        table_data['load_url'] = reverse('mck_website:mck_newsletter_list')
        table_data['create_url'] = None
        table_data['delete_url'] = reverse('mck_website:mck_newsletter_delete', args=[0])

        table_data["columns"] = []

        table_data["columns"].append(dict(
            display_name="Email", can_show=True,
            class_name="", column_name="email",
            search_key="email"
        ))
        table_data["columns"].append(dict(
            display_name="Active", can_show=True,
            class_name="", column_name="is_active",
            search_key="is_active"
        ))
        table_data["columns"].append(dict(
            display_name="Subscribed On", can_show=True,
            class_name="", column_name="subscribed_on",
            search_key="subscribed_on"
        ))
        table_data["columns"].append(dict(
            display_name="Created On", can_show=True,
            class_name="", column_name="created_on",
            search_key="created_on"
        ))
        table_data["columns"].append(dict(
            display_name="Status", can_show=True,
            class_name="", column_name="datamode",
            search_key="datamode"
        ))
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return table_data


# ─────────────────────────────────────────────────────────────────────────────
# ContactUs Table Builder
# ─────────────────────────────────────────────────────────────────────────────

@app_logger.functionlogs(log=log_name)
def build_contact_us_table(request):
    table_data = dict()
    try:
        table_data['title'] = "Contact Us"
        table_data['sub_title'] = "Contact Us Management"

        table_data['load_url'] = reverse('mck_website:mck_contact_us_list')
        table_data['create_url'] = None
        table_data['delete_url'] = reverse('mck_website:mck_contact_us_delete', args=[0])

        table_data["columns"] = []

        table_data["columns"].append(dict(
            display_name="Name", can_show=True,
            class_name="", column_name="name",
            search_key="name"
        ))
        table_data["columns"].append(dict(
            display_name="Email", can_show=True,
            class_name="", column_name="email",
            search_key="email"
        ))
        table_data["columns"].append(dict(
            display_name="Subject", can_show=True,
            class_name="", column_name="subject",
            search_key="subject"
        ))
        table_data["columns"].append(dict(
            display_name="Message", can_show=True,
            class_name="", column_name="message",
            search_key="message"
        ))
        table_data["columns"].append(dict(
            display_name="Status", can_show=True,
            class_name="", column_name="status",
            search_key="status"
        ))
        table_data["columns"].append(dict(
            display_name="Created On", can_show=True,
            class_name="", column_name="created_on",
            search_key="created_on"
        ))
        table_data["columns"].append(dict(
            display_name="Data Mode", can_show=True,
            class_name="", column_name="datamode",
            search_key="datamode"
        ))
    except Exception as e:
        exc_type, exc_obj, exc_traceback = sys.exc_info()
        logger.error('Error at %s:%s' % (exc_traceback.tb_lineno, e))
    return table_data