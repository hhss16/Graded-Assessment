# Instructions to run this project

Please make sure you have pip and pipenv installed first. 

```sh
git clone https://github.com/hhss16/GradedAssessment
cd GradedAssessment
pipenv shell
pipenv install 
python manage.py makemigrations 
python manage.py migrate
python manage.py runserver
```

## Djoser is required

`pipend install djoser`

## changes in settings.py file 

```python 
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework.authtoken',
    'LittleLemonDRF',
    'djoser'
]

```

and 

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
}
```

## Create super admin user

```
python manage.py createsuperuser
```

## Create other users

Now login to Django admin panel at `http://127.0.0.1:8000/admin/` as admin and create two users and generate their tokens

![Tokens](https://res.cloudinary.com/dpebhamdp/image/upload/v1667839615/Labs/GradedAssessment/django-admin-tokens_jyly6x.png)


## Ratings Endpoint 
You can access `http://127.0.0.1:8000/api/ratings` to display all ratings

![Ratings](https://res.cloudinary.com/dpebhamdp/image/upload/v1667839615/Labs/GradedAssessment/display-ratings_ayqeu8.png)


## Rate an item
Send a POST request to `http://127.0.0.1:8000/api/ratings` with `menuitem_id` and `rating` (must be 0 to 5) and add a user token 

**Form Data**
![Form Data](https://res.cloudinary.com/dpebhamdp/image/upload/v1667839615/Labs/GradedAssessment/add-rating-as-adrian_rxbmzz.png)

**Token**
![User Token](https://res.cloudinary.com/dpebhamdp/image/upload/v1667839615/Labs/GradedAssessment/add-rating-adrian-user-token_uuduvx.png)


## Multiple submission creates errors (successful validation)

![Validation](https://res.cloudinary.com/dpebhamdp/image/upload/v1667839615/Labs/GradedAssessment/user-cannot-rate-same-item-twice_qybcmg.png)


## Files 

* 7 lines in the views.py file - https://github.com/hhss16/GradedAssessment/blob/main/LittleLemonDRF/views.py
* 20 lines in the serializers.py file - https://github.com/hhss16/GradedAssessment/blob/main/LittleLemonDRF/serializers.py
* 4 lines in the models.py file - https://github.com/hhss16/GradedAssessment/blob/main/LittleLemonDRF/models.py



