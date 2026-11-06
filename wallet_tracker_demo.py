
import json
import urllib.request

RPC_URL = "https://api.mainnet-beta.solana.com"

def recent_transactions(wallet, limit=5):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getSignaturesForAddress",
        "params": [wallet, {"limit": limit}]
    }

    request = urllib.request.Request(
        RPC_URL,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"}
    )

    with urllib.request.urlopen(request, timeout=15) as response:
        result = json.load(response)

    if "error" in result:
        raise RuntimeError(result["error"])

    return result.get("result", [])

if __name__ == "__main__":
    wallet = input("Enter public Solana wallet address: ").strip()

    try:
        transactions = recent_transactions(wallet)
        if not transactions:
            print("No recent transactions found.")

        for tx in transactions:
            print("Signature:", tx["signature"])
            print("Slot:", tx["slot"])
            print("Status:", "Failed" if tx["err"] else "Success")
            print("-" * 30)

    except Exception as error:
        print("Error:", error)
  