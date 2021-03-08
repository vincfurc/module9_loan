from brownie import accounts, Bank
import pytest


def test_deposited_amount_is_in_bank(bank):
    balance = bank.balance()
    bank.deposit( "10 ether", {'from': accounts[0],'amount': "10 ether"})
    assert balance + "10 ether" == bank.balance()

def test_lender_is_in_lenders_list(bank):
    balance = bank.balance()
    bank.deposit( "10 ether", {'from': accounts[0],'amount': "10 ether"})
    name = bank.get_lender_address(0)
    assert name == accounts[0].address


def test_lent_amount_is_in_lenders_list(bank):
    balance = bank.balance()
    bank.deposit( "10 ether", {'from': accounts[0],'amount': "10 ether"})
    amount = bank.get_lent_amount({'from': accounts[0]})
    assert amount == 10000000000000000000


def test_number_of_lenders(bank):
    balance = bank.balance()
    bank.deposit( "10 ether", {'from': accounts[0],'amount': "10 ether"})
    n = bank.get_number_of_lenders()
    assert n == 1
