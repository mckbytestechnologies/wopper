"""
SEO - mck P112 App
"""
from django.conf import settings


def get_page_tags(func, dynamic_seo_kwargs=None):
    """
    Build Page SEO
    """
    global_title="WOPPER "
    global_description = "WOPPER "
    global_keywords = """WOPPER """

    page_kwargs = {}
    if dynamic_seo_kwargs:
        title=dynamic_seo_kwargs.get('title','')
        keywords =dynamic_seo_kwargs.get('keywords','')
        description=dynamic_seo_kwargs.get('description','')

    elif func=="error_404":
        title="Page Not Found Error"
        keywords = "Page Not Found Error"
        description= "Page Not Found Error"

    elif func=="error_500":
        title="Internal Server Error"
        keywords = "Internal Server Error"
        description= "Internal Server Error"

    elif func=="downtime":
        title="Downtime"
        keywords = "Downtime"
        description= "Downtime"

    
        
    else:
        title=global_title
        keywords = global_keywords
        description= global_description

        page_kwargs["title"] = title
    page_kwargs["keywords"] = keywords
    page_kwargs["description"] = description

    # Static and media URLs
    page_kwargs["media_url"] = settings.STATIC_URL
    page_kwargs["uploaded_url"] = settings.MEDIA_URL

    page_kwargs["function"] = func

    return page_kwargs

    return page_kwargs
