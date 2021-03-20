#!/usr/bin/python3

from algosdk.v2client import algod
from algosdk import mnemonic
from algosdk import transaction
from algosdk import mnemonic
import base64


#1) Generate an account
#2) Fund the account from the Algorand Testnet Dispenser
#3) Write a python script to send coins to a specified address

#Connect to Algorand node maintained by PureStake



algod_token = "B3SU4KcVKi94Jap2VXkK83xx38bsv95K5UZm2lab" #API key
algod_address = "https://testnet-algorand.api.purestake.io/ps2"
#algod_token = 'IwMysN3FSZ8zGVaQnoUIJ9RXolbQ5nRY62JRqF2H'
headers = {"X-API-Key": algod_token}



mnemonic_secret = "polar taxi broccoli decrease ten decrease illness engine suit useless unit planet eternal abandon click during adapt decide jazz proud evil kingdom century abstract empty"
sk = mnemonic.to_private_key(mnemonic_secret)
pk = mnemonic.to_public_key(mnemonic_secret)
acl = algod.AlgodClient(algod_token, algod_address, headers)
min_balance = 100000 #https://developer.algorand.org/docs/features/accounts/#minimum-balance

#print(algod_address)
#print(algod_token)
#print(headers)
#print("Base64 Private Key: {}\nPublic Algorand Address: {}\n".format(sk, pk))
#Base64 Private Key: cvc2Zgq8GVTtCAR9PAC8O6rLn7s39QdOKU3ldvLK6zffxHg1oanbrGbU3kL6w0NeB4KO2ChJHaaDf25Zb1OqZw==
#Public Algorand Address: 37CHQNNBVHN2YZWU3ZBPVQ2DLYDYFDWYFBER3JUDP5XFS32TVJT3ZEXNE4

#Your function should take two inputs, a string “receiver_pk” and a number "amount". Your function should create a transaction
#that sends “amount” microalgos to the account given by “receiver_pk” and submit the transaction to the Algorand Testnet.
def send_tokens( receiver_pk, tx_amount ):
    params = acl.suggested_params()
    gen_hash = params.gh
    first_valid_round = params.first
    tx_fee = params.min_fee
    last_valid_round = params.last
    
    #Your code here
    #Your function should return the address of the sender (“sender_pk”) as well as the id of the 
    #resulting transaction (“txid”) as it appears on the Testnet blockchain.
    send_amount = tx_amount
    existing_account = pk
    send_to_address = receiver_pk

    #create and sign transaction
    tx = transaction.PaymentTxn(existing_account, tx_fee, first_valid_round, last_valid_round, gen_hash, send_to_address, send_amount, flat_fee=True)
    signed_tx = tx.sign(sk)

    #send the signed transaction to the blockchain
    try:
        tx_confirm = acl.send_transaction(signed_tx)
        wait_for_confirmation(acl, txid=signed_tx.transaction.get_txid())
    except Exception as e:
        print(e)

    txid = tx
    sender_pk = send_to_address
    print(txid, sender_pk)

    return sender_pk, txid


# Function from Algorand Inc.
def wait_for_confirmation(client, txid):
    """
    Utility function to wait until the transaction is
    confirmed before proceeding.
    """
    last_round = client.status().get('last-round')
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0):
        print("Waiting for confirmation")
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    print("Transaction {} confirmed in round {}.".format(txid, txinfo.get('confirmed-round')))
    return txinfo



send_tokens('AEC4WDHXCDF4B5LBNXXRTB3IJTVJSWUZ4VJ4THPU2QGRJGTA3MIDFN3CQA', 3000)