from os.path import abspath
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.functions import col, row_number
from pyspark.sql.window import Window
from delta import *


# setup da aplicação Spark
spark = SparkSession \
    .builder \
    .appName("job-1-spark") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")\
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")\
    .getOrCreate()

# bucket_raw = 's3a://raw-bootcampde-872226808963'
# bucket_processed = 's3://processed-bootcampde-872226808963'
# bucket_curated = 's3a://curated-bootcampde-872226808963'

# definindo o método de logging da aplicação use INFO somente para DEV [INFO,ERROR]
spark.sparkContext.setLogLevel("ERROR")

def read_csv(bucket, path):
    print (f"{bucket}/{path}")
    # lendo os dados do Data Lake
    df = spark.read.format("csv")\
        .option("header", "True")\
        .option("inferSchema","True")\
        .csv(f"{bucket}/{path}")
    # imprime os dados lidos da raw
    print ("\nImprime os dados lidos da raw:")
    print (df.show(5))
    # imprime o schema do dataframe
    print ("\nImprime o schema do dataframe lido da raw:")
    print (df.printSchema())
    return df

def read_delta(bucket, path):
    df = spark.read.format("delta")\
        .load(f"{bucket}/{path}")
    return df

def write_processed(bucket, path, data_format, mode):
    print ("\nEscrevendo os dados lidos da raw para delta na processing zone...")
    try:
        df.write.format(data_format)\
            .mode(mode)\
            .save(f"{bucket}/{path}")
        print (f"Dados escritos na processed com sucesso!")
        return 0
    except Exception as err:
        print (f"Falha para escrever dados na processed: {err}")
        return 1
    
def write_processed_partitioned(bucket, path, col_partition, data_format, mode):
    print ("\nEscrevendo os dados lidos da raw para delta na processing zone...")
    try:
        df.write.format(data_format)\
            .partitionBy(col_partition)\
            .mode(mode)\
            .save(f"{bucket}/{path}")
        print (f"Dados escritos na processed com sucesso!")
        return 0
    except Exception as err:
        print (f"Falha para escrever dados na processed: {err}")
        return 1

def write_curated(bucket, path, dataframe, data_format, mode):
    # converte os dados processados para parquet e escreve na curated zone
    print ("\nEscrevendo os dados na curated zone...")
    try:
        dataframe.write.format(data_format)\
                .mode(mode)\
                .save(f"{bucket}/{path}")
        print (f"Dados escritos na curated com sucesso!")
        return 0
    except Exception as err:
        print (f"Falha para escrever dados na processed: {err}")
        return 1


def write_delta_updates(df, bucket, path, mode):
    print ("\nEscrevendo os dados lidos da raw para delta")
    try:
        df.write.format('delta') \
            .mode(mode) \
            .option("overwriteSchema","true") \
            .save(f"{bucket}/updates/{path}")
        print (f"Dados escritos com sucesso!")
        return df
    except Exception as err:
        print (f"Falha para escrever dados em delta: {err}")
        return None
    
def upsert_tables(spark, table1, table2):
    # load table source, cdc table
    df_table1 = spark.read.format("delta").load(table1)
    df_table2 = spark.read.format("delta").load(table2)
    
    print("\nBefore merge...")
    print("\nTable source...")
    df_table1.show()
    
    print("\nTable updates...")
    df_table2.show()

    # carrega tabelas delta
    deltaTable_1 = DeltaTable.forPath(spark, table1)
    deltaTable_2 = DeltaTable.forPath(spark, table2)
    deltaTable_2 = deltaTable_2.toDF()

    # get the last changed in table by key
    deltaTable_2 = deltaTable_2.withColumn("rn", row_number().over(Window.partitionBy('id').orderBy(col("TIMESTAMP").desc())))
    deltaTable_2 = deltaTable_2.select('*').where('rn=1')
    dfUpdates = deltaTable_2.select("id","Op","name","email","TIMESTAMP")

    deltaTable_1.alias('table1') \
        .merge(
        dfUpdates.alias('table2'),
        'table1.id = table2.id') \
        .whenMatchedDelete(condition="table2.Op ='D'")\
        .whenMatchedUpdateAll(condition="table2.Op ='U'")\
        .whenNotMatchedInsertAll(condition="table2.Op ='I'")\
        .execute()
    
    print("\n printing the table source after merge...")
    df = deltaTable_1.toDF()
    df.show()

bucket_raw = 's3a://raw-bootcampde-872226808963'
bucket_processed = 's3://processed-bootcampde-872226808963'
bucket_curated = 's3a://curated-bootcampde-872226808963'

print ("Dados de customers...\n")

# Ler tabela customers
df_customers = read_delta(bucket_processed,'customers/')
df_customers_update = read_csv(bucket_raw,'public/customers/2023*.csv')
# escreve dados csv para delta
df_customers_update_delta = write_delta_updates(df_customers_update, bucket_processed,"customers","delta","overwrite")

if df_customers_update_delta is not None:
    upsert_tables(spark, df_customers, df_customers_update_delta)
    




# print ("Dados de products...\n")

# # Ler dados da raw
# #df = read_csv(bucket_raw,'public/products/')
# df = read_csv("/home/rodrigo/codes/stack/bootcampde-02/raw/public/customers")

# # Processa os dados e escreve na camada processed
# write_processed(bucket_processed,"products","delta","overwrite")

# # Lear dados da processed...
# print ("Dados lidos da processed em Delta..\n")
# df = read_delta(bucket_processed,"products")

# # Imprime informações sobre a base de dados
# print (df.show())

# print ("Dados de orders...\n")

# # Ler dados da raw
# df = read_csv(bucket_raw,'public/orders/')

# # Processa os dados e escreve na camada processed
# write_processed(bucket_processed,"orders","delta","overwrite")

# # Lear dados da processed...
# print ("Dados lidos da processed em Delta..\n")
# df = read_delta(bucket_processed,"orders")

# # Imprime informações sobre a base de dados
# print (df.show())

# para a aplicação
spark.stop()