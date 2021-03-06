from brownie import accounts, Bank

def test_deposit():
    bank = Bank.deploy({'from': accounts[0]})
    balance = bank.balance()
    bank.deposit( "10 ether", {'from': accounts[0],'amount': "10 ether"})
    assert balance + "10 ether" == bank.balance()

def test_withdraw():
    bank = Bank.deploy({'from': accounts[0]})
    bank.deposit( "10 ether", {'from': accounts[0],'amount': "10 ether"})
    balance = bank.balance();
    bank.withdraw( "10 ether", {'from': accounts[0]})
    assert balance - "10 ether" == bank.balance()

def test_borrow():
    bank = Bank.deploy({'from': accounts[0]})
    bank.deposit( "10 ether", {'from': accounts[0],'amount': "10 ether"})
    balance = bank.balance();
    bank.borrow( "10 ether", {'from': accounts[1]})
    assert balance - "10 ether" == bank.balance()
