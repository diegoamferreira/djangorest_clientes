# API com Django 3: Validações, buscas, filtros e deploy

https://cursos.alura.com.br/course/api-django-3-validacoes-buscas-filtros-deploy

* How to validate fields in your API using Django Rest Framework
* Understand how to add filters, searches, and sorting to your endpoints
* Create a good architecture in your Django Rest API projects
* Put your API online by deploying it
* Discover how to create your own APIs with Django

* [Python 3.9.13](https://www.python.org/)
* [Django 4.1.5](https://www.djangoproject.com/)
* [Django Rest Framework 3.14.0](https://www.django-rest-framework.org/)

## How to run the project?

* clone this repository.
* Create a virtualenv with Python 3.
* Active virtualenv.
* install dependencies.
* Run migrations.

```
git clone https://github.com/diegoamferreira/djangorest_clientes.git
cd djangorest_clientes
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Django
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Populate client tables with fake clients

run `python populate_script.py`

## Django Rest Framework

[Django REST framework](https://www.django-rest-framework.org/) is a powerful and flexible toolkit for building Web
APIs.

* The Web browsable API is a huge usability win for your developers.
* Authentication policies including packages for OAuth1a and OAuth2.
* Serialization that supports both ORM and non-ORM data sources.
* Customizable all the way down - just use regular function-based views if you don't need the more powerful features.
* Extensive documentation, and great community support.
* Used and trusted by internationally recognised companies including Mozilla, Red Hat, Heroku, and Eventbrite.

## What did I learn here??

___

### Validators

All validators used in Django models will be used in serializers, but custom validators can also be created directly in
serializers.

```
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

    def validate_cpf(self, cpf):
        if len(cpf) != 11:
            raise serializers.ValidationError("O CPF deve ter 11 dígitos")
        return cpf

    def validate_nome(self, nome):
        if not nome.isalpha():
            raise serializers.ValidationError("Não inclua números neste campo")
        return nome

    def validate_rg(self, rg):
        if len(rg) != 9:
            raise serializers.ValidationError("O RG deve ter 9 dígitos")
        return rg

    def validate_celular(self, celular):
        if len(celular) < 11:
            raise serializers.ValidationError("O Celular deve ter 11 dígitos")
        return celular
```

The above sample shows a custom serializer validation for the CPF field. It checks if the length of the CPF is 11. To
create a custom validation, the method must follow the template **validate_**`field`, with the word "field" being
replaced by the name of the field being validated.

We should create a new file for validators to improve the architecture.

### Using Validators from pip module

`pip install validate-docbr`

```
from validate_docbr import CPF

cpf = CPF()

# Validar CPF
cpf.validate("012.345.678-90")  # True
cpf.validate("012.345.678-91")  # False
```

```
# validators.py
def cpf_valido(cpf):
    cpf_validator = CPF()

    # Validar CPF
    return cpf_validator.validate(cpf)  # True


def nome_valido(nome):
    return nome.isalpha()


def rg_valido(rg):
    return len(rg) == 9


def celular_valido(celular):
    """Check cell number using regex"""
    modelo = r'[0-9]{2} [0-9]{5}-[0-9]{4}'
    pattern = re.compile(modelo)
    return bool(pattern.match(celular))

```

```
# serializers.py
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

    def validate(self, data):
        if not cpf_valido(data['cpf']):
            raise serializers.ValidationError({'cpf': 'CPF Inválido'})
        if not nome_valido(data['nome']):
            raise serializers.ValidationError({'nome': 'O Nome não pode conter números'})
        if not rg_valido(data['rg']):
            raise serializers.ValidationError({'rg': 'O RG deve ter 9 dígitos'})
        if not celular_valido(data['celular']):
            raise serializers.ValidationError({'celular': 'Número de celular inválido, padrão: 12 12345-1234'})
        return data

```

We've changed the logic of validators. Now they return True if the value is valid and False if it's not valid. We import
these functions into the serializers and use each validator by passing the field value as a parameter.

___

## Script Populate Clients

```
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangorest2.settings')
django.setup()

from faker import Faker
from validate_docbr import CPF
import random
from clientes.models import Cliente


def criando_pessoas(quantidade_de_pessoas):
    fake = Faker('pt_BR')
    Faker.seed(10)
    for _ in range(quantidade_de_pessoas):
        cpf = CPF()
        nome = fake.name()
        email = '{}@{}'.format(nome.lower(), fake.free_email_domain())
        email = email.replace(' ', '')
        cpf = cpf.generate()
        rg = "{}{}{}{}".format(random.randrange(10, 99),
                               random.randrange(100, 999),
                               random.randrange(100, 999),
                               random.randrange(0, 9))
        celular = "{} 9{}-{}".format(random.randrange(10, 21),
                                     random.randrange(4000, 9999),
                                     random.randrange(4000, 9999))
        ativo = random.choice([True, False])
        p = Cliente(nome=nome, email=email, cpf=cpf, rg=rg, celular=celular, ativo=ativo)
        p.save()


criando_pessoas(200)
```

___

## Pagination

You can easily set a default pagination for REST views adding the following code in the `settings.py`:

```
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```

This will return json as:

```
{
"count": 400,
"next": "http://127.0.0.1:8000/clientes/?format=json&page=2",
"previous": null,
"results": [...]
}
```

___

## Ordering

Just set the `ordering_fields` in the view, just like in the admin class.

```
class ClientesViewSet(viewsets.ModelViewSet):
    """Listando clientes"""
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    ordering_fields = ['nome']
```

___

We can set `filter_backends` in view to allow the client to choose the sort order, ascending or descending.

```
class ClientesViewSet(viewsets.ModelViewSet):
    """Listando clientes"""
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['nome']
```

* Ascending = `http://127.0.0.1:8000/clientes/?ordering=nome`
* Descending = `http://127.0.0.1:8000/clientes/?ordering=-nome`

___


## Filtering

### Search filter
```
filter_backends = [filters.OrderingFilter, filters.SearchFilter]
search_fields = ['nome', 'cpf']
```

* nome - `http://127.0.0.1:8000/clientes/?search=vitor`
* cpf - `http://127.0.0.1:8000/clientes/?search=vitor`

### DjangoFilterBackend
We can use the `django-filter` library to allow the client to choose the sort order, ascending or descending.
```
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['ativo']
```
By setting the `filterset_fields`, we can specify which fields can be used as filters.
* url: `http://127.0.0.1:8000/clientes/?ativo=false`
