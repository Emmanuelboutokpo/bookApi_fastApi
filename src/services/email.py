import resend
from src.config import settings

resend.api_key = settings.resend_api_key

def send_otp_email(email: str, otp: str):
    params = {
        "from": "onboarding@resend.dev", 
        "to": email,
        "subject": "Votre code de vérification",
        "html": f"<strong>Votre code OTP est : {otp}</strong>. Il expire dans 10 minutes.",
    }
    resend.Emails.send(params)

def send_confirmation_email(email: str, name: str):
    params = {
        "from": "onboarding@resend.dev",
        "to": email,
        "subject": "Bienvenue chez BookReview !",
        "html": f"""
            <h1>Félicitations {name} !</h1>
            <p>Votre compte est désormais vérifié. Vous pouvez maintenant consulter et noter vos livres préférés.</p>
        """,
    }
    resend.Emails.send(params)



def send_reset_password_email(email: str, token: str):
    print(f"Envoi de l'email de réinitialisation à {email} avec le token {token}")
    # Remplace l'URL par celle de ton frontend
    reset_link = f"http://127.0.0.1:8000/docs#/default/forgot_password_api_v1_reset_password?token={token}"
    
    html_content = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 10px;">
        <h2 style="color: #333; text-align: center;">Réinitialisation de votre mot de passe</h2>
        <p>Bonjour,</p>
        <p>Vous avez demandé à réinitialiser votre mot de passe pour votre compte <strong>BookReview</strong>.</p>
        <p>Cliquez sur le bouton ci-dessous pour choisir un nouveau mot de passe. Ce lien est valable pendant <strong>30 minutes</strong>.</p>
        
        <div style="text-align: center; margin: 30px 0;">
            <a href="{reset_link}" 
               style="background-color: #007bff; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block;">
               Réinitialiser mon mot de passe
            </a>
        </div>
        
        <p style="color: #666; font-size: 0.9em;">Si vous n'avez pas demandé cette modification, vous pouvez ignorer cet email en toute sécurité.</p>
        <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
        <p style="color: #999; font-size: 0.8em; text-align: center;">L'équipe BookReview</p>
    </div>
    """
    
    resend.Emails.send({
        "from": "onboarding@resend.dev", # À remplacer par ton domaine vérifié
        "to": email,
        "subject": "Réinitialisation de mot de passe - BookReview",
        "html": html_content
    })