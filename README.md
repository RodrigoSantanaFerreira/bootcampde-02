# Bootcamp de Engenharia de Dados

## Setup AWS

1. Crie uma conta na AWS (Conta root);
2. Crie uma conta com permissão de `administrador` para ser a conta usada para projeto;
3. Crie um servidor PostgreSQL usando o Amazon RDS;
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
