# バンドリのライブ更新情報の自動ツイートボット
バンドリのHPからライブ情報を1日2回スクレイピングして、更新情報があれば自動でツイートするツール  
実装の詳細については、ブログの以下記事をご覧ください  
Pythonコード・インフラ(AWS)構成：https://soramania.com/python-aws-livebot/  
Terraform環境構築：https://soramania.com/wsl2-linux-terraform/  
Terraformコード：（作成中）  

# デモ（実際のツイート例）
（ツイート例の画像はgithubに挙げて貼る予定）

# 使用技術
ツール：Python  
インフラ：AWS・Terraform

# 使い方
前提として、Linux環境にてTerraformの実行環境が準備できていることとします  
WindowsでのLinux+Terraformの環境構築について、冒頭のブログをご参考ください  
また、コード実行にあたってはAWSアクセスキー・TwitterAPIのアクセスキー・コンシューマーキーが必要になります  
※実行する場合は、アクセス先のサーバへ負荷がかからないよう、複数回連続しての実行はお控えください  
　ツール実行は自己責任でお願いいたします  

1. クローン作成
```bash
git clone https://github.com/kirishima-sora/bangdream-twitterbot
```

2. terraform.tfvarsに必要情報の記載
AWSアクセスキー等  
twitterAPIアクセスキー等

3. ツール実行
```bash
sh get_library.sh
terraform init
terraform apply
```

# 注意事項
使い方にも記載しましたが、スクレイピングするため、アクセス先のサーバへ負荷がかからないよう、複数回連続しての実行はお控えください  
ツール実行は自己責任でお願いいたします  

# バージョン情報
2022/ 8/ 6  v1.2リリース（utf8文字コード変換エラーの対応）  
2022/ 5/ 1  v1.1リリース（新情報が間に入ったときに対応）  
2022/ 4/29  v1.0リリース  

# 製作者
桐島 空  
twitter：https://twitter.com/sinri_kirishima
