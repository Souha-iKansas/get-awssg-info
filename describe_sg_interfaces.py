import csv
import subprocess
import json
import argparse
import re

def describe_network_interfaces(sg_id):
    try:
        result = subprocess.run(
            ["aws", "ec2", "describe-network-interfaces", "--filters", f"Name=group-id,Values={sg_id}"],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error describing interfaces for {sg_id}: {e}")
        return None

def get_resource_info(interface, sg_id):
    description = interface.get("Description", "")
    attachment = interface.get("Attachment", {})
    instance_id = attachment.get("InstanceId", "")
    eni_id = interface.get("NetworkInterfaceId", "")
    private_ip = interface.get("PrivateIpAddress", "")
    status = interface.get("Status", "unknown")
    vpc_id = interface.get("VpcId", "Unknown")
    name = ""
    
    # ネットワークインターフェースのNameタグを探す
    for tag in interface.get("TagSet", []):
        if tag.get("Key") == "Name":
            name = tag.get("Value")
            break
    
    resource_type = "Unknown"
    resource_id = eni_id  # default fallback

    # 判定ロジック
    if instance_id:
        resource_type = "EC2"
        resource_id = instance_id
    elif "ClientVPN Endpoint resource" in description:
        resource_type = "ClientVPN"
        match = re.search(r"cvpn-endpoint-[a-z0-9]+", description)
        if match:
            resource_id = match.group(0)
    elif "ELB" in description:
        resource_type = "ELB"
    elif "NAT Gateway" in description:
        resource_type = "NAT Gateway"
    elif "Transit Gateway" in description:
        resource_type = "Transit Gateway"

    # セキュリティグループ名を取得
    sg_name = ""
    for group in interface.get("Groups", []):
        if group.get("GroupId") == sg_id:
            sg_name = group.get("GroupName", "")
            break

    return private_ip, eni_id, status, resource_type, resource_id, vpc_id, name, sg_name

def main():
    parser = argparse.ArgumentParser(description="Check SG usage and output details to CSV")
    parser.add_argument("input_csv", help="Input CSV file with sg-ids (header required)")
    parser.add_argument("output_csv", help="Output CSV file")
    args = parser.parse_args()

    with open(args.input_csv, newline="") as infile, open(args.output_csv, mode="w", newline="") as outfile:
        reader = csv.reader(infile)
        next(reader)  # ヘッダー読み飛ばし
        writer = csv.writer(outfile)
        writer.writerow([
            "sg_id", "sg_name", "private_ip", "eni_id", "status", 
            "resource_type", "resource_id", "vpc_id", "name"
        ])

        for row in reader:
            if not row or not row[0].startswith("sg-"):
                continue
            sg_id = row[0]
            data = describe_network_interfaces(sg_id)
            if not data or "NetworkInterfaces" not in data:
                continue

            interfaces = data["NetworkInterfaces"]
            if not interfaces:
                writer.writerow([sg_id, "", "", "", "not-attached", "None", "", "", ""])
            else:
                for interface in interfaces:
                    private_ip, eni_id, status, resource_type, resource_id, vpc_id, name, sg_name = get_resource_info(interface, sg_id)
                    writer.writerow([
                        sg_id, sg_name, private_ip, eni_id, status, 
                        resource_type, resource_id, vpc_id, name
                    ])

if __name__ == "__main__":
    main()
