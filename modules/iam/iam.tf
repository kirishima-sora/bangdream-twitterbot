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
data aws_iam_policy s3_full_access {
    arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

#IAMロールへのIAMポリシーのアタッチ
resource aws_iam_role_policy_attachment lambda_basic_execution {
    role = aws_iam_role.lambda_role.name
    policy_arn = data.aws_iam_policy.lambda_basic_execution.arn
}
resource aws_iam_role_policy_attachment s3_access {
    role = aws_iam_role.lambda_role.name
    policy_arn = data.aws_iam_policy.s3_full_access.arn
}

#Lambdaで使用する値のアウトプット
output lambda_role_arn {
    value = aws_iam_role.lambda_role.arn
}
output lambda_policy {
    value = aws_iam_role_policy_attachment.s3_access
}
