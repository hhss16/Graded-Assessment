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

## Models

All models are created in the `LittleLemonDRF/models.py` file

If you want to turn off order item details in the `orders` endpoint, then remove the `related_name=order` from this model

```python
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order')
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('order', 'menuitem')

```

## Serializers 

All serializers are in the `LittleLemonDRF/serializers.py` file. The `UserSerializer` class was userd to display the users (Managers and Delivery crews)

## Available URLs

## Using / Running this project

Follow these steps to run this project. 

### Groups 
Create a superuser and then log into Django admin panel and create the following groups

* Manager
* Delivery Crew

### Users
create a few random users and assign them randomly in these two groups> Also create token for each of these users from the admin panel for later use


## Create categories and menu items 

Login as admin and access the following endppoints to create categories and menu items. You can use both browsable API view or a RESt client with admin/manager token
 * http://127.0.0.1:8000/api/categories
 * http://127.0.0.1:8000/api/menu-items

## Cart

Add items to cart by visiting this endpoint, or sending POST request with token

* http://127.0.0.1:8000/api/cart/menu-items
