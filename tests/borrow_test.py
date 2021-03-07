from brownie import accounts, Bank, chain
import pytest

def test_to_borrow_amount_is_received(bank):
    bank.deposit( "10 ether", {'from': accounts[0],'amount': "10 ether"})
    balance = bank.balance();
    idx = bank.borrow( "10 ether", {'from': accounts[1]})
    assert balance - "10 ether" == bank.balance()

def test_loan_count_increases_first_loan(bank):
    bank.deposit( "10 ether", {'from': accounts[0],'amount': "10 ether"})
    balance = bank.balance();
    bank.borrow( "10 ether", {'from': accounts[1]})
    idx = bank.get_loans_count({'from': accounts[1]})
    assert idx == 1

def test_loan_count_increases_multiple_loans(bank):
    bank.deposit( "50 ether", {'from': accounts[0],'amount': "50 ether"})
    balance = bank.balance();
    bank.borrow( "10 ether", {'from': accounts[1]})
    bank.borrow( "10 ether", {'from': accounts[1]})
    bank.borrow( "10 ether", {'from': accounts[1]})
    idx = bank.get_loans_count({'from': accounts[1]})
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
