#awsアクセスキー
variable aws_access_key_id {}
variable aws_secret_access_key {}
#Lambda環境変数（twitterAPIアクセスキー・タイムゾーン）
variable twitter_access_token_key {}
variable twitter_access_token_key_secret {}
variable twitter_consumer_key {}
variable twitter_consumer_key_secret {}

#awsプロバイダ情報
provider aws {
    access_key = var.aws_access_key_id
    secret_key = var.aws_secret_access_key
    region = "ap-northeast-1"   
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
}

#EventbridgeからLambda関数の呼び出しを許可
resource aws_lambda_permission allow_cloudwatch {
    statement_id  = "AllowExecutionFromCloudWatch"
    action        = "lambda:InvokeFunction"
    function_name = module.lambda.function_name
    principal     = "events.amazonaws.com"
    source_arn    = module.cloudwatch_event.rule_arn
}
