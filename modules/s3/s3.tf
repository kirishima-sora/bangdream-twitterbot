#S3
#バケット作成
resource aws_s3_bucket bucket {
    bucket = "bangdream-eventlist-terraform"
    acl    = "private"
    versioning {
        enabled = false
    }
}

#デモ実施時のみ
resource aws_s3_bucket_object csv_upload {
    bucket = aws_s3_bucket.bucket.id
    key    = "bandre-event-old.csv"
    source = "./test_csv/bandre-event-old.csv"
}

