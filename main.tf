#awsプロバイダ情報
variable aws_access_key_id {}
variable aws_secret_access_key {}
provider aws {
    access_key = var.aws_access_key_id
    secret_key = var.aws_secret_access_key
    region = "ap-northeast-1"   
}

module iam {
    source = "./modules/iam"
}

module lambda {
    source = "./modules/lambda"
    role_arn = module.iam.lambda_role_arn
    policy = module.iam.lambda_policy
}




