### Deploying the Site

#### Creating the Heroku App
* On the Heroku dashboard at the top righthand side select the New button and then Create new app.
* Give the app a name and select the most appropriate location then select create app.

#### Configuring the Heroku App
* From the menu at the top of the page select the Resources tab.
* In the Add-ons box on the resources tab search for Postgres and select Heroku Postgres selecting the free plan before confirming.
* From the menu at the top of the page select the settings tab.
* Under Config Vars select Reveal Config Vars. The DATABASE_URL should already be listed.
* Add any other required environment variables. Below is a list of those required for this project and if appropriate where they can be found.
    * AWS_ACCESS_KEY_ID - AWS CSV file (see below).
    * AWS_SECRET_ACCESS_KEY - AWS CSV file (see below).
    * EMAIL_HOST_PASS - password provided by email client.
    * EMAIL_HOST_USER - sites email address.
    * SECRET_KEY - random key, can be generated online.
    * STRIPE_PUBLIC_KEY - on the Stripe dashboard developers tab under API keys.
    * STRIPE_SECRET_KEY - on the Stripe dashboard developers tab under API keys.
    * STRIPE_WH_SECRET - on the Stripe dashboard developers tab under Webhooks, the signing secret can be viewed when the specific endpoint is selected.
    * USE_AWS - set to true when using AWS (see below).

#### Setting up AWS

**Creating the Bucket**
* At the top of tha AWS Management Console search for and select 'S3'.
* Click 'Create Bucket', give it a name associated with the Heroku app name and select the most appropriate location.
* Under Object Ownership select 'ACLs enabled' and 'Bucket owner preferred'
*  Untick 'Block all public access' and acknowledge this choice.
* Then select 'Create Bucket'

**Bucket Settings**
* On the properties tab in the 'Static Website Hosting' option at the bottom select 'Use this bucket to host a website' and fill in some default index and error document values.
* On the permissions tab in the Cross-origin resource sharing section paste in the following:
    ```
    [
        {
            "AllowedHeaders": [
                "Authorization"
            ],
            "AllowedMethods": [
                "GET"
            ],
            "AllowedOrigins": [
                "*"
            ],
                "ExposeHeaders": []
        }
    ]

    ```
* In the bucket policy section on the permissions tab select 'Policy Generator' and select the following options in the generator page:
    * Policy type - S3 Bucket Policy
    * Add Statement(s) - Pricipal: *, Actions: GetObject, ARN: copy from bucket policy section.
    * Select 'Add Statement' then 'Generate Policy' copy the policy and paste into the bucket policy editor adding /* to the end of the resource key.
* In the 'Access Control List' section on the permissions tab click edit and enable 'List' for 'Everyone'.

**Identity and Access Management (IAM)**
* In the services search box search for and select IAM.
* On the sidebar select User Groups and Create Group. Choose a name associated with the S3 Bucket name and select Create Group.
* On the sidebar select Policies and Create Policy.
* Go to the JSON tab and select import managed policy and select and import AmazonS3FullAccess.
* Paste the bucket policy ARN from the s3 Bucket policy page into a list in the resource option (see below):
    ```
    "Resource": [
        "{PASTED ARN}",
        "{PASTED ARN}/*"
    [
    ```
* Click Next then Review policy giving it a name and description before selecting create policy.
* In the sidebar select User Groups. Select the group just created.
* On the permissions tab open the Add permissions dropdown and click Attach policies.
* Select the policy and click Add permissions at the bottom.
* On the sidebar select Users then Add User give it a name and select 'Programmatic access' for the 'Access Type' option.
* Select next and add the user to the recently created group.
* Click through to the end and select Create User.
* Download and save the CSV file. The AWS config vars can be found in here.

#### Configuring the Django Settings
* In the workspace terminal install the Gunicorn web server:
    ```
    pip3 install gunicorn
    ```
* In the workspace terminal install the libraries required by the database:
    ```
    pip3 install dj_database_url psycopg2
    ```
* In the workspace terminal install boto3 for the AWS configuration:
    ```
    pip3 install boto3
    ```
* In the workspace terminal install django storages for the AWS configuration:
    ```
    pip3 install django-storages
    ```
* Add the installs to the requirements.txt file
    ```
    pip3 freeze --local > requirements.txt
    ```
* Add storages to the INSTALLED_APPS in the Django settings file.
* Create an env.py file in the top level of the directory and add the following variables to the file:
    * SECRET_KEY
    * STRIPE_PUBLIC_KEY
    * STRIPE_SECRET_KEY
    * STRIPE_WH_SECRET
    * DEVELOPMENT (set to true)
    * DATABASE_URL (comment out until required)
* At the top of the django settings file import os and import dj_database_url.
* At the top of the django settings file add the following if statement to use the env.py file in the development environment:
    ```
    if os.path.isfile('env.py'):
        import env
    ````
* Add the database to databases section in the Django settings file keeping the original database details for development:
    ```
    if 'DATABASE_URL' in os.environ:
        DATABASES = {
            'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
        }
    else:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
    ```
* Replace the SECRET_KEY setting in the Django settings file with:
    ```
    SECRET_KEY = os.environ.get('SECRET_KEY')
    ```
* When ready to deploy, save required model objects to JSON fixtures files:
    ```
    python3 manage.py dumpdata app_name > filename.json
    ```
* Migrate the models to the database first ensuring that the 'DATABASE_URL' variable in the env file is uncommented for the migrations:
    ```
    python3 manage.py migrate
    ```
* Create the model objects from the JSON fixtures files:
    ```
    python3 manage.py loaddata filename.json
    ```
* Create a superuser for the app:
    ```
    python3 manage.py createsuperuser
    ```
* Add the Heroku Hostname to the ALLOWED_HOSTS setting in the Django settings file:
    ```
    ALLOWED_HOSTS = ['jewellery-art.herokuapp.com', 'localhost']
    ```
* Set DEBUG to False except for in development in the settings file:
    ```
        DEBUG = 'DEVELOPMENT' in os.environ
    ```
* Add a Procfile containing the following code in the top level of the directory:
    ```
    web: gunicorn jewellery_art.wsgi
    ```
* For AWS add the following settings to the settings file:
    ```
    if 'USE_AWS' in os.environ:
        # Bucket Config
        AWS_STORAGE_BUCKET_NAME = 'jewellery-art'
        AWS_S3_REGION_NAME = 'eu-west-2'
        AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
        AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

        # Static and media files
        STATICFILES_STORAGE = 'custom_storages.StaticStorage'
        STATICFILES_LOCATION = 'static'
        DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'
        MEDIAFILES_LOCATION = 'media'

        # Override static and media URLs in production
        STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATICFILES_LOCATION}/'
        MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIAFILES_LOCATION}/'
    ```
* Add a custom_storages.py file to the top level of the directory with the following code:
    ```
    """ Custom storages for AWS file storage. """
    from django.conf import settings
    from storages.backends.s3boto3 import S3Boto3Storage


    class StaticStorage(S3Boto3Storage):
        """ Custom static file storage location. """
        location = settings.STATICFILES_LOCATION


    class MediaStorage(S3Boto3Storage):
        """ Custom media file storage location. """
        location = settings.MEDIAFILES_LOCATION
    ```
* To set-up the site to send email add the following settings to the settings file (settings based on gmail account, check individual email client documentation for how to set-up and get the values required):
    ```
    if 'DEVELOPMENT' in os.environ:
        EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
        DEFAULT_FROM_EMAIL = 'jewellery-art@example.com'
    else:
        EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
        EMAIL_USE_TLS = True
        EMAIL_PORT = 587
        EMAIL_HOST = 'smtp.gmail.com'
        EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
        EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASS')
        DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_HOST_USER')
    ```
* In the terminal add, commit and push all changes.

#### Deploying the App
    * In Heroku select the deploy tab from the menu at the top.
    * Select GitHub as the deployment method and browse and connect to the correct repository.
    * Under manual deploy select the main branch and the select deploy branch.

### Forking the GitHub Repository

The following steps can be used to fork the GitHub repository:
* On GitHub navigate to the main page of the repository.
* The 'Fork' button can be found on the top righthand side of the screen.
* Click the button to create a copy of the original repository.

### Add cloning section?