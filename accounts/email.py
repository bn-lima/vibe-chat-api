from django.core.mail import EmailMessage

def send_reset_token_by_email(email, rese_token):
    url = f"127.0.0.1:8000/account/password/change/?reset_token={rese_token}"

    email_message = EmailMessage(
        subject = "Password Reset",
        body = f"Click the link below to reset your password\n{url}",
        to=[email]
    )
    email_message.send()