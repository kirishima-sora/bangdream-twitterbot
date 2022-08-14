#awsアクセスキー
variable aws_access_key_id {}
variable aws_secret_access_key {}
#Lambda環境変数（twitterAPIアクセスキー・タイムゾーン）
variable twitter_access_token_key {}
variable twitter_access_token_key_secret {}
variable twitter_consumer_key {}
variable twitter_consumer_key_secret {}

#Terraformバージョン
terraform {
    required_version = "~> 0.12.5"
}

#プロバイダ情報
provider aws {
    version = "3.37.0"
    access_key = var.aws_access_key_id
    secret_key = var.aws_secret_access_key
    region = "ap-northeast-1"   
}
provider archive {
    version = "2.1.0"
}

#IAM
module iam {
    source = "./modules/iam"
}

#Lambda
module lambda {
    source = "./modules/lambda"
    role_arn = module.iam.lambda_role_arn
    policy = module.iam.lambda_policy
    twi_access_token_key = var.twitter_access_token_key
    twi_access_token_key_secret = var.twitter_access_token_key_secret
    twi_consumer_key = var.twitter_consumer_key
    twi_consumer_key_secret = var.twitter_consumer_key_secret
}

#Eventbridge
module cloudwatch_event {
    source = "./modules/eventbridge"
    lambda_arn = module.lambda.arn
    lambda_function_name = module.lambda.function_name
}

#S3
module s3 {
    source = "./modules/s3"
}

