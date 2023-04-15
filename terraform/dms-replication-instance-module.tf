# data "aws_partition" "current" {}
# data "aws_region" "current" {}

# module "dms" {
#   source  = "terraform-aws-modules/dms/aws"
#   version = "~> 1.6"

#   # Subnet group
#   repl_subnet_group_name        = var.vpc_group_name
#   repl_subnet_group_description = var.vpc_group_description
#   repl_subnet_group_subnet_ids  = var.subnet_id
  
#   # Instance
#   repl_instance_apply_immediately      = true
#   repl_instance_multi_az               = false
#   repl_instance_class                  = "dms.t3.micro"
#   repl_instance_id                     = "${var.project_name}-dms-instance-${var.environment}"
#   repl_instance_publicly_accessible    = false
#   repl_instance_vpc_security_group_ids = var.security_group_id_list

#   depends_on = [aws_s3_bucket.buckets-stack, aws_db_instance.PostgrelSQL-01]
  
# }