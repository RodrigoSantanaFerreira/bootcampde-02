resource "aws_security_group" "access-rds-port" {
  name        = "access_rds"

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    
    # Please restrict your ingress to only necessary IPs and ports.
    # Opening to 0.0.0.0/0 can lead to security vulnerabilities.
    cidr_blocks = ["0.0.0.0/0"]

  }
  tags = {
    security_group = "access-rds-port"
  }
}

resource "aws_db_instance" "PostgrelSQL-01" {
  db_name              = "coins"
  engine               = "postgres"
  engine_version       = "13.7"
  instance_class       = "db.t3.micro"
  username             = var.db_username
  password             = var.db_password
  skip_final_snapshot  = true
  
  # resource identifier
  identifier = "${var.project_name}-rds-database-${var.environment}"
  
  # Storage options
  allocated_storage    = 50
  max_allocated_storage = 100
  
  # allow remotly access
  vpc_security_group_ids = [aws_security_group.access-rds-port.id]
  publicly_accessible = "true"
}

# print information
output "address_endpoint" {
    value = aws_db_instance.PostgrelSQL-01.address
}
output "db_user_admin" {
    value = aws_db_instance.PostgrelSQL-01.username
}
output "instance_port" {
    value = aws_db_instance.PostgrelSQL-01.port
}