# resource "aws_dms_endpoint" "postgresql_endpoint" {
#   endpoint_id                 = "${var.project_name}-endpoint-source-${var.environment}"
#   endpoint_type               = "source"
#   engine_name                 = "postgres"
#   username                    = var.db_username
#   password                    = var.db_password
#   port                        = var.db_port
#   database_name               = aws_db_instance.PostgrelSQL-01.db_name
#   server_name                 = aws_db_instance.PostgrelSQL-01.address
#   ssl_mode                    = "none"
#   depends_on = [aws_s3_bucket.buckets-stack,aws_db_instance.PostgrelSQL-01]
# }

# resource "aws_dms_endpoint" "s3_endpoint" {
#   endpoint_id                 = "${var.project_name}-endpoint-target-${var.environment}"
#   endpoint_type               = "target"
#   engine_name                 = "s3"
#   ssl_mode                    = "none"
#   extra_connection_attributes = "IncludeOpForFullLoad=True;TimestampColumnName=TIMESTAMP;AddColumnName=True"
  
#   s3_settings {
#     bucket_name             = aws_s3_bucket_public_access_block.public_access_block[0].bucket
#     service_access_role_arn = "arn:aws:iam::395882348933:role/Role-DMS-S3-Access"
#     add_column_name = true
#     cdc_path = "cdc"
#     timestamp_column_name = "TIMESTAMP"
#  }
#   depends_on = [aws_s3_bucket.buckets-stack]
# }

# resource "aws_dms_replication_task" "replication-task1" {
#   migration_type            = "full-load"
#   replication_instance_arn  = module.dms.replication_instance_arn
#   replication_task_id       = "${var.project_name}-replication-task-${var.environment}"
#   source_endpoint_arn       = aws_dms_endpoint.postgresql_endpoint.endpoint_arn
#   target_endpoint_arn       = aws_dms_endpoint.s3_endpoint.endpoint_arn
#   #table_mappings            = "{\"rules\":[{\"rule-type\":\"selection\",\"rule-id\":\"1\",\"rule-name\":\"1\",\"object-locator\":{\"schema-name\":\"%\",\"table-name\":\"%\"},\"rule-action\":\"include\"}]}"
#   tags = {
#     Name = "${var.project_name}-replication-task-${var.environment}"
#   }
#   depends_on = [aws_s3_bucket.buckets-stack]
# }

  