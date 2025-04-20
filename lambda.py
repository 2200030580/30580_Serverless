import boto3
import os

waf = boto3.client('wafv2', region_name='Asia Pacafic (Mumbai)')  # Change region if needed

IP_SET_NAME = 'MyIpset'
IP_SET_SCOPE = 'REGIONAL'  # 'CLOUDFRONT' if used with CloudFront
IP_SET_ID = '7fd9447d-4b9a-42f0-b720-15838ae6102a'  # get this from your WAF console

def lambda_handler(event, context):
    ip_to_block = event['ip']  # Expected input via event
    print(f"Blocking IP: {ip_to_block}")

    # Get current IP set addresses
    response = waf.get_ip_set(
        Name=IP_SET_NAME,
        Scope=IP_SET_SCOPE,
        Id=IP_SET_ID
    )
    
    addresses = response['IPSet']['Addresses']
    lock_token = response['LockToken']

    cidr_ip = ip_to_block + "/32"
    if cidr_ip in addresses:
        return {'message': f"IP {ip_to_block} already blocked."}

    addresses.append(cidr_ip)

    # Update IP set
    waf.update_ip_set(
        Name=IP_SET_NAME,
        Scope=IP_SET_SCOPE,
        Id=IP_SET_ID,
        Addresses=addresses,
        LockToken=lock_token
    )

    return {'message': f"Successfully blocked IP: {ip_to_block}"}
