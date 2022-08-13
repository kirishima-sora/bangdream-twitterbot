# バンドリのライブ更新情報の自動ツイートボット
バンドリのHPからライブ情報を1日2回スクレイピングして、更新情報があれば自動でツイートするツール  
実装の詳細については、ブログの以下記事をご覧ください  
Pythonコード・インフラ(AWS)構成：https://soramania.com/python-aws-livebot/  
Terraform環境構築：https://soramania.com/wsl2-linux-terraform/  
Terraformコード：https://soramania.com/aws-terraform/ 

# ツール全体構成
![Alt text](/overall_structure.png)

# デモ（実際のツイート例）
![Alt text](/demo.png)

# 使用技術
ツール：Python  
インフラ：AWS・Terraform

# 使い方
手順や前提条件が多いため、あくまで自分用のメモです  
前提条件
* Linux環境にてTerraformの実行環境が準備できていること

WindowsでのLinux+Terraformの環境構築について、冒頭のブログをご参考ください  
また、コード実行にあたってはAWSとTwitterAPIのアクセスキー等が必要になります  
※実行する場合は、アクセス先のサーバへ負荷がかからないよう、複数回連続しての実行はお控えください  
　ツール実行は自己責任でお願いいたします  

## 1.クローン作成
```
git clone https://github.com/kirishima-sora/bangdream-twitterbot
```

## 2.terraform.tfvarsに必要情報の記載  
* AWSアクセスキー等  
* twitterAPIアクセスキー等

## 3.S3バケットの作成、ファイル配置  
* バケットを作成  
* 作成したバケット配下にtest_csvフォルダにあるbandre-event-old.csvを配置  
* 作成したバケット配下にoldlist-csvフォルダを作成

## 4.app/lambda_function.pyの編集  
* 変数bucket_nameを作成したバケット名に変更

## 5.ツール実行
```
sh get_library.sh
terraform init
terraform apply
```

# 注意事項
使い方にも記載しましたが、スクレイピングするためアクセス先のサーバへ負荷がかからないよう、複数回連続しての実行はお控えください  
ツール実行は自己責任でお願いいたします  

# Pythonツールバージョン情報
2022/ 8/14&emsp;v1.3リリース（S3周りの処理効率化）
2022/ 8/ 6&emsp;v1.2リリース（utf8文字コード変換エラーの対応）  
2022/ 5/ 1&emsp;v1.1リリース（新情報が間に入ったときに対応）  
2022/ 4/29&emsp;v1.0リリース  

# 製作者
桐島 空  
twitter：https://twitter.com/sinri_kirishima
