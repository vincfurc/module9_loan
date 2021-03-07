from brownie import accounts, Bank
import pytest


def test_deposited_amount_is_in_bank(bank):
    balance = bank.balance()
    bank.deposit( "10 ether", {'from': accounts[0],'amount': "10 ether"})
    assert balance + "10 ether" == bank.balance()

def test_lender_is_in_lenders_list():
    pass

def test_lent_amount_is_in_lenders_list():
    pass
