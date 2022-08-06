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
    handler = "lambda_function.lambda_handler"
    runtime = "python3.8"
    timeout = 15
    filename = data.archive_file.function_source.output_path
    source_code_hash = data.archive_file.function_source.output_base64sha256
    role = var.role_arn
    depends_on = [var.policy, aws_cloudwatch_log_group.lambda_log_group]
}

#CloudWatchLogsグループ定義
resource aws_cloudwatch_log_group lambda_log_group {
    name = "/aws/lambda/${local.function_name}"
}
