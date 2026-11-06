
import json
import urllib.request
from datetime import datetime, timezone

RPC_URL = "https://api.mainnet-beta.solana.com"


def rpc_call(method, params):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params,
    }

    request = urllib.request.Request(
        RPC_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        data = json.load(response)

    if "error" in data:
        raise RuntimeError(data["error"])

    return data["result"]


def get_balance(wallet):
    result = rpc_call("getBalance", [wallet])
    return result["value"] / 1_000_000_000


def get_transactions(wallet, limit=10):
    return rpc_call(
        "getSignaturesForAddress",
        [wallet, {"limit": limit}],
    )


def format_date(timestamp):
    if timestamp is None:
        return "Unknown"

    return datetime.fromtimestamp(
        timestamp, tz=timezone.utc
    ).strftime("%Y-%m-%d %H:%M UTC")


def main():
    print("=== Solana Wallet Tracker V2 ===")
    wallet = input("Enter public Solana wallet address: ").strip()

    if not wallet:
        print("Wallet address is required.")
        return

    try:
        balance = get_balance(wallet)
        transactions = get_transactions(wallet)

        print(f"\nSOL Balance: {balance:.9f} SOL")
        print(f"Recent transactions: {len(transactions)}")

        successful = sum(tx["err"] is None for tx in transactions)
        failed = len(transactions) - successful

        print(f"Successful: {successful}")
        print(f"Failed: {failed}")

        for index, tx in enumerate(transactions, start=1):
            print(f"\nTransaction #{index}")
            print("Date:", format_date(tx.get("blockTime")))
            print("Signature:", tx["signature"])
            print("Slot:", tx["slot"])
            print("Status:", "Failed" if tx["err"] else "Success")

    except Exception as error:
        print("Error:", error)


if __name__ == "__main__":
    main()
