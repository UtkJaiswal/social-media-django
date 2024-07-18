# Social Media Application Django

Web application APIs for for social networking using Django Restframework.

## Project Overview

- `User` App

    - User management of APIs for following APIs

        1. `Register` : To register user with unique email and password

        2. `Login` : To login a user with matching credentials and generating token

- `Interaction` App

    - Managements of APIs for following APIs

        1. `GetFriendsList`: To get the list of friends of the Logged in user

        2. `GetSentPendingRequests` : To get the list of sent pending requests ( which are yet not accepted or rejected )

        3. `GetReceivedPendingRequests` : To get the list of receieved requests ( which are yet not accepted or rejected )

        4. `AcceptRequest`: API to accept a pending received request

        5. `SendRequest`: API to send a request to a user

        6. `RejectRequest`: API to reject an already received request

        7. `SearchUser` : For searching a user based on exact matching of email or substring matching of name


## Installation

- Clone the repository

- Jump into the project direcotry

```bash
cd social_media
```

- Create a virtual environment

```bash
python3 -m venv venv
```

- Activate the virtual environment

```bash
source venv/bin/activate
```

- Install the dependencies

```bash
pip install -r requirements.txt
```

## Project Setup

- Run the makemigrations command

```bash
python manage.py makemigrations
```

- Migrate command

```bash
python manage.py migrate
```

- Run the server

```bash
python manage.py runserver
```    
        
