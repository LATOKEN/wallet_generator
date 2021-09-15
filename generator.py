from eth_wallet import Wallet
from eth_wallet.utils import generate_mnemonic
import web3
from ethereum import utils
import sys


FEED_PRIVATE_KEY = bytes.fromhex('d95d6db65f3e2223703c5d8e205d98e3e6b470f067b0f94f6c6bf73d4301ce48')
FEED_ADDRESS = utils.checksum_encode(utils.privtoaddr(FEED_PRIVATE_KEY))
CHAIN_ID = 41
LOCALNET_NODE = 'http://127.0.0.1:7070'
DEVNET_NODE = 'http://88.198.78.106:7070'
TESTNET_NODE = 'http://95.217.17.248:7070'


def gen_wallet():
    wallet = Wallet()
    wallet.from_mnemonic(mnemonic=generate_mnemonic(language="english"), passphrase=None)
    wallet.from_path("m/44'/60'/0'/0/0")
    res = (wallet.address(), f"0x{wallet.private_key()}", wallet.mnemonic())
    return res


def send_amount(to, amount, node, nonce):
    transaction = {
        'from': FEED_ADDRESS,
        'to': utils.checksum_encode(to),
        'value': amount,
        'gas': 4000000,
        'gasPrice': 1,
        'nonce': nonce,
        'chainId': CHAIN_ID
    }
    signed = web3.eth.Account.signTransaction(transaction, FEED_PRIVATE_KEY)
    txid = node.eth.sendRawTransaction(signed.rawTransaction)
    return txid


def main(number_to_generate, initial_amount, output):
    node = web3.Web3(web3.Web3.HTTPProvider(DEVNET_NODE))
    nonce = node.eth.getTransactionCount(FEED_ADDRESS)
    with open(output, "wt") as resfile:
        for i in range(number_to_generate):
            address, priv_key, seed = gen_wallet()
            send_amount(address, node.toWei(initial_amount, "ether"),node, nonce)
            nonce += 1
            resfile.write(f"{address};{priv_key};{seed}\n")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: generator.py number_of_addresses initial_amount")
        print("for example, generator.py 10 0.001")
        exit()
    main(int(sys.argv[1]), float(sys.argv[2]), "result.csv")

