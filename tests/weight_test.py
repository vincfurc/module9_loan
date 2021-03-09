from brownie import accounts, Bank, chain
import pytest


def test_lender_weight_calculation(bank,chain):
    balance = bank.balance()
    bank.deposit( "10 ether", {'from': accounts[0],'amount': "10 ether"})
    w_ = bank.calculate_weight(accounts[0])
    assert w_ == 100


def test_lenders_weight_calculation(bank,chain):
    bank.deposit( "40 ether", {'from': accounts[0],'amount': "40 ether"})
    bank.deposit( "20 ether", {'from': accounts[3],'amount': "20 ether"})
    bank.borrow( "10 ether", {'from': accounts[1]})
    balance0 = accounts[0].balance();
    balance3 = accounts[3].balance();
    w_0 = bank.calculate_weight(accounts[0])
    w_3= bank.calculate_weight(accounts[3])
    assert w_0 == 66
    assert w_3 == 33
