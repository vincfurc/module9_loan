from brownie import accounts, Bank, chain
import pytest


def test_lenders_weight_calculation(bank,chain):
    balance = bank.balance()
    bank.deposit( "10 ether", {'from': accounts[0],'amount': "10 ether"})
    w_ = bank.calculate_weight(accounts[0])
    assert w_ == 1
    
