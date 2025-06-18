# get-awssg-info  
## 概要  
AWSのセキュリティグループ情報をCSVで出力するプログラムです。  

## 使い方  
①AWS CloudShellで以下のコマンドを実行  
aws ec2 describe-security-groups --output json > all_security_groups.json  
  
②「security_groups_list.py」にjsonを読みこませ、jsonからセキュリティグループ一覧をCSVに出力  
~ $ python security_groups_list.py all_security_groups.json security_groups_output.csv  
  
③「describe_sg_interfaces.py」にCSVを読み込ませ、使用状況と関連付けされたリソースをCSVで出力  
~ $ python describe_sg_interfaces.py security_groups_output.csv sg-interface-output.csv  
