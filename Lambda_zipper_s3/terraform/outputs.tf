output "lambda_function_name" {
  value = aws_lambda_function.zip_s3_files.function_name
}

output "cloudwatch_rule" {
  value = aws_cloudwatch_event_rule.daily_trigger.name
}