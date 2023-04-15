variable "environment" {
    description = "setup the environment"
}

variable "project_name" {
    description = "Nome do projeto"
}

variable "bucket_names" {
    type = list(string)
}

variable "db_username" {
    type = string
}

variable "db_password" {
    type = string
    sensitive = false
}
variable "db_port" {
    type = string
}

variable "vpc_group_name" {
    type = string
}
variable "vpc_group_description" {
    type = string
}

variable "subnet_id" {
    type = string
}

variable "vpc_id" {
    type = list(string)
}
variable "security_group_id_list" {
    type = list(string)
}


variable "athena_database_name" {
    type = string
}