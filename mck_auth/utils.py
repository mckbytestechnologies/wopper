# mck_auth/utils.py

from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_otp_email(email, otp, first_name=""):
    """Send OTP email for verification - Wopper Cleaning Products"""
    try:
        subject = "Verify Your Email - Wopper Cleaning Solutions 🧹"
        
        html_message = f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{
                    font-family: 'Segoe UI', Arial, sans-serif;
                    line-height: 1.6;
                    margin: 0;
                    padding: 0;
                    background-color: #f4f4f4;
                }}
                .container {{
                    max-width: 600px;
                    margin: 20px auto;
                    background: white;
                    border-radius: 12px;
                    overflow: hidden;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                }}
                .header {{
                    background: linear-gradient(135deg, #00828a 0%, #00a3ad 100%);
                    padding: 30px;
                    text-align: center;
                }}
                .header h1 {{
                    color: white;
                    margin: 0;
                    font-size: 28px;
                    font-weight: 700;
                }}
                .header p {{
                    color: rgba(255,255,255,0.9);
                    margin: 5px 0 0;
                }}
                .content {{
                    padding: 30px;
                    background: #ffffff;
                }}
                .greeting {{
                    font-size: 18px;
                    color: #333;
                    margin-bottom: 20px;
                }}
                .otp-box {{
                    background: linear-gradient(135deg, #e8f5f6 0%, #d4edef 100%);
                    padding: 25px;
                    text-align: center;
                    border-radius: 10px;
                    margin: 25px 0;
                    border: 2px dashed #00828a;
                }}
                .otp-code {{
                    font-size: 36px;
                    font-weight: bold;
                    letter-spacing: 8px;
                    color: #00828a;
                    font-family: monospace;
                }}
                .expiry {{
                    color: #ff6b6b;
                    font-weight: bold;
                    margin-top: 15px;
                }}
                .features {{
                    background: #f9f9f9;
                    padding: 20px;
                    border-radius: 8px;
                    margin: 20px 0;
                }}
                .feature-item {{
                    display: flex;
                    align-items: center;
                    margin-bottom: 12px;
                }}
                .feature-icon {{
                    width: 30px;
                    color: #00828a;
                    font-size: 18px;
                }}
                .footer {{
                    background: #f5f5f5;
                    padding: 20px;
                    text-align: center;
                    font-size: 12px;
                    color: #666;
                }}
                .button {{
                    display: inline-block;
                    background: #00828a;
                    color: white;
                    padding: 10px 20px;
                    text-decoration: none;
                    border-radius: 5px;
                    margin-top: 15px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🧹 Wopper Cleaning Solutions</h1>
                    <p>Premium Cleaning & Hygiene Products</p>
                </div>
                <div class="content">
                    <div class="greeting">
                        <strong>Hello {first_name or 'Valued Customer'}! 👋</strong>
                    </div>
                    
                    <p>Thank you for joining <strong>Wopper</strong> - your trusted partner for premium cleaning and hygiene solutions!</p>
                    
                    <div class="otp-box">
                        <div style="font-size: 14px; color: #666; margin-bottom: 10px;">Your Verification Code</div>
                        <div class="otp-code">{otp}</div>
                        <div class="expiry">⏰ This code will expire in 10 minutes</div>
                    </div>
                    
                    <div class="features">
                        <div class="feature-item">
                            <div class="feature-icon">✅</div>
                            <div>Premium quality cleaning products</div>
                        </div>
                        <div class="feature-item">
                            <div class="feature-icon">🚚</div>
                            <div>Free shipping on orders over ₹999</div>
                        </div>
                        <div class="feature-item">
                            <div class="feature-icon">💎</div>
                            <div>Up to 40% off on first order</div>
                        </div>
                        <div class="feature-item">
                            <div class="feature-icon">🔄</div>
                            <div>Easy returns & 100% satisfaction guarantee</div>
                        </div>
                    </div>
                    
                    <p style="color: #666; font-size: 14px;">Start exploring our range of premium cleaning products:</p>
                    <ul style="color: #666;">
                        <li>🏠 Home Cleaning Essentials</li>
                        <li>🧼 Professional Hygiene Solutions</li>
                        <li>🚿 Bath & Kitchen Care</li>
                        <li>✨ Eco-friendly Products</li>
                    </ul>
                    
                    <p style="color: #999; font-size: 12px; margin-top: 20px;">If you didn't create an account with Wopper, please ignore this email.</p>
                </div>
                <div class="footer">
                    <p>© 2026 Wopper Cleaning Solutions. All rights reserved.</p>
                    <p style="margin-top: 10px;">
                        <a href="#" style="color: #00828a; text-decoration: none;">About Us</a> | 
                        <a href="#" style="color: #00828a; text-decoration: none;">Privacy Policy</a> | 
                        <a href="#" style="color: #00828a; text-decoration: none;">Contact</a>
                    </p>
                    <p>📍 India's Leading Cleaning Products Brand</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        plain_message = f"""
        🧹 Wopper Cleaning Solutions - Email Verification
        
        Hello {first_name or 'Valued Customer'}!
        
        Thank you for joining Wopper - your trusted partner for premium cleaning and hygiene solutions!
        
        Your Verification Code: {otp}
        
        ⏰ This code will expire in 10 minutes
        
        Why join Wopper?
        ✅ Premium quality cleaning products
        🚚 Free shipping on orders over ₹999
        💎 Up to 40% off on first order
        🔄 Easy returns & 100% satisfaction guarantee
        
        Start exploring our range:
        • Home Cleaning Essentials
        • Professional Hygiene Solutions  
        • Bath & Kitchen Care
        • Eco-friendly Products
        
        If you didn't create an account with Wopper, please ignore this email.
        
        © 2026 Wopper Cleaning Solutions. All rights reserved.
        India's Leading Cleaning Products Brand
        """
        
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
            html_message=html_message
        )
        logger.info(f"OTP email sent successfully to {email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send OTP email to {email}: {str(e)}")
        return False


def send_password_reset_email(email, reset_link, first_name=""):
    """Send password reset email - Wopper Cleaning Products"""
    try:
        subject = "Reset Your Password - Wopper Cleaning Solutions 🔐"
        
        html_message = f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: 'Segoe UI', Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f4f4f4;
                }}
                .container {{
                    max-width: 600px;
                    margin: 20px auto;
                    background: white;
                    border-radius: 12px;
                    overflow: hidden;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                }}
                .header {{
                    background: linear-gradient(135deg, #00828a 0%, #00a3ad 100%);
                    padding: 30px;
                    text-align: center;
                }}
                .header h1 {{ color: white; margin: 0; font-size: 28px; }}
                .content {{ padding: 30px; }}
                .reset-box {{
                    background: #f0f8f9;
                    padding: 25px;
                    text-align: center;
                    border-radius: 10px;
                    margin: 25px 0;
                }}
                .reset-button {{
                    display: inline-block;
                    background: #00828a;
                    color: white;
                    padding: 14px 35px;
                    text-decoration: none;
                    border-radius: 50px;
                    font-weight: bold;
                    margin: 10px 0;
                }}
                .warning {{
                    background: #fff3cd;
                    border-left: 4px solid #ffc107;
                    padding: 12px;
                    margin: 20px 0;
                    font-size: 13px;
                }}
                .footer {{
                    background: #f5f5f5;
                    padding: 20px;
                    text-align: center;
                    font-size: 12px;
                    color: #666;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🧹 Wopper Cleaning Solutions</h1>
                    <p>Password Reset Request</p>
                </div>
                <div class="content">
                    <h3>Hello {first_name or 'Valued Customer'}! 👋</h3>
                    
                    <p>We received a request to reset your password for your Wopper account.</p>
                    
                    <div class="reset-box">
                        <p style="margin-bottom: 15px;">Click the button below to create a new password:</p>
                        <a href="{reset_link}" class="reset-button">Reset Password 🔐</a>
                        <p style="margin-top: 15px; font-size: 12px; color: #666;">This link will expire in 24 hours</p>
                    </div>
                    
                    <div class="warning">
                        <strong>⚠️ Security Tip:</strong> Never share this link with anyone. Wopper will never ask for your password via email.
                    </div>
                    
                    <p style="color: #666;">If you didn't request this password reset, please ignore this email or contact our support team.</p>
                    
                    <p style="margin-top: 20px;">Continue exploring our premium cleaning products! ✨</p>
                </div>
                <div class="footer">
                    <p>© 2026 Wopper Cleaning Solutions. All rights reserved.</p>
                    <p style="margin-top: 10px;">Need help? Contact us at support@wopper.com</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        plain_message = f"""
        🔐 Wopper Cleaning Solutions - Password Reset
        
        Hello {first_name or 'Valued Customer'}!
        
        We received a request to reset your password for your Wopper account.
        
        Click this link to reset your password:
        {reset_link}
        
        ⏰ This link will expire in 24 hours
        
        ⚠️ Security Tip: Never share this link with anyone. Wopper will never ask for your password via email.
        
        If you didn't request this password reset, please ignore this email or contact our support team.
        
        Continue exploring our premium cleaning products!
        
        © 2026 Wopper Cleaning Solutions
        Need help? Contact us at support@wopper.com
        """
        
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
            html_message=html_message
        )
        logger.info(f"Password reset email sent successfully to {email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send password reset email to {email}: {str(e)}")
        return False


def send_password_reset_confirmation_email(email, first_name=""):
    """Send password reset confirmation email - Wopper Cleaning Products"""
    try:
        subject = "Password Reset Successful - Wopper Cleaning Solutions ✅"
        
        html_message = f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: 'Segoe UI', Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f4f4f4;
                }}
                .container {{
                    max-width: 600px;
                    margin: 20px auto;
                    background: white;
                    border-radius: 12px;
                    overflow: hidden;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                }}
                .header {{
                    background: linear-gradient(135deg, #00828a 0%, #00a3ad 100%);
                    padding: 30px;
                    text-align: center;
                }}
                .header h1 {{ color: white; margin: 0; font-size: 28px; }}
                .content {{ padding: 30px; text-align: center; }}
                .success-icon {{
                    font-size: 64px;
                    color: #10b981;
                    margin-bottom: 20px;
                }}
                .features {{
                    background: #f9f9f9;
                    padding: 20px;
                    border-radius: 8px;
                    margin: 25px 0;
                    text-align: left;
                }}
                .button {{
                    display: inline-block;
                    background: #00828a;
                    color: white;
                    padding: 14px 35px;
                    text-decoration: none;
                    border-radius: 50px;
                    font-weight: bold;
                    margin: 20px 0;
                }}
                .footer {{
                    background: #f5f5f5;
                    padding: 20px;
                    text-align: center;
                    font-size: 12px;
                    color: #666;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🧹 Wopper Cleaning Solutions</h1>
                    <p>Password Reset Confirmation</p>
                </div>
                <div class="content">
                    <div class="success-icon">✅</div>
                    
                    <h3 style="color: #00828a;">Password Reset Successful!</h3>
                    
                    <p>Hello {first_name or 'Valued Customer'}! 👋</p>
                    
                    <p>Your Wopper account password has been successfully changed.</p>
                    
                    <div class="features">
                        <strong>✨ What's waiting for you:</strong>
                        <ul style="margin-top: 10px;">
                            <li>🛍️ Shop premium cleaning products</li>
                            <li>🎁 Exclusive member discounts up to 40%</li>
                            <li>🚚 Free shipping on orders over ₹999</li>
                            <li>⭐ Early access to new products</li>
                            <li>💎 Loyalty rewards program</li>
                        </ul>
                    </div>
                    
                    <a href="{settings.SITE_URL}/website/login/" class="button">Sign In to Your Account 🧹</a>
                    
                    <p style="color: #666; font-size: 13px; margin-top: 20px;">If you didn't make this change, please contact our support team immediately.</p>
                </div>
                <div class="footer">
                    <p>© 2026 Wopper Cleaning Solutions. All rights reserved.</p>
                    <p>📍 India's Leading Cleaning Products Brand</p>
                    <p style="margin-top: 10px;">❤️ A cleaner home, a happier life!</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        plain_message = f"""
        ✅ Wopper Cleaning Solutions - Password Reset Successful
        
        Hello {first_name or 'Valued Customer'}!
        
        Your Wopper account password has been successfully changed.
        
        ✨ What's waiting for you:
        • Shop premium cleaning products
        • Exclusive member discounts up to 40%
        • Free shipping on orders over ₹999
        • Early access to new products
        • Loyalty rewards program
        
        Sign in to your account: {settings.SITE_URL}/website/login/
        
        If you didn't make this change, please contact our support team immediately.
        
        © 2026 Wopper Cleaning Solutions
        India's Leading Cleaning Products Brand
        A cleaner home, a happier life! 🏠✨
        """
        
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
            html_message=html_message
        )
        logger.info(f"Password reset confirmation email sent successfully to {email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send password reset confirmation email to {email}: {str(e)}")
        return False


def send_welcome_email(email, first_name=""):
    """Send welcome email after successful registration - Wopper Cleaning Products"""
    try:
        subject = "Welcome to Wopper Cleaning Solutions! 🎉"
        
        html_message = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: 'Segoe UI', Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f4f4f4;
                }}
                .container {{
                    max-width: 600px;
                    margin: 20px auto;
                    background: white;
                    border-radius: 12px;
                    overflow: hidden;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                }}
                .header {{
                    background: linear-gradient(135deg, #00828a 0%, #00a3ad 100%);
                    padding: 30px;
                    text-align: center;
                }}
                .welcome-offer {{
                    background: linear-gradient(135deg, #ff6b6b 0%, #ff8e8e 100%);
                    color: white;
                    padding: 20px;
                    text-align: center;
                }}
                .button {{
                    display: inline-block;
                    background: #00828a;
                    color: white;
                    padding: 14px 35px;
                    text-decoration: none;
                    border-radius: 50px;
                    font-weight: bold;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🧹 Welcome to Wopper!</h1>
                    <p>Your journey to a cleaner home begins here</p>
                </div>
                <div class="welcome-offer">
                    <h2>🎁 Welcome Offer!</h2>
                    <p style="font-size: 24px; font-weight: bold;">Get 20% OFF</p>
                    <p>on your first order</p>
                    <p style="font-size: 12px;">Use code: WELCOME20</p>
                </div>
                <div style="padding: 30px;">
                    <h3>Dear {first_name or 'Valued Customer'},</h3>
                    <p>Thank you for choosing Wopper - India's leading cleaning solutions brand!</p>
                    <p>Start exploring our premium products designed to make your home sparkle:</p>
                    <ul>
                        <li>🏠 Home Cleaning Essentials</li>
                        <li>🚿 Bathroom Care Products</li>
                        <li>🍳 Kitchen Cleaning Solutions</li>
                        <li>✨ Eco-friendly Range</li>
                    </ul>
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{settings.SITE_URL}/products/" class="button">Shop Now 🛍️</a>
                    </div>
                </div>
                <div style="background: #f5f5f5; padding: 20px; text-align: center; font-size: 12px;">
                    <p>© 2026 Wopper Cleaning Solutions. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        send_mail(
            subject,
            "Welcome to Wopper Cleaning Solutions!",
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
            html_message=html_message
        )
        logger.info(f"Welcome email sent successfully to {email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send welcome email to {email}: {str(e)}")
        return False