from brownie import accounts, Bank, chain
from brownie.test import given, strategy
import pytest

def test_to_borrow_amount_is_received(bank):
    bank.deposit( "10 ether", {'from': accounts[0],'amount': "10 ether"})
    balance = bank.balance();
    bank.borrow( "10 ether", {'from': accounts[1]})
    assert balance - "10 ether" == bank.balance()


def test_interests_accumulate_on_10_eth(bank, chain):
    bank.deposit( "50 ether", {'from': accounts[0],'amount': "50 ether"})
    balance = bank.balance();
    bank.borrow( "10 ether", {'from': accounts[1]})
    t0 = bank.get_loan_timestamp(0,{'from': accounts[1]})
    # sleep for 1 second
    chain.sleep(1)
    #Sleeping does not mine a new block. Contract view functions that rely on block.timestamp will be unaffected until you perform a transaction or call chain.mine.
    chain.mine(1)
    tot = bank.get_fee_accumulated_on_loan((0), {'from': accounts[1]})
    t1 = chain[-1].timestamp
    tot_expected = (t1-t0) * 2000000000 * 10
    assert tot == tot_expected

@given(amount=strategy('uint256', max_value=10**18))
def test_interests_accumulate(bank, chain,amount):
    bank.deposit( "50 ether", {'from': accounts[0],'amount': "50 ether"})
    balance = bank.balance();
    bank.borrow( amount, {'from': accounts[1]})
    t0 = bank.get_loan_timestamp(0,{'from': accounts[1]})
    # sleep for 1 second
    chain.sleep(1)
    #Sleeping does not mine a new block. Contract view functions that rely on block.timestamp will be unaffected until you perform a transaction or call chain.mine.
    chain.mine(1)
    tot = bank.get_fee_accumulated_on_loan((0), {'from': accounts[1]})
    t1 = chain[-1].timestamp
    tot_expected = (t1-t0) * 2000000000 * (amount/10**18)
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
    bank.deposit( "30 ether", {'from': accounts[3],'amount': "30 ether"})
    bank.borrow( "10 ether", {'from': accounts[1]})
    balance0 = accounts[0].balance();
    balance3 = accounts[3].balance();
    # sleep for 1 second
    chain.sleep(10)
    #Sleeping does not mine a new block. Contract view functions that rely on block.timestamp will be unaffected until you perform a transaction or call chain.mine.
    chain.mine(1)
    fee = bank.get_fee_accumulated_on_loan(0, {'from': accounts[1]})
    assert fee > 0
    bank.repay_full_loan(0, {'from': accounts[1], 'amount': "15 ether" })
    earned = bank.get_accumulated_earnings({'from': accounts[0]})
    assert earned>0
    bank.withdraw_fees({'from': accounts[0]})
    bank.withdraw_fees({'from': accounts[3]})
    assert accounts[0].balance() > balance0
    assert accounts[3].balance() > balance3
