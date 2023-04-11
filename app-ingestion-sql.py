import psycopg2
from faker import Faker
import random
from dotenv import load_dotenv
import os

def createTables(cur):
    try:
        # Cria a tabela Customers
        cur.execute("""
        CREATE TABLE Customers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100)
        )
        """)

        # Cria a tabela Products
        cur.execute("""
        CREATE TABLE Products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            category VARCHAR(50),
            price DECIMAL(10,2)
        )
        """)

        # Cria a tabela Orders
        cur.execute("""
        CREATE TABLE Orders (
            id SERIAL PRIMARY KEY,
            customer_id INTEGER REFERENCES Customers(id),
            product_id INTEGER REFERENCES Products(id),
            quantity INTEGER,
            total DECIMAL(10,2),
            status VARCHAR(20)
        )
        """)
        print ("Tabelas criadas com sucesso no banco de dados")
    except Exception as e:
        print (f"Erro ao tentar criar tabelas no banco de dados:{e}")
    return 0

def randomData(cur, conn, numClients):
    try:
        #Insere os clientes na tabela Customers
        customers = []
        for i in range(numClients):
            name = fake.name()
            email = fake.email()
            cur.execute("INSERT INTO Customers (name, email) VALUES (%s, %s)", (name, email))
            customers.append(name)

        conn.commit()
        print ("Dados de usuários gerados com sucesso.")
    except Exception as e:
        print (f"Falha ao tentar gerar dados de usuários: {e}")

    try:
        # Insere os produtos na tabela Products
        products = ['Notebook Acer Aspire 5', 'Smartphone Samsung Galaxy S20', 'Smart TV LG 50 polegadas', 'Mouse Logitech MX Master', 'Fone de Ouvido Sony WH-1000XM4', 'Teclado Mecânico Corsair K95', 'Câmera Digital Canon EOS Rebel T7', 'Headset HyperX Cloud II', 'Monitor Gamer Alienware 34"', 'Tablet Samsung Galaxy Tab S7', 'Caixa de Som Bluetooth JBL Flip 5', 'Impressora HP Deskjet 3755', 'Smartwatch Apple Watch Series 6', 'Drone DJI Mavic Air 2', 'Roçadeira Elétrica Tramontina', 'Notebook Dell Inspiron 15', 'Smartphone Motorola Moto G Power', 'Smart TV Sony 55 polegadas', 'Mouse Pad Gamer Corsair MM300', 'Fone de Ouvido JBL Tune 750BTNC', 'Teclado sem Fio Logitech K780', 'Câmera de Segurança Nest Cam IQ', 'Headset Razer Kraken Tournament', 'Monitor LG UltraWide 29"', 'Tablet Amazon Fire HD 10', 'Caixa de Som Sony SRS-XB43', 'Impressora Epson EcoTank L3150', 'Smartwatch Samsung Galaxy Watch 3', 'Drone DJI Mini 2', 'Aparador de Grama Tramontina', 'Notebook HP Pavilion 15', 'Smartphone Apple iPhone SE', 'Smart TV TCL 50 polegadas', 'Mouse Logitech G502 HERO', 'Fone de Ouvido Bose QuietComfort 35 II', 'Teclado Mecânico Razer BlackWidow Elite', 'Câmera de Ação GoPro HERO9 Black', 'Headset SteelSeries Arctis 7', 'Monitor Dell UltraSharp 27"', 'Tablet Apple iPad Air', 'Caixa de Som JBL Xtreme 3', 'Impressora Brother MFC-L2750DW', 'Smartwatch Fitbit Versa 3', 'Drone DJI Mavic Mini', 'Aspirador de Pó Robô iRobot Roomba i3+', 'Notebook Asus Zenbook UX425', 'Smartphone OnePlus 8T', 'Smart TV Samsung 55 polegadas', 'Mouse Pad Gamer Razer Goliathus', 'Fone de Ouvido Sennheiser Momentum True Wireless 2', 'Teclado sem Fio Logitech K810', 'Câmera Mirrorless Sony Alpha a7 III', 'Headset Astro A50 Wireless', 'Monitor Asus TUF Gaming 24,5"', 'Tablet Microsoft Surface Pro 7', 'Caixa de Som Ultimate Ears BOOM 3', 'Impressora Canon PIXMA TS9120', 'Smartwatch Garmin Venu', 'Drone DJI Phantom 4', 'Lavadora de Alta Pressão Karcher K4', 'Notebook Lenovo IdeaPad 5', 'Smartphone Xiaomi Redmi Note 9 Pro', 'Smart TV LG OLED 55 polegadas', 'Mouse sem Fio Logitech MX Anywhere 2S', 'Fone de Ouvido Jabra Elite 85h', 'Teclado Mecânico HyperX Alloy FPS Pro', 'Câmera de Segurança Arlo Pro 3', 'Headset Turtle Beach Stealth 700', 'Monitor Acer Nitro XV272U']
        categories = ['Eletrônicos', 'Informática', 'Celulares', 'Acessórios']
        for i in range(len(products)):
            name = products[i]
            category = categories[i % len(categories)]
            price = round(random.uniform(50, 1000), 2)
            cur.execute("INSERT INTO Products (name, category, price) VALUES (%s, %s, %s)", (name, category, price))
        conn.commit()
    except Exception as e:
        print (f"Falha ao tentar gerar dados de produtos: {e}")

    try:
        # Insere os pedidos na tabela Orders
        for i in range(len(products)):
            customer_id = random.randint(1, len(customers))
            product_id = random.randint(1, len(products))
            quantity = random.randint(1, 5)
            cur.execute("SELECT price FROM products WHERE id = %s", (product_id,))
            price = cur.fetchone()[0]
            total = round(price * quantity, 2)
            status = random.choice(['Pendente', 'Em andamento', 'Concluído'])
            cur.execute("INSERT INTO Orders (customer_id, product_id, quantity, total, status) VALUES (%s, %s, %s, %s, %s)", (customer_id, product_id, quantity, total, status))
        conn.commit()
    except Exception as e:
        print (f"Falha ao tentar gerar dados de pedidos: {e}")
        
    # Fecha a conexão com o banco de dados
    cur.close()
    conn.close()

# Cria instância da biblioteca Faker
fake = Faker(locale='pt_BR')

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Conecta ao banco de dados PostgreSQL
conn = psycopg2.connect(
    host = os.environ.get('DB_HOST'),
    port = os.environ.get('DB_PORT'),
    database = os.environ.get('DB_NAME'),
    user = os.environ.get('DB_USER'),
    password=os.environ.get('DB_PASSWORD')
)

numClients = int(os.environ.get('numClients'))

# Cria um cursor para executar as instruções SQL
cur = conn.cursor()
createTables(cur)
randomData(cur, conn, numClients)