import brownie
from brownie import accounts, Bank
import pytest

def test_deposit_fails_from_insufficient_balance(bank):
    balance = bank.balance()
    with brownie.reverts("Insufficient balance."):
        bank.deposit( "1000 ether", {'from': accounts[2],'amount': "100 ether"})
