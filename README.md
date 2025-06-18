# get-awssg-info

## 概要
AWSのセキュリティグループの情報のうち使用状況と関連付けされたリソースをCSVで出力するプログラムです。

## 使い方
### AWS CloudShellで以下のコマンドを実行
aws ec2 describe-security-groups --output json > all_security_groups.json

### 「security_groups_list.py」にjsonを読みこませ、jsonからセキュリティグループ一覧をCSVに出力
~ $ python security_groups_list.py all_security_groups.json security_groups_output.csv

### 「describe_sg_interfaces.py」にCSVを読み込ませ、使用状況と関連付けされたリソースをCSVで出力
~ $ python describe_sg_interfaces.py security_groups_output.csv sg-interface-output.csv
