# バンドリのライブ更新情報の自動ツイートボット
バンドリのHPからライブ情報を1日2回スクレイピングして、更新情報があれば自動でツイートするツール  
実装の詳細については、ブログの以下記事をご覧ください  
Pythonコード解説・インフラ(AWS)のGUIでの構築：https://soramania.com/python-aws-livebot/  
Terraformの実行環境構築：https://soramania.com/wsl2-linux-terraform/  
Terraformコード解説：https://soramania.com/aws-terraform/ 

# ツール全体構成
![Alt text](/overall_structure.png)

# デモ（実際のツイート例）
![Alt text](/demo.png)

# 使用技術
ツール：Python  
インフラ：AWS・Terraform

# 使い方
前提条件
* Linux環境にてTerraformの実行環境が準備できていること
* ツール全体構成に記載の構成を実現するための権限が付与されているAWSアクセスキーが準備できていること
* アクセスレベルがElevatedのTwitterAPIキーが準備できていること

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

## 3.ツール実行
```
sh get_library.sh
terraform init
terraform apply
```

# 注意事項
使い方にも記載しましたが、スクレイピングするためアクセス先のサーバへ負荷がかからないよう、複数回連続しての実行はお控えください  
ツール実行は自己責任でお願いいたします  

# Pythonツールバージョン情報
2022/11/17&emsp;v1.5リリース（スクレイピング後のcp932への文字コード変換の追加）  
2022/11/14&emsp;v1.4リリース（CSV書き込み時のcp932文字コードエラーの対応(ignoreの追加)）  
2022/ 8/14&emsp;v1.3リリース（S3周りの処理効率化）  
2022/ 8/ 6&emsp;v1.2リリース（utf8文字コード変換エラーの対応）  
2022/ 5/ 1&emsp;v1.1リリース（新情報が間に入ったときに対応）  
2022/ 4/29&emsp;v1.0リリース  

# 製作者
桐島 空  
twitter：https://twitter.com/sinri_kirishima
