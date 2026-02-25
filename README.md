# Vibe Chat API

Backend de chat feito em Django + DRF.  
Atualmente implementa apenas **autenticação de usuários**.

## Funcionalidades

- Registro de usuários
- Login com token
- Logout (invalida token)
- Reset de senha via email

## Endpoints

- POST `/account/register/` → criar conta  
- POST `/account/login/` → login e retorna token  
- DELETE `/account/logout/` → logout (invalida token)  
- POST `/account/password/change/` → atualizar senha com reset token  
- POST `/account/password/change/forgot/` → solicitar reset de senha  
- POST `/account/password/change/request/` → criar token de reset via usuário logado

## Instalação

```bash
git clone https://github.com/bn-lima/vibe-chat-api.git
cd vibe-chat-api
python -m venv myvenv
source myvenv/bin/activate  # Windows: .\myvenv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
