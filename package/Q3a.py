from sys import exit
from bitcoin.core.script import *
from bitcoin.wallet import CBitcoinSecret

from lib.utils import *
from lib.config import (my_private_key, my_public_key, my_address,
                    faucet_address, network_type)
from Q1 import send_from_P2PKH_transaction


cust1_private_key = CBitcoinSecret(
    'cT3EfU9RFgeP7A7KhJWWXbbvz5mueynusT8vPdBEGM65McMvAoEz')
cust1_public_key = cust1_private_key.pub # mx1fdA7eVc2Auxfjp8jakijxsdhVQMqtND
cust2_private_key = CBitcoinSecret(
    'cVXcm4S2xAiAwo2M2oSVkWX4fEPU9v8atwTuR733va7ZukSgP7v2')
cust2_public_key = cust2_private_key.pub # mjRmixNKn4Pjdaaxy7MRTuNewyV3RmZKzg
cust3_private_key = CBitcoinSecret(
    'cRusG2J5nnxdXb1SwnobV9A7chmwATsXX8zPaT6gpMhmG8y7zjK3')
cust3_public_key = cust3_private_key.pub # mfuhjMgv7jmF9rNM2DsENs8ioMcxK8La8a


######################################################################
# TODO: Complete the scriptPubKey implementation for Exercise 3

# You can assume the role of the bank for the purposes of this problem
# and use my_public_key and my_private_key in lieu of bank_public_key and
# bank_private_key.

# inputs: bank_sig, customer_sig
# https://en.bitcoin.it/wiki/OP_CHECKMULTISIG
Q3a_txout_scriptPubKey = [
    # First verify the bank signature
    OP_SWAP,                 # [customer_sig, bank_sig]
    my_public_key,           # [customer_sig, bank_sig, bank_pubkey]
    OP_CHECKSIGVERIFY,       # Verify bank signature, consume both: [bank_sig, bank_pubkey]
    OP_0,                    # [customer_sig, 0] for bug fix
    OP_SWAP,                 # [0, customer_sig]
    OP_1,                    # requer uma assinatura [0, customer_sig, 1]
    cust1_public_key,        # [0, customer_sig, 1, cust1_pubkey]
    cust2_public_key,        # [0, customer_sig, 1, cust1_pubkey, cust2_pubkey]
    cust3_public_key,        # [0, customer_sig, 1, cust1_pubkey, cust2_pubkey, cust3_pubkey]
    OP_3,                    # total de chaves publicas [0, customer_sig, 1, cust1_pubkey, cust2_pubkey, cust3_pubkey, 3]
    OP_CHECKMULTISIG         # verifica se pelo menos 1 assinatura é valida [true]
]
######################################################################

if __name__ == '__main__':
    ######################################################################
    # TODO: set these parameters correctly
    amount_to_send = 0.00017910 # amount of BTC in the output you're sending minus fee
    txid_to_spend = (
        '96a1d18b1704ac18d8802d99e313505e4d8a40c67efb7556aa96057f233315ca')
    utxo_index = 3 # index of the output you are spending, indices start at 0
    ######################################################################

    response = send_from_P2PKH_transaction(amount_to_send, txid_to_spend, 
        utxo_index, Q3a_txout_scriptPubKey, my_private_key, network_type)
    print(response.status_code, response.reason)
    print(response.text)
