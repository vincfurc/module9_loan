from brownie import accounts, Bank, chain
from brownie.test import given, strategy
import pytest

@pytest.mark.parametrize("amount", [0, 31337, 10**18])
def test_to_borrow_amount_is_received(bank, amount):
    bank.deposit( amount, {'from': accounts[0],'amount': "10 ether"})
    balance = bank.balance();
    idx = bank.borrow( amount, {'from': accounts[1]})
    assert balance - amount == bank.balance()

@given(amount=strategy('uint256', max_value=10**18))
def test_loan_count_increases_first_loan(bank,amount):
    bank.deposit( amount, {'from': accounts[0],'amount': amount})
    balance = bank.balance();
    bank.borrow( amount, {'from': accounts[1]})
    idx = bank.get_loans_count({'from': accounts[1]})
    assert idx == 1

@given(
  receiver=strategy('address'),
  amount=strategy('uint256', max_value=10**18),
)
def test_loan_count_increases_multiple_loans(bank, amount, receiver):
    bank.deposit( amount*3, {'from': accounts[0],'amount': amount*3})
    balance = bank.balance();
    bank.borrow( amount, {'from': receiver})
    bank.borrow( amount, {'from': receiver})
    bank.borrow( amount, {'from': receiver})
    idx = bank.get_loans_count({'from': receiver})
    assert idx == 3

def test_borrowed_amount_in_borrowers_list(bank):
    bank.deposit( "50 ether", {'from': accounts[0],'amount': "50 ether"})
    balance = bank.balance();
    bank.borrow( "10 ether", {'from': accounts[1]})
    bank.borrow( "10 ether", {'from': accounts[1]})
    bank.borrow( "10 ether", {'from': accounts[1]})
    tot = bank.get_borrowed_amount({'from': accounts[1]})
    assert tot == "30 ether"

def test_borrowed_amount_in_borrowers_list(bank):
    bank.deposit( "50 ether", {'from': accounts[0],'amount': "50 ether"})
    balance = bank.balance();
    bank.borrow( "10 ether", {'from': accounts[1]})
    bank.borrow( "10 ether", {'from': accounts[1]})
    bank.borrow( "10 ether", {'from': accounts[1]})
    tot = bank.get_loan_amount(0,{'from': accounts[1]})
    assert tot == "10 ether"
