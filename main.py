import json
import cloudscraper
from eth_account import Account
import time

def generate_wallet():
    # Generate a new Ethereum wallet
    acct = Account.create()
    wallet_address = acct.address
    private_key = acct._private_key.hex()  # Use _private_key instead of privateKey
    
    # Return the wallet address and private key
    return wallet_address, private_key

def save_wallet_info(wallet_address, private_key):
    # Read existing wallet info if the file exists
    try:
        with open("wallet_info.json", "r") as f:
            wallet_data = json.load(f)
            # If the loaded data is a dictionary, convert it to a list
            if isinstance(wallet_data, dict):
                wallet_data = [wallet_data]
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file does not exist or is empty, initialize an empty list
        wallet_data = []
    
    # Add the new wallet to the list
    wallet_data.append({"address": wallet_address, "private_key": private_key})

    # Save the updated wallet data back to the file
    with open("wallet_info.json", "w") as f:
        json.dump(wallet_data, f, indent=4)

def claim_airdrop(address):
    url = "https://exchange-airdrop.msu.io/api/gateway/v1/airdrop/address"
    headers = {
        "Origin": "https://exchange-airdrop.msu.io",
        "Referer": "https://exchange-airdrop.msu.io/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123 Safari/537.36",
        "Content-Type": "application/json"
    }
    payload = {
        "upbitAddress": address,
        "isAgree": True,
        "isAgree2": True
    }

    scraper = cloudscraper.create_scraper()
    response = scraper.post(url, headers=headers, json=payload)
    print(f"[{response.status_code}] {response.text}")

if __name__ == "__main__":
    while True:
        # Generate a new wallet address and private key
        wallet_address, private_key = generate_wallet()
        print(f"New wallet generated: Address = {wallet_address}")  # Only print the address
        
        # Save the wallet info to a file
        save_wallet_info(wallet_address, private_key)
        
        # Claim the airdrop using the new wallet address
        claim_airdrop(wallet_address)
        
        # Optionally, wait a few seconds before generating the next wallet (to avoid spamming)
        time.sleep(2)  # Adjust the delay as needed

