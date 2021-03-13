from brownie import accounts, Bank, chain
import pytest


def test_fees_distributed__upon_repayment_standard(bank, chain):
        bank.deposit( "30 ether", {'from': accounts[0],'amount': "30 ether"})
        bank.deposit( "20 ether", {'from': accounts[3],'amount': "20 ether"})
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
        a = (balance0 + (fee*0.6))
        b = (balance3 + (fee*0.4))
        assert accounts[0].balance() == a
        assert accounts[3].balance() == b



@pytest.mark.xfail
def test_fees_distributed_upon_repayment_v2(bank, chain):
        bank.deposit( "30 ether", {'from': accounts[0],'amount': "30 ether"})
        bank.borrow( "10 ether", {'from': accounts[1]})
        bank.deposit( "20 ether", {'from': accounts[3],'amount': "20 ether"})
        # bank.borrow( "20 ether", {'from': accounts[2]})
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
        # should fail here
        bank.deposit( "20 ether", {'from': accounts[3],'amount': "20 ether"})
        bank.withdraw_fees({'from': accounts[0]})
        bank.withdraw_fees({'from': accounts[3]})
        a = (balance0 + (fee*0.6))
        b = (balance3 + (fee*0.4))
        assert accounts[0].balance() == a
        assert accounts[3].balance() == b

def test_fees_distributed__second_deposit_after_borrow(bank, chain):
        bank.deposit( "30 ether", {'from': accounts[0],'amount': "30 ether"})
        bank.borrow( "10 ether", {'from': accounts[1]})
        bank.deposit( "20 ether", {'from': accounts[3],'amount': "20 ether"})
        # bank.borrow( "20 ether", {'from': accounts[2]})
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
        # bank.withdraw_fees({'from': accounts[3]})
        a = (balance0 + (fee*0.6))
        b = (balance3 + (fee*0.4))
        assert accounts[0].balance() == a
        assert accounts[3].balance() == balance3
        bank.deposit( "30 ether", {'from': accounts[0],'amount': "30 ether"})
        bank.borrow( "20 ether", {'from': accounts[1]})
        chain.sleep(10)
        chain.mine(1)
        fee2 = bank.get_fee_accumulated_on_loan(1, {'from': accounts[1]})
        bank.repay_full_loan(1, {'from': accounts[1], 'amount': "25 ether" })
        bank.withdraw_fees({'from': accounts[0]})
        bank.withdraw_fees({'from': accounts[3]})
        a2 = (balance0 + (fee*0.6)) - 30000000000000000000 + (fee2*0.75)
        b2 = (balance3 + (fee*0.4))+ (fee2*0.25)
        assert accounts[3].balance() == b2
        assert accounts[0].balance() == a2

def test_fees_distributed__fees_not_withdrawn_until_second_loan_repaid(bank, chain):
        bank.deposit( "30 ether", {'from': accounts[0],'amount': "30 ether"})
        bank.borrow( "10 ether", {'from': accounts[1]})
        bank.deposit( "20 ether", {'from': accounts[3],'amount': "20 ether"})
        # bank.borrow( "20 ether", {'from': accounts[2]})
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
        # bank.withdraw_fees({'from': accounts[3]})
        a = (balance0 + (fee*0.6))
        b = (balance3 + (fee*0.4))
        assert accounts[0].balance() == a
        assert accounts[3].balance() == balance3
        bank.deposit( "30 ether", {'from': accounts[0],'amount': "30 ether"})
        bank.borrow( "20 ether", {'from': accounts[1]})
        chain.sleep(10)
        chain.mine(1)
        fee2 = bank.get_fee_accumulated_on_loan(1, {'from': accounts[1]})
        bank.repay_full_loan(1, {'from': accounts[1], 'amount': "25 ether" })
        bank.withdraw_fees({'from': accounts[0]})
        bank.withdraw("60 ether",{'from': accounts[0]})
        bank.withdraw_fees({'from': accounts[3]})
        a2 = (balance0 + (fee*0.6)) + 30000000000000000000 + (fee2*0.75)
        b2 = (balance3 + (fee*0.4))+ (fee2*0.25)
        assert accounts[3].balance() == b2
        assert accounts[0].balance() == a2
