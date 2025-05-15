import json
from web3 import Web3

# Konfigurasi
RPC_URL = "https://api.avax.network/ext/bc/C/rpc"
TOKEN_CONTRACT = "0x5E0E90E268BC247Cc850c789A0DB0d5c7621fb59"
ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function"
    }
]

# Inisialisasi Web3 dan Kontrak
w3 = Web3(Web3.HTTPProvider(RPC_URL))
contract = w3.eth.contract(address=w3.to_checksum_address(TOKEN_CONTRACT), abi=ABI)
decimals = contract.functions.decimals().call()

# Baca file wallet_info.json
with open('wallet_info.json') as f:
    wallets = json.load(f)

total_balance = 0

print("=== Hasil Pemindaian Wallet ===\n")

for wallet in wallets:
    address = wallet['address']
    try:
        checksum_address = w3.to_checksum_address(address)
        raw_balance = contract.functions.balanceOf(checksum_address).call()
        human_balance = raw_balance / (10 ** decimals)
        total_balance += human_balance

        print(f"Wallet: {address}")
        print(f"Saldo Token: {human_balance:.4f}\n")
    except Exception as e:
        print(f"Error membaca saldo {address}: {e}\n")

print("=== Akumulasi Total Token ===")
print(f"Total Token dari Semua Wallet: {total_balance:.4f}")

