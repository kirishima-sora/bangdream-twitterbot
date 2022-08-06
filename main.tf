
#awsプロバイダ情報
variable "aws_access_key_id" {}
variable "aws_secret_access_key" {}
provider aws {
    access_key = var.aws_access_key_id
    secret_key = var.aws_secret_access_key
    region = "ap-northeast-1"   
}

#IAM
#信頼ポリシー(lambdaがこのロールを受け取れるようにする)
data aws_iam_policy_document assume_role {
    statement {
        actions = ["sts:AssumeRole"]
        effect  = "Allow"
        principals {
            type = "Service"
            identifiers = ["lambda.amazonaws.com"]
        }
    }
}

#IAMロールの作成
resource aws_iam_role lambda_role {
    name = "MyLambdaRole"
    assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

#IAMポリシー（AWSLambdaBasicExecutionRole）
data aws_iam_policy lambda_basic_execution {
    arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

#IAMロールへのIAMポリシーのアタッチ
resource aws_iam_role_policy_attachment lambda_basic_execution {
    role = aws_iam_role.lambda_role.name
    policy_arn = data.aws_iam_policy.lambda_basic_execution.arn
}



#lambda
#定数定義
locals {
    function_name  = "terraform_bangdre_function"
}

#lambda実行ファイル定義
data archive_file function_source {
    type = "zip"
    source_dir = "app"
    output_path = "archive/lambda.zip"
}

#lambda作成
resource aws_lambda_function function {
    function_name = local.function_name
    handler = "lambda.lambda_handler"
    runtime = "python3.8"
    filename = data.archive_file.function_source.output_path
    source_code_hash = data.archive_file.function_source.output_base64sha256
    role = aws_iam_role.lambda_role.arn
    # environment {
    #     variables = {
    #         BASE_MESSAGE = "Hello"
    #     }
    # }
    depends_on = [aws_iam_role_policy_attachment.lambda_basic_execution, aws_cloudwatch_log_group.lambda_log_group]
}

#CloudWatchLogsグループ定義
resource aws_cloudwatch_log_group lambda_log_group {
    name = "/aws/lambda/${local.function_name}"
}

