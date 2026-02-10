from tonsdk.contract.wallet import Wallets, WalletVersionEnum
from tonsdk.crypto import mnemonic_new
from tonsdk.utils import bytes_to_b64str, to_nano

from aiohttp import request
from decimal import Decimal


class BlockchainsGateway:
    def __init__(self, key: str):
        self.url = "https://testnet.toncenter.com/api/v2/"
        self.key = key

    async def getWalletInformation(self, walletHash: str) -> dict:
        params = {"address": walletHash, "api_key": self.key}
        async with request("GET", f"{self.url}getWalletInformation", params=params) as resp:
            response = await resp.json()
            if not (resp.ok):
                raise Exception(f"Failed to getWalletInformation with {walletHash} : {response}")
            
            return response
    
    async def getBalance(self, wallet: str):
        params = {"address": wallet, "api_key": self.key}
        async with request("GET", f"{self.url}getAddressBalance", params=params) as resp:
            resp = (await resp.json())["result"]
            return Decimal(f"{resp}") * (Decimal("10") ** -9)
    
    async def generateWallet(self) -> dict[str,str]:
        mnemonics, publickKey, secretKey, wallet = Wallets.from_mnemonics(
            version=WalletVersionEnum.v4r2, mnemonics=mnemonic_new()
        )

        walletHash = wallet.address.to_string(
            is_user_friendly=True,
            is_url_safe=True,
            is_bounceable=False,
            is_test_only=True
        )
        return {"walletHash": walletHash, "mnemonics": mnemonics}
    
    async def deployWallet(self, walletHash: str, mnemonics: list[str]) -> int:
        mnemonics, publickKey, secretKey, wallet = Wallets.from_mnemonics(
            version=WalletVersionEnum.v4r2, mnemonics=mnemonics
        )

        message = bytes_to_b64str(
            wallet.create_init_external_message()["message"].to_boc(False)
        )

        headers={"Content-Type": "application/json"}
        payload = {"boc": message}

        async with request("POST", f"{self.url}sendBoc?api_key={self.key}", json=payload, headers=headers) as resp:
            response = await resp.json()
            if not (resp.ok):
                raise Exception(f"Deploy failed with {walletHash}: {response}")

            return response
        
    async def sendTransfer(self, walletHash: str, mnemonics: list[str], destination: str, quantum: Decimal) -> int:
        mnemonics, publickKey, secretKey, wallet = Wallets.from_mnemonics(
            version=WalletVersionEnum.v4r2, mnemonics=mnemonics
        )

        walletInformation = await self.getWalletInformation(walletHash)

        query = wallet.create_transfer_message(
            destination, to_nano(str(quantum), "ton"), walletInformation["result"]["seqno"]
        )

        payload = {"boc": bytes_to_b64str(query["message"].to_boc(False))}
        headers={"Content-Type": "application/json"}

        async with request("POST", f"{self.url}sendBoc?api_key={self.key}", json=payload, headers=headers) as resp:
            response = await resp.json()
            if not (resp.ok):
                raise Exception(f"Failed sendTransfer with {walletHash} : {response}")
            
            return response