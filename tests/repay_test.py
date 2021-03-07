from brownie import accounts, Bank
import pytest

def test_to_borrow_amount_is_received(bank):
    bank.deposit( "10 ether", {'from': accounts[0],'amount': "10 ether"})
    balance = bank.balance();
    bank.borrow( "10 ether", {'from': accounts[1]})
    assert balance - "10 ether" == bank.balance()

def test_interests_accumulate():
    pass

def test_repayed_amount_is_transfered():
    pass

def test_interests_accumulate_correctly():
    pass

def test_repaying_affects_balance_correctly():
    pass
