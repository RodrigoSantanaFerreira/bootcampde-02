from datetime import datetime
from decimal import Decimal
import json
import time
import boto3
from faker import Faker
import os
from dotenv import load_dotenv

# Edite a quantidade de eventos a serem gerados
numEvents = 100

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Define classe de codificação personalizada
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(CustomEncoder, self).default(obj)


# Cria instância da biblioteca Faker
fake = Faker(locale='pt_BR')

# Obtém as credenciais da AWS a partir das variáveis de ambiente
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

# Configura as credenciais de acesso à conta da AWS
s3 = boto3.resource('s3', aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key)

# Define o nome do bucket S3

bucket_name = os.environ.get('BUCKET_RAW')

# Define lista de páginas do aplicativo
pages = [
    'home',
    'products',
    'product_details',
    'cart',
    'checkout',
    'profile'
]

# Define lista de ações do usuário
actions = [
    'view_page',
    'click_link',
    'add_to_cart',
    'remove_from_cart',
    'checkout',
    'purchase'
]

# Gera eventos aleatórios do usuário
for i in range(numEvents):
    # Define dados do usuário
    user_data = {
        'id': fake.random_int(min=1, max=100),
        'name': fake.name(),
        'sex': fake.random_element(elements=('Male', 'Female')),
        'address': fake.address(),
        'ip': fake.ipv4(),
        'state': fake.state(),
        'latitude': fake.latitude(),
        'longitude': fake.longitude()
    }

    # Define dados do evento
    event_data = {
        'timestamp': int(time.time()),
        'page': fake.random_element(elements=pages),
        'action': fake.random_element(elements=actions),
        'product_id': fake.random_int(min=1, max=100),
        'quantity': fake.random_int(min=1, max=5),
        'estoque_id': fake.random_int(min=1, max=100),
        'price': Decimal(str(round(fake.pyfloat(left_digits=2, right_digits=2, positive=True), 2))),
        'estoque_id_number': fake.random_int(min=10, max=100),
        'price': Decimal(str(round(fake.pyfloat(left_digits=2, right_digits=2, positive=True), 2)))
    }
    
    # Combina dados do usuário e do evento em um único objeto
    data = {
        'user': user_data,
        'event': event_data
    }

    # Escreve dados em um arquivo JSON localmente
    now = datetime.now()
    frt_date = now.strftime("%d_%m_%Y_%H_%M_%S")

    with open(f"event_customers_mobile{i}_{frt_date}.json", "w") as f:
        time.sleep(1)
        json.dump(data, f, cls=CustomEncoder)

    # # Salva os dados em arquivos json no bucket S3
    #time.sleep(3)
    s3.Object(bucket_name, f"event_customers_mobile{i}_{frt_date}.json").put(Body=json.dumps(data, cls=CustomEncoder))