# Bootcamp de Engenharia de Dados

## Setup AWS

1. Crie uma conta na AWS (Conta root);
2. Crie uma conta com permissão de `administrador` para ser a conta usada para projeto;
3. Crie um servidor PostgreSQL **na versão 13** usando o Amazon RDS;
4. Clique no Security Groupo e libere o acesso a porta 5432 vindo do seu ip público;


## Setup Ingestion to RDS

1. Edite o arquivo `.env` com as informções do Amazon RDS;
2. Instale todas as bibliotecas necessárias para rodar a aplicação de ingestão com o comando:
```
pip install -r requirements.txt
```
3. Execute a aplicação `app-ingestion-sql`
4. Conecte no banco de dados usando algum cliente de banco de dados, por exemplo o *dbeaver* e verifique se as tabelas foram criadas.

## Setup Ingestion to Data Lake
1. Edite o arquivo .env informando as credencias de chave de acesso, por exemplo:

```console
AWS_ACCESS_KEY_ID=AKIA4WFGE4SB25sdfadf
AWS_SECRET_ACCESS_KEY=mwXXs8NjLwI83fnxrZ7rm4zsQHEftY3adfafd
```
2. Crie um bucket na aws, no meu caso criei *raw-bootcampde-872226808963*
3. Edit o arquivo .env informando o nome do bucket criado na variável BUCKET_NAME
4. Execute a aplicação `app-mobile-customers.py`
5. Verifique se os arquivos .json estão sendo inseridos no bucket.

**Importante**:
- Interrompa o banco de dados RDS.


- DMS Setup

1. Crie uma instância de replicação.
2. Crie os endpoints target e source.
3. Use o código abaixo para criar a police/role para o endpoint target no s3.
4. Documentação do s3 como target endpoint: https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.S3.html

```console
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:DeleteObject",
                "s3:PutObjectTagging"
            ],
            "Resource": [
                "arn:aws:s3:::raw-bootcampde-872226808963/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::raw-bootcampde-872226808963"
            ]
        }
    ]
}
```
5. Adicione a opção `AddColumName` no endpoint target.
6. Crie uma task para iniciar o DMS.


## Setup EMR

1. Libere o acesso na porta 22. Para isso clique em `EC2 security group` clique no security group e libere a porta 22 para o IP.

Acesso via ssh com Putty:

*   1. Download PuTTY.exe to your computer from: https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html 
    2. Start PuTTY.
    3. In the Category list, choose Session.
    4. In the Host Name field, enter hadoop@ec2-52-23-204-207.compute-1.amazonaws.com
    5. In the Category list, expand Connection > SSH and then choose Auth.
    6. For private key file for authentication, choose Browse and select the private key file (key-boot02.ppk) that you used to launch the cluster.
    7. Select Open.
    8. Select Yes to dismiss the security alert.
*

2. Copie a aplicação para o servidor do Amazon EMR usando o WinScp (Windows) ou o scp (linux), para linux segue um exemplo:

```console
scp -i ~/Downloads/pair-bootcamp.pem job-spark-app-emr-redshift.py hadoop@ec2-54-90-3-194.compute-1.amazonaws.com:/home/hadoop/
```

3. Para executar o cluster Spark use o comando abaixo:

```console
spark-submit --packages io.delta:delta-core_2.12:2.0.0 --conf "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension" --conf "spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog" app-spark-processing.py
```

## Crawlers

- Usar os data catalog com o caminho o URI do objeto: `s3://teste-872226808963/orders/`
- *Sempre usar a barra no final para informar o data store.*
- Usar Natives tables

## Athena
- **Importante**: Alterar o engine para usar athena 3.0 (tabelas delta)
- Utilize o arquivo `querys.sql` para consultar as tabelas diretamente no Athena.

### Setup Athena + Power BI

Configuração do DSN
1 - Baixar o drive ODBC no site: Conectar-se ao Amazon Athena com ODBC - Amazon Athena

