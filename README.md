# Vibe Chat API

Este projeto é o backend de uma aplicação de chat com autenticação, perfis de usuário e salas de conversa em tempo real. A API foi desenvolvida com Django, Django REST Framework e Channels, e oferece tanto endpoints HTTP quanto comunicação via WebSocket.

## O que a aplicação faz

- Cadastro e autenticação de usuários
- Login com geração de token de autenticação
- Logout que invalida o token do usuário
- Recuperação de senha por email
- Gerenciamento de perfil do usuário
- Criação, entrada, saída e exclusão de salas de chat
- Envio de mensagens em salas específicas
- Comunicação em tempo real entre usuários conectados
- Busca de salas por nome ou assunto

## Estrutura do projeto

- accounts: autenticação, modelo de usuário personalizado, tokens e recuperação de senha
- account_profile: perfil do usuário com foto, descrição, nome exibido e dados extras
- chat: modelos de salas e mensagens, validações, listagens e WebSocket
- vibe_chat: configuração principal do projeto, URLs e setup do ASGI

## Principais rotas

### Autenticação

- POST /account/register/
- POST /account/login/
- DELETE /account/logout/
- POST /account/password/change/
- POST /account/password/change/forgot/
- POST /account/password/change/request/

### Chat

- GET /chatroom/rooms/
- GET /chatroom/public/
- GET /chatroom/myrooms/
- POST /chatroom/new/
- GET /chatroom/<id>/detail/
- POST /chatroom/<id>/join/
- POST /chatroom/<id>/leave/
- DELETE /chatroom/<id>/delete/
- POST /chatroom/<id>/send/

### Perfil

- GET /profile/<id>/detail/
- POST /profile/edit/

## Tecnologias principais

- Django
- Django REST Framework
- Channels
- Daphne
- Redis
- PostgreSQL
- Pillow

## Requisitos locais

- Python 3.x
- Redis rodando localmente
- PostgreSQL configurado
- Ambiente virtual recomendado

## Como rodar o projeto

1. Crie e ative um ambiente virtual

```bash
python -m venv myvenv
source myvenv/bin/activate
```

2. Instale as dependências

```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente

Crie um arquivo .env na raiz do projeto com os dados do banco PostgreSQL:

```env
DB_NAME=seu_banco
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432
```

4. Aplique as migrações

```bash
python manage.py migrate
```

5. Inicie o Redis e rode a aplicação

```bash
redis-server
python manage.py runserver
```

Para o fluxo de chat em tempo real, o Redis precisa estar disponível, pois o projeto utiliza o Channels com Redis como camada de mensagens.

## Observações

O projeto ainda está em desenvolvimento e usa uma configuração básica para ambiente local. Para produção, é recomendável revisar itens como segurança, secret key, DEBUG, armazenamento de mídia e configuração de email.
