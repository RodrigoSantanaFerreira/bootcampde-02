from os.path import abspath
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# setup da aplicação Spark
spark = SparkSession \
    .builder \
    .appName("job-1-spark") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")\
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")\
    .getOrCreate()

# definindo o método de logging da aplicação use INFO somente para DEV [INFO,ERROR]
spark.sparkContext.setLogLevel("ERROR")

def read_csv(bucket, path):
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
            .option("mergeSchema", "true")\
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

bucket_raw = 's3a://raw-bootcampde-872226808963'
bucket_processed = 's3://processed-bootcampde-872226808963'
bucket_curated = 's3a://curated-bootcampde-872226808963'

print ("Dados de customers...\n")
# Ler dados da raw
df = read_csv(bucket_raw,'public/customers/')

# Processa os dados e escreve na camada processed
write_processed(bucket_processed,"customers","delta","overwrite")

# Lear dados da processed...
print ("Dados de customers lidos da processed em Delta..\n")
df = read_delta(bucket_processed,"customers")

# Imprime informações sobre a base de dados
print (df.show())

print ("Dados de products...\n")

# Ler dados da raw
df = read_csv(bucket_raw,'public/products/')

# Processa os dados e escreve na camada processed
write_processed(bucket_processed,"products","delta","overwrite")

# Lear dados da processed...
print ("Dados lidos da processed em Delta..\n")
df = read_delta(bucket_processed,"products")

# Imprime informações sobre a base de dados
print (df.show())

print ("Dados de orders...\n")

# Ler dados da raw
df = read_csv(bucket_raw,'public/orders/')

# Processa os dados e escreve na camada processed
write_processed(bucket_processed,"orders","delta","overwrite")

# Lear dados da processed...
print ("Dados lidos da processed em Delta..\n")
df = read_delta(bucket_processed,"orders")

# Imprime informações sobre a base de dados
print (df.show())

# para a aplicação
spark.stop()