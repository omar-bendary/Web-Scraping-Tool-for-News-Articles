# Web scraping  module.
This Project is web scraping tool for collecting the articles from different news websites then store them in the database in a structured way to retrieve and control them through APIs
<br/>
<br/>

# Basic functionality
1. Login and Registration.
2. List all stored websites that you scraped with your system ( Website name - Website
link - Created at - Last scraped at - Last scraped by ).
3. Re-scrape a selected website(by passing it ID ) to get the new articles.
4. All scarped data is stored at 'scraped_datasets' folder as JSON files
5. Get all the scraped articles by the website ID (Article title- Article description - Article
DOM - Published at - Article link- Website name), ordered desc by “Published at”.
6. Log each scraping request with whoever sent it and on which website.
7. List the website scraping history (User name - Scraping date)

8. Websites were scrapped:
    1. https://www.mklat.com/category/technology/computer-internet/
    2. https://www.arabmediasociety.com/category/features/

<br/>
<br/>

# Getting started

## Pre-requisites and Local Development

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install packages.

<br/>

### To create a virtual environment


1- Open the project Code folder in Terminal/Windows (PowerShell).

2- Run this command .
```bash
# Windows
> python -m venv .venv
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# macOS
% python3 -m venv .venv
```

### To activate a new virtual environment called .venv:

```bash
# Windows
> .venv\Scripts\Activate.ps1
(.venv) >

# macOS
% source .venv/bin/activate
(.venv) %
```

### To deactivate and leave a virtual environment type deactivate.

```bash
# Windows
(.venv) > deactivate
>

# macOS
(.venv) % deactivate
%
```

### install requirements.txt


Run `pip install requirements.txt`. All required packages are included in the requirements file.

> make sure to activate the virtual environment first
```bash
pip install -r requirements.txt
```

**You might see a WARNING message about updating pip after running these commands. It’s always good to be on the latest version of software and to remove the annoying WARNING message each time you use pip. You can either copy and paste the recommended command or run `python -m pip install --upgrade pip` to be on the latest version.**

```bash
(.venv) > python -m pip install --upgrade pip
```

## Now let’s confirm everything is working by running Django’s internal web server via the runserver command

```bash
(.venv) > python manage.py  makemigrations 
```
```bash
(.venv) > python manage.py  migrate 
```
> Now create the admin user
```bash
(.venv) > python manage.py createsuperuser 
```
Run the surver
```bash
# Windows
(.venv) > python manage.py runserver

# macOS
(.venv) % python3 manage.py runserver
```

## Set up your RDBMS , open your setting.py
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'DB_NAME',
        'USER': 'DB_USER',
        'PASSWORD': 'DB_PASSWORD',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}
```

The application is run on http://127.0.0.1:8000/ by default in the backend configuration.

**Open http://127.0.0.1:8000/ your web browser**

<br/>


# API Reference

## Getting Started
Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:8000/, which is in the backend configuration.

<br/>

## Endpoints
### POST /auth/users
* General:
  * Create a new user.
  * Returns user information if it was created successfully.
* `curl http://127.0.0.1:8000/auth/users/ -X POST -H "Content-Type: application/json" -d '{"username": "testuser","email": "test@gmail.com","password": "MyPassword", "first_name": "test","last_name": "user"}'`

```json
{
    "id": 2,
    "username": "testuser",
    "email": "test@gmail.com",
    "first_name": "test",
    "last_name": "user"
}
```
<br/>

### POST /auth/jwt/create
* General:
  * Login a user to the system by creating access and refresh tokens.
  * Returns user access and refresh tokens (to use it for logging-in) if it was created successfully.
* `curl http://127.0.0.1:8000/auth/jwt/create/ -X POST -H "Content-Type: application/json" -d '{"username": "testuser", "password": "MyPassword"}'`

```json
{
  {
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY2NzY5NTY4NiwianRpIjoiZDI0MzkzNmM0MGFkNDcxMmEyNGI5N2M5YjIxNWI1ZjciLCJ1c2VyX2lkIjoxfQ.J_YiVMoPBuRK0qHSoLoOy8FrnPM0FFydztEu3qQ_Wy8",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY3Njk1Njg2LCJqdGkiOiI5NTY4MGEyNjkyZDg0ZmJhOTlhNzU1NDhkZjQ5ZDc1NyIsInVzZXJfaWQiOjF9.AsdT7UfJTtXlkgKk3Xmhghz3Arz3yytU024wB25w-Nw"
}
}
```

