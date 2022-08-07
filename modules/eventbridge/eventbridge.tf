resource aws_cloudwatch_event_rule event_rule {
    name = "cron-lambda-terraform"
    schedule_expression = "cron(0 11,15 * * ? *)"
}

resource aws_cloudwatch_event_target event_target {
    rule = aws_cloudwatch_event_rule.event_rule.name
    arn  = var.lambda_arn
}

output rule_arn {
    value = aws_cloudwatch_event_rule.event_rule.arn
}