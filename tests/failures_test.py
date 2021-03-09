import brownie
from brownie import accounts, Bank
import pytest

def test_deposit_fails_from_insufficient_balance(bank):
    with brownie.reverts("Insufficient balance."):
        bank.deposit( "1000 ether", {'from': accounts[0],'amount': "100 ether"})

def test_borrow_fails_from_insufficient_balance(bank):
    bank.deposit( "50 ether", {'from': accounts[0],'amount': "50 ether"})
    with brownie.reverts():
        bank.borrow( "100 ether", {'from': accounts[2]})
