from brownie import accounts, Bank, chain
import pytest

def test_to_borrow_amount_is_received(bank):
    bank.deposit( "10 ether", {'from': accounts[0],'amount': "10 ether"})
    balance = bank.balance();
    bank.borrow( "10 ether", {'from': accounts[1]})
    assert balance - "10 ether" == bank.balance()

def test_interests_accumulate(bank, chain):
    bank.deposit( "50 ether", {'from': accounts[0],'amount': "50 ether"})
    balance = bank.balance();
    bank.borrow( "10 ether", {'from': accounts[1]})
    t0 = chain.time()
    # sleep for 1 second
    chain.sleep(1)
    #Sleeping does not mine a new block. Contract view functions that rely on block.timestamp will be unaffected until you perform a transaction or call chain.mine.
    chain.mine(1)
    t1 = chain.time()
    tot = bank.get_fee_accumulated_on_loan((0), {'from': accounts[1]})
    tot_expected = (t1-t0)* 1000000000
    assert tot == tot_expected

def test_repayed_amount_is_transfered(bank,chain):
    bank.deposit( "50 ether", {'from': accounts[0],'amount': "50 ether"})
    bank.borrow( "10 ether", {'from': accounts[1]})
    balance = bank.balance();
    # sleep for 1 second
    chain.sleep(1)
    #Sleeping does not mine a new block. Contract view functions that rely on block.timestamp will be unaffected until you perform a transaction or call chain.mine.
    chain.mine(1)
    bank.repay_full_loan(0, {'from': accounts[1], 'amount': "15 ether" })
    assert bank.balance() > balance

def test_change_is_given_back(bank,chain):
    bank.deposit( "50 ether", {'from': accounts[0],'amount': "50 ether"})
    bank.borrow( "10 ether", {'from': accounts[1]})
    balance = bank.balance();
    # sleep for 1 second
    chain.sleep(1)
    #Sleeping does not mine a new block. Contract view functions that rely on block.timestamp will be unaffected until you perform a transaction or call chain.mine.
    chain.mine(1)
    bank.repay_full_loan(0, {'from': accounts[1], 'amount': "15 ether" })
    assert bank.balance() < balance + 15000000000000000000

def test_repaying_affects_lenders_balance(bank, chain):
    bank.deposit( "50 ether", {'from': accounts[0],'amount': "50 ether"})
    bank.borrow( "10 ether", {'from': accounts[1]})
    balance = accounts[0].balance();
    # sleep for 1 second
    chain.sleep(1)
    #Sleeping does not mine a new block. Contract view functions that rely on block.timestamp will be unaffected until you perform a transaction or call chain.mine.
    chain.mine(1)
    bank.repay_full_loan(0, {'from': accounts[1], 'amount': "15 ether" })
    # bank.distribute_fees(200000000000000, {'from':bank.address})
    assert accounts[0].balance() > balance 
