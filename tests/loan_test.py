from brownie import accounts, Bank
import pytest

#add the fn_isolation fixture to ensure that our tests
#are properly isolated. A snapshot of the local blockchain
#will be taken immediately after the token fixture executes,
#and each test will start from this snapshot.
@pytest.fixture(autouse=True)
def shared_setup(fn_isolation):
    pass



def test_deposit(bank):
    balance = bank.balance()
    bank.deposit( "10 ether", {'from': accounts[0],'amount': "10 ether"})
    assert balance + "10 ether" == bank.balance()

def test_withdraw(bank):
    bank.deposit( "10 ether", {'from': accounts[0],'amount': "10 ether"})
    balance = bank.balance();
    bank.withdraw( "10 ether", {'from': accounts[0]})
    assert balance - "10 ether" == bank.balance()

def test_borrow(bank):
    bank.deposit( "10 ether", {'from': accounts[0],'amount': "10 ether"})
    balance = bank.balance();
    bank.borrow( "10 ether", {'from': accounts[1]})
    assert balance - "10 ether" == bank.balance()