![Alt text](athena/Site%20da%20aws%20para%20baixar%20drive.PNG)

1.1 - Escolha o drive conforme o sitema operacional:

![Alt text](athena/Baixar%20drive%20de%20acordo%20com%20o%20SO.PNG)

2 – Instalar o drive baixado.

![Alt text](athena/Instala%C3%A7%C3%A3o%20do%20drive.PNG)

3 – No Windows pesquise "Odbc" no menu iniciar, depois clique em em Fonte de dados ODBC > DSN de sistema > Adicionar

![Alt text](athena/criando%20uma%20nova%20fonte%20de%20dados.PNG)

4 – Clique em *DNS do Sistema*, depois escolha o Simba Athena ODBC drive

![Alt text](athena/Adicionando%20um%20novo%20DSN.PNG)

5 – Configurar o Simba com os dados solicitados

![Alt text](athena/configurando%20o%20dsn.PNG)

6 – Configurar as opções de autenticação

![Alt text](athena/op%C3%A7%C3%B5es%20de%20autentica%C3%A7%C3%A3o.PNG)

Obtendo dados do Athena no Power BI

1 – No Power BI, em obter dados, selecionar o conector ODBC

![Alt text](athena/escolhendo%20o%20conector%20ODBC.PNG)

2 – Escolher o DSN configurado

![Alt text](athena/configurando%20o%20dsn.PNG)

3 – Escolher as tabelas desejadas

![Alt text](athena/escolhendo%20as%20tabelas%20para%20serem%20utilizadas%20no%20power%20bi.PNG)

![Alt text](athena/dados%20dispon%C3%ADveis%20para%20uso%20no%20power%20bi.PNG)

## Delta tables

 - Enforcement Schema
 ```
 ALTER TABLE public.customers ADD sexo varchar NULL;
 ALTER TABLE public.orders ADD setor varchar NULL;
 ALTER TABLE public.products ADD estoque_id varchar NULL;
 ```

- Para trabalhar com alteração de schemas em tabelas delta use:
- *mergeSchema* para atualizações em tabelas.
- *overwriteSchema* para sobrescrever todo o schema de uma tabela.

```console
.option("mergeSchema", "true")\
.option("overwriteSchema", "true")\
```

## Terraform

- Instale o aplicativo aws-cli
1. Faça o download aqui conforme o seu sistema operacional: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
2. Se estiver usando Windows instale com o seguinte comando:

```console
msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi
```
3. Feche o VSCode e abra novamente para o terminal encontrar o `aws` app no terminal.

4. abra o terminal e digite:
aws configure

5. entre com as credenciais, exemplo:
*ACCESS_KEY: AKIA4WFGE4SBSIJOBTdd
SECRET_KEY: 1qNX6PCP+g3RzjFank+nRKnLiIDMkYQfQMDcMdfx*

6. Para validar que as credenciais da AWS deram certo execute o comando:
aws s3 ls

7. Deve listar os buckets da conta.

## Terraform - Infraestrutura como Código

0. Antes de fazer o setup do terraform crie um bucket para ser nosso bucket de backend.

1. Após criar o bucket, edite o arquivo *backend.tf* informando o nome do bucket criado. Exemplo:
*
terraform {
  backend "s3" {
    # Edit the bucket name and region
    bucket         = "stack-terraform-backend-872226808963"
    key            = "global/s3/terraform.tfstate"
    region         = "us-east-1"
  }
}*

## Instalando o Terraform

1. Faça o download aqui: https://developer.hashicorp.com/terraform/downloads

2. extraia o binário do terraform dentro da pasta "terraform".

3. Execute o comando para inicializar o terraform e fazer o setup do bucket para o backend

```console
terraform init
```

4. Execute o comando abaixo para planejar os recursos a serem criados:

```console
terraform plan
```

5. Execute o comando abaixo para fazer deploy de todos os recursos:

```console
terraform apply
```

6. Execute o comando abaixo para fazer remover toda infraestrutura criada:

```console
terraform destroy
```

