from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr

from app.core.config import settings
from app.core.logger import logging

logger = logging.getLogger(__name__)

conf = ConnectionConfig(
    MAIL_USERNAME=settings.EMAIL_USERNAME,
    MAIL_PASSWORD=settings.EMAIL_PASSWORD,
    MAIL_FROM=settings.EMAIL_FROM_ADDRESS,
    MAIL_PORT=settings.EMAIL_PORT,
    MAIL_SERVER=settings.EMAIL_HOST,
    MAIL_FROM_NAME=settings.EMAIL_FROM_NAME,
    MAIL_STARTTLS=settings.EMAIL_USE_TLS,
    MAIL_SSL_TLS=settings.EMAIL_USE_SSL,
    USE_CREDENTIALS=bool(settings.EMAIL_USERNAME),
    VALIDATE_CERTS=True,
)

fast_mail = FastMail(conf)


async def send_magic_link_email(email: EmailStr, name: str, magic_link: str, otp_code: str) -> None:
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .container {{
                background-color: #f9f9f9;
                border-radius: 10px;
                padding: 30px;
                text-align: center;
            }}
            .logo {{
                font-size: 24px;
                font-weight: bold;
                color: #333;
                margin-bottom: 20px;
            }}
            .code-box {{
                background-color: #fff;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 20px;
                margin: 20px 0;
                font-size: 32px;
                letter-spacing: 8px;
                font-weight: bold;
                color: #333;
            }}
            .button {{
                display: inline-block;
                background-color: #007bff;
                color: white !important;
                text-decoration: none;
                padding: 12px 30px;
                border-radius: 5px;
                margin: 20px 0;
                font-weight: 500;
            }}
            .button:hover {{
                background-color: #0056b3;
            }}
            .footer {{
                margin-top: 30px;
                font-size: 14px;
                color: #666;
            }}
            .warning {{
                color: #dc3545;
                font-size: 14px;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">Dothe2</div>
            <h2>Hi {name}! 👋</h2>
            <p>You requested to sign in to your Dothe2 account.</p>

            <p><strong>Your verification code is:</strong></p>
            <div class="code-box">{otp_code}</div>

            <p><strong>Or click the button below to sign in instantly:</strong></p>
            <a href="{magic_link}" class="button">Sign In to Dothe2</a>

            <div class="warning">
                ⚠️ This link and code will expire in 15 minutes.<br>
                If you didn't request this, please ignore this email.
            </div>

            <div class="footer">
                <p>Having trouble? Copy and paste this link into your browser:</p>
                <p style="word-break: break-all; font-size: 12px;">{magic_link}</p>
            </div>
        </div>
    </body>
    </html>
    """

    message = MessageSchema(
        subject="Sign in to Dothe2",
        recipients=[email],
        body=html,
        subtype=MessageType.html,
    )

    try:
        await fast_mail.send_message(message)
        logger.info(f"Magic link email sent to {email}")
    except Exception as e:
        logger.error(f"Failed to send email to {email}: {str(e)}")
        raise


async def send_welcome_email(email: EmailStr, name: str) -> None:
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .container {{
                background-color: #f9f9f9;
                border-radius: 10px;
                padding: 30px;
                text-align: center;
            }}
            .logo {{
                font-size: 24px;
                font-weight: bold;
                color: #333;
                margin-bottom: 20px;
            }}
            .button {{
                display: inline-block;
                background-color: #28a745;
                color: white !important;
                text-decoration: none;
                padding: 12px 30px;
                border-radius: 5px;
                margin: 20px 0;
                font-weight: 500;
            }}
            .features {{
                text-align: left;
                margin: 20px 0;
                background-color: #fff;
                padding: 20px;
                border-radius: 8px;
            }}
            .features li {{
                margin: 10px 0;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">Dothe2</div>
            <h1>Welcome to Dothe2, {name}! 🎉</h1>
            <p>We're excited to have you on board. Dothe2 helps you organize your tasks
            efficiently using the Eisenhower Matrix.</p>

            <div class="features">
                <h3>Get started with:</h3>
                <ul>
                    <li>📊 Organize tasks by urgency and importance</li>
                    <li>🎯 Focus on what matters most</li>
                    <li>✅ Track your progress</li>
                    <li>🚀 Boost your productivity</li>
                </ul>
            </div>

            <a href="{settings.BASE_URL}" class="button">Go to Dothe2</a>

            <p style="font-size: 14px; color: #666; margin-top: 30px;">
                Need help? Just reply to this email and we'll be happy to assist!
            </p>
        </div>
    </body>
    </html>
    """

    message = MessageSchema(
        subject="Welcome to Dothe2! 🎉",
        recipients=[email],
        body=html,
        subtype=MessageType.html,
    )

    try:
        await fast_mail.send_message(message)
        logger.info(f"Welcome email sent to {email}")
    except Exception as e:
        logger.error(f"Failed to send welcome email to {email}: {str(e)}")
