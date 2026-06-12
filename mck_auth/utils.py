# mck_auth/utils.py

from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_otp_email(email, otp, first_name=""):
    """Send OTP email for verification"""
    try:
        subject = "Email Verification - Matrimony Platform"
        
        html_message = f"""
        <html>
        <body style="font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background: linear-gradient(135deg, #ff6b9d 0%, #ff477e 100%); padding: 30px; text-align: center; border-radius: 20px 20px 0 0;">
                    <h2 style="color: white; margin: 0; font-size: 28px;">💖 Matrimony</h2>
                    <p style="color: #ffe0e8; margin: 5px 0 0;">Find Your Perfect Match</p>
                </div>
                <div style="background-color: #fff5f7; padding: 30px; border-radius: 0 0 20px 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                    <h3 style="color: #ff477e; margin-top: 0;">Hello {first_name or 'User'}! 💕</h3>
                    <p style="color: #555;">Thank you for registering with our Matrimony platform! Please use the verification code below to complete your registration:</p>
                    <div style="text-align: center; margin: 30px 0;">
                        <div style="background: linear-gradient(135deg, #ff6b9d 0%, #ff477e 100%); padding: 15px 30px; border-radius: 50px; font-size: 32px; font-weight: bold; letter-spacing: 8px; display: inline-block; color: white; box-shadow: 0 4px 12px rgba(255, 71, 126, 0.3);">
                            {otp}
                        </div>
                    </div>
                    <p style="color: #ff477e; font-weight: bold;">⏰ This code will expire in 10 minutes</p>
                    <p style="color: #777;">If you didn't request this, please ignore this email.</p>
                    <hr style="margin: 20px 0; border-color: #ffd6e4;">
                    <p style="color: #999; font-size: 12px; text-align: center;">© 2024 Matrimony Platform. Find Your Perfect Match 💑</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        plain_message = f"""
        Email Verification - Matrimony Platform
        
        Hello {first_name or 'User'}!
        
        Thank you for registering! Please use the verification code below to complete your registration:
        
        {otp}
        
        This code will expire in 10 minutes.
        
        If you didn't request this, please ignore this email.
        
        © 2024 Matrimony Platform
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
    """Send password reset email to user"""
    try:
        subject = "Password Reset Request - Matrimony Platform 💕"
        
        html_message = f"""
        <html>
        <body style="font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background: linear-gradient(135deg, #ff6b9d 0%, #ff477e 100%); padding: 30px; text-align: center; border-radius: 20px 20px 0 0;">
                    <h2 style="color: white; margin: 0; font-size: 28px;">💖 Password Reset</h2>
                    <p style="color: #ffe0e8; margin: 5px 0 0;">Matrimony Platform</p>
                </div>
                <div style="background-color: #fff5f7; padding: 30px; border-radius: 0 0 20px 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                    <h3 style="color: #ff477e; margin-top: 0;">Hello {first_name or 'User'}! 💕</h3>
                    <p style="color: #555;">We received a request to reset your password. Click the button below to create a new password:</p>
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{reset_link}" style="background: linear-gradient(135deg, #ff6b9d 0%, #ff477e 100%); color: white; padding: 14px 35px; text-decoration: none; border-radius: 50px; display: inline-block; font-weight: bold; box-shadow: 0 4px 12px rgba(255, 71, 126, 0.3);">Reset Password 🔐</a>
                    </div>
                    
                    <p style="color: #ff477e; font-weight: bold;">⏰ This link will expire in 24 hours</p>
                    <p style="color: #777;">If you didn't request this, please ignore this email.</p>
                    <hr style="margin: 20px 0; border-color: #ffd6e4;">
                    <p style="color: #999; font-size: 12px; text-align: center;">© 2024 Matrimony Platform. Find Your Perfect Match 💑</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        plain_message = f"""
        Password Reset Request - Matrimony Platform
        
        Hello {first_name or 'User'}!
        
        We received a request to reset your password. Use this link to create a new password:
        
        {reset_link}
        
        This link will expire in 24 hours.
        
        If you didn't request this, please ignore this email.
        
        © 2024 Matrimony Platform
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
    """Send confirmation email after successful password reset"""
    try:
        subject = "Password Reset Successful - Matrimony Platform ✅"
        
        html_message = f"""
        <html>
        <body style="font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background: linear-gradient(135deg, #ff6b9d 0%, #ff477e 100%); padding: 30px; text-align: center; border-radius: 20px 20px 0 0;">
                    <h2 style="color: white; margin: 0; font-size: 28px;">✅ Password Reset</h2>
                    <p style="color: #ffe0e8; margin: 5px 0 0;">Successfully Updated!</p>
                </div>
                <div style="background-color: #fff5f7; padding: 30px; border-radius: 0 0 20px 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                    <h3 style="color: #ff477e; margin-top: 0;">Hello {first_name or 'User'}! 💕</h3>
                    <p style="color: #555;">Your password has been successfully reset.</p>
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{settings.SITE_URL}/website/login/" style="background: linear-gradient(135deg, #ff6b9d 0%, #ff477e 100%); color: white; padding: 14px 35px; text-decoration: none; border-radius: 50px; display: inline-block; font-weight: bold; box-shadow: 0 4px 12px rgba(255, 71, 126, 0.3);">Sign In Now 💑</a>
                    </div>
                    <p style="color: #ff477e; font-weight: bold;">💝 Welcome back to your journey of finding the perfect match!</p>
                    <p style="color: #777;">If you did not perform this action, please contact our support team immediately.</p>
                    <hr style="margin: 20px 0; border-color: #ffd6e4;">
                    <p style="color: #999; font-size: 12px; text-align: center;">© 2024 Matrimony Platform. Find Your Perfect Match 💑</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        plain_message = f"""
        Password Reset Successful - Matrimony Platform
        
        Hello {first_name or 'User'}!
        
        Your password has been successfully reset.
        
        You can now sign in with your new password.
        
        If you did not perform this action, please contact our support team immediately.
        
        © 2024 Matrimony Platform
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