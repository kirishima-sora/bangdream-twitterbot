#EventBridge
#ルール作成
resource aws_cloudwatch_event_rule event_rule {
    name = "cron-lambda-terraform"
    schedule_expression = "cron(0 11,15 * * ? *)"
}

#Lambdaアクセス権限付与
resource aws_cloudwatch_event_target event_target {
    rule = aws_cloudwatch_event_rule.event_rule.name
    arn  = var.lambda_arn
}

#EventbridgeとLambda関数への結び付け
resource aws_lambda_permission allow_cloudwatch {
    statement_id  = "AllowExecutionFromCloudWatch"
    action = "lambda:InvokeFunction"
    function_name = var.lambda_function_name
    principal = "events.amazonaws.com"
    source_arn = aws_cloudwatch_event_rule.event_rule.arn
}