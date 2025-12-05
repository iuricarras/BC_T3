from sys import exit
from bitcoin.core.script import *

from lib.utils import *
from lib.config import (my_private_key, my_public_key, my_address,
                    faucet_address, network_type)
from Q1 import send_from_P2PKH_transaction


######################################################################
# TODO: Complete the scriptPubKey implementation for Exercise 2
# x + y = 154, x - y = 32
# x = 93, y = 61
Q2a_txout_scriptPubKey = [
    OP_2DUP,           # Duplica os dois valores do topo (agora temos: x y x y)
    OP_ADD,            # Soma os dois do topo (agora temos: x y (x+y))
    154,               # Push 154 para a stack (agora temos: x y (x+y) 154)
    OP_EQUALVERIFY,    # Verifica se (x+y) == 154 e retira os dois comparados e o true da stack
    OP_SUB,            # Subtrai y de x (agora temos: (x-y))
    32,                # Push 32 para a stack (agora temos: (x-y) 32)
    OP_EQUAL           # Verifica se (x-y) == 32
]
######################################################################

if __name__ == '__main__':
    ######################################################################
    # TODO: set these parameters correctly
    amount_to_send = 0.00017910 # amount of BTC in the output you're sending minus fee
    txid_to_spend = (
        '96a1d18b1704ac18d8802d99e313505e4d8a40c67efb7556aa96057f233315ca')
    utxo_index = 2 # index of the output you are spending, indices start at 0
    ######################################################################

    response = send_from_P2PKH_transaction(
        amount_to_send, txid_to_spend, utxo_index,
        Q2a_txout_scriptPubKey, my_private_key, network_type)
    print(response.status_code, response.reason)
    print(response.text)
