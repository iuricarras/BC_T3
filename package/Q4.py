from bitcoin.core.script import *

######################################################################
# These functions will be used by Alice and Bob to send their respective
# coins to a utxo that is redeemable either of two cases:
# 1) Recipient provides x such that hash(x) = hash of secret
#    and recipient signs the transaction.
# 2) Sender and recipient both sign transaction
#
# TODO: Fill these in to create scripts that are redeemable by both
#       of the above conditions.
# See this page for opcode documentation: https://en.bitcoin.it/wiki/Script

# This is the ScriptPubKey for the swap transaction
def coinExchangeScript(public_key_sender, public_key_recipient, hash_of_secret):
    return [
        # fill this in!             # [secret, signature_recipient]  ou [signature_sender, signature_recipient]
        OP_SWAP,                    # [signature_recipient, secret]  ou [signature_recipient, signature_sender]
        OP_DUP,                     # [signature_recipient, secret, secret] ou [signature_recipient, signature_sender, signature_sender]
        OP_HASH160,                 # [signature_recipient, secret, hash(secret)] -> se for realmente o segredo
        hash_of_secret,             # [signature_recipient, secret, hash(secret), hash_of_secret]
        OP_EQUAL,                   # verifica se os dois hashes sao iguais [signature_recipient, true] ou [signature_recipient, false]
        OP_IF,                      # [signature_recipient, secret]
            OP_DROP, 
            public_key_recipient,   
            OP_CHECKSIG,            # verifica a assinatura do recipient 
        OP_ELSE,                    # [signature_recipient, signature_sender]
            OP_SWAP,                # [signature_sender, signature_recipient]
            OP_0,                   # [signature_sender, signature_recipient, 0]
            OP_ROT,                 # [signature_sender, 0, signature_recipient]
            OP_ROT,                 # [0, signature_sender, signature_recipient]
            OP_2,                   # [0, signature_sender, signature_recipient, 2]
            public_key_sender,      # [0, signature_sender, signature_recipient, 2, public_key_sender]
            public_key_recipient,   # [0, signature_sender, signature_recipient, 2, public_key_sender, public_key_recipient]
            OP_2,                   # [0, signature_sender, signature_recipient, 2, public_key_sender, public_key_recipient, 2]
            OP_CHECKMULTISIG,       # verifica se ambas assinaturas sao validas []
        OP_ENDIF
    ]

# This is the ScriptSig that the receiver will use to redeem coins
def coinExchangeScriptSig1(sig_recipient, secret):
    return [
        secret,
        sig_recipient
    ]

# This is the ScriptSig for sending coins back to the sender if unredeemed
def coinExchangeScriptSig2(sig_sender, sig_recipient):
    return [
        sig_sender,
        sig_recipient
    ]
######################################################################

######################################################################
#
# Configured for your addresses
#
# TODO: Fill in all of these fields
#

alice_txid_to_spend     = "cbb9dd8c0d27f5b04c1bd633db3b8004ab50bdc8fa64a9606c56c6c4321ee99c"
alice_utxo_index        = 1
alice_amount_to_send    = 0.00017910

bob_txid_to_spend       = "17f73ef60a077aa412a0e760544b93249a7f9c2921e86e6495eff61fdad0440d"
bob_utxo_index          = 1
bob_amount_to_send      = 0.008

# Get current block height (for locktime) in 'height' parameter for each blockchain (will be used in swap.py):
#  curl https://api.blockcypher.com/v1/btc/test3
btc_test3_chain_height  = 4783950

#  curl https://api.blockcypher.com/v1/bcy/test
bcy_test_chain_height   = 2143978

# Parameter for how long Alice/Bob should have to wait before they can take back their coins
# alice_locktime MUST be > bob_locktime
alice_locktime = 5
bob_locktime = 3

tx_fee = 0.0001

# While testing your code, you can edit these variables to see if your
# transaction can be broadcasted succesfully.
broadcast_transactions = False
alice_redeems = True

######################################################################