>To keep your user logged-in , use an extention like [Moheader](https://modheader.com/)

- - - -
<br/>

### GET /api/websites
* General:
  * Returns a list of all stored websites that you scraped with your system ( Website name - Website
link - Created at - Last scraped at - Last scraped by )
* Sample: `curl http://127.0.0.1:8000/api/websites/`

```json
[
    {
        "id": 1,
        "name": "Arab Media & Society",
        "link": "https://www.arabmediasociety.com/",
        "created_at": "November 04, 2022 - (09:56) PM",
        "last_scraped_at": "November 04, 2022 - (09:56) PM",
        "last_scraped_by": {
            "username": "omarbendary"
        }
    },
    {
        "id": 2,
        "name": "موقع مقالات Mklat.com",
        "link": "https://www.mklat.com",
        "created_at": "November 04, 2022 - (03:14) PM",
        "last_scraped_at": "November 04, 2022 - (03:14) PM",
        "last_scraped_by": {
            "username": "omarbendary"
        }
    }
]
```
<br/>

### GET /api/articles
* General:
  * Returns a list of all the scraped articles by the website ID (Article title- Article description - Article DOM - Published at - Article link- Website name), ordered desc by “Published at”
* Sample: `curl http://127.0.0.1:8000/api/articles/`
> The following json is a sample 3 articles out of 82(total articles scraped)
```json
[
    {
        "title": "The Use of Twitter by Saudi Sports Clubs to Increase Fan Interaction (Arabic)",
        "description": "Scroll down for Arabic abstract. This study seeks to determine how Saudi sports clubs can use Twitter to increase fan participation and interaction. The forms of the provided content and its vitality were analyzed to determine whether there is a relationship between fans’ interaction and types of content and whether …",
        "DOM": "<article class=\"post-listing post-7942 post type-post status-publish format-standard has-post-thumbnail category-features category-uncategorized tag-netography tag-participation tag-sentiment-analysis tag-social-networks tag-sports-marketing wl_entity_type-article post_issue-issue-33-winter-spring-2022 ams_post_type-peer-reviewed-scholarship\" id=\"the-post\">",
        "published_at": "October 01, 2022",
        "link": "https://www.arabmediasociety.com/the-use-of-twitter-by-saudi-sports-clubs-to-increase-fan-interaction/",
        "website": {
            "name": "Arab Media & Society",
            "link": "https://www.arabmediasociety.com/"
        }
    },
    {
        "title": "Hate Speech Between Arab Sports Fans on Social Media (Arabic)",
        "description": "Scroll down for Arabic abstract. This study sought to monitor the hate speech between Arab sports fans on social media. The researcher relied on both discourse and content analysis to analyze 41,505 comments that were published on the Egyptian Al-Ahly Club page on Facebook about the 2018 African Champions League …",
        "DOM": "<article class=\"post-listing post-7946 post type-post status-publish format-standard has-post-thumbnail category-culture-society category-features category-scholarship tag-hate-speech tag-impoliteness-model tag-social-media tag-sports-fans wl_entity_type-article post_issue-issue-33-winter-spring-2022 ams_post_type-peer-reviewed-scholarship\" id=\"the-post\">",
        "published_at": "October 01, 2022",
        "link": "https://www.arabmediasociety.com/hate-speech-between-arab-sports-fans-on-social-media/",
        "website": {
            "name": "Arab Media & Society",
            "link": "https://www.arabmediasociety.com/"
        }
    },
    {
        "title": "The Effects on User Attention of Using Multimedia Features on Arabic Sports Websites: A Quasi-Experimental Study (Arabic)",
        "description": "Scroll down for Arabic abstract. Multimedia capacity is one of the most important aspects of the website design industry, particularly with respect to sports, which is characterized by a large audience of followers operating on two levels, the method of content production and presentation, and the general appearance of the …",
        "DOM": "<article class=\"post-listing post-7950 post type-post status-publish format-standard has-post-thumbnail category-features category-scholarship tag-multimedia tag-visual-attention tag-visual-perception tag-website-design wl_entity_type-article post_issue-issue-33-winter-spring-2022 ams-featured-features ams_post_type-peer-reviewed-scholarship\" id=\"the-post\">",
        "published_at": "October 01, 2022",
        "link": "https://www.arabmediasociety.com/the-effects-on-user-attention-of-using-multimedia-features-on-arabic-sports-websites-a-quasi-experimental-study/",
        "website": {
            "name": "Arab Media & Society",
            "link": "https://www.arabmediasociety.com/"
        }
    },
    
   
]
```

### GET /api/scraping_history
* General:
  * Returns a list of all the websites scraping history (User name - Scraping date)
* Sample: `curl http://127.0.0.1:8000/api/scraping_history/`

```json
[
    {
        "name": "Arab Media & Society",
        "scrape_history": [
            {
                "scraped_at": "November 04, 2022 - (02:00) PM",
                "user": {
                    "username": "omarbendary"
                }
            },
            {
                "scraped_at": "November 04, 2022 - (02:15) PM",
                "user": {
                    "username": "omarbendary"
                }
            },
            {
                "scraped_at": "November 04, 2022 - (09:56) PM",
                "user": {
                    "username": "omarbendary"
                }
            }
        ]
    },
    {
        "name": "موقع مقالات Mklat.com",
        "scrape_history": [
            {
                "scraped_at": "November 04, 2022 - (02:00) PM",
                "user": {
                    "username": "omarbendary"
                }
            },
            {
                "scraped_at": "November 04, 2022 - (02:12) PM",
                "user": {
                    "username": "omarbendary"
                }
            },
            {
                "scraped_at": "November 04, 2022 - (02:29) PM",
                "user": {
                    "username": "omarbendary"
                }
            },
            {
                "scraped_at": "November 04, 2022 - (03:14) PM",
                "user": {
                    "username": "omarbendary"
                }
            }
        ]
    }
]
```
<br/>

### POST /api/re-scrape
* General:
  * re-scrape a selected website(by passing it ID ) to get the new articles.
  * Log each scraping request with whoever sent it and on which website.
  * Returns success = true if  it was re-scraped successfully.
  * Returns success = false  if it wasn't re-scraped successfully.
* `curl http://127.0.0.1:8000/api/re-scrape/1/`

```json
{
    "success": true
}
```

* Errors :
    * Returns status = false if you passed non-existent website id.
* `curl http://127.0.0.1:8000/api/re-scrape/9/`
```json
{
    "status": false
}
```

<br/>

# Deployment N/A

<br/>

# Authors
Omar Bendary