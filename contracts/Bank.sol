// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.6.6;

import "./SafeMath.sol";
import "./ABDKMath64x64.sol";
/**
 * @title loan
 * @dev borrow and loan money
 */

contract Bank {

    struct Borrower {
        uint256 amount_borrowed;
        uint256 weight;
        uint256 loan_count;
        //bool isValue;
    }

    struct Lender {
        uint256 amount_lent;
        uint256 last_weight;
        /* bool isValue; */
    }

    struct Loan {
        uint256 amount_borrowed;
        uint256 amount_lent;
        uint256 timestamp;
    }

    mapping(address => Borrower) public borrowers;
    mapping(address => Lender) public lenders;
    mapping(address => uint256) public accumulated_earnings;
    mapping(address => Loan[]) public loans;
    mapping(address => Loan[]) public deposits;
    mapping(address => uint256) public rewards_at_deposit;

    address[] public lenders_;
    uint256 public total_supply;
    uint256 public rewards_pool;
    uint256 precision = 12;

    //fee per second
    uint256 internal FEE =  10000000000 wei;

    constructor() payable public {
      rewards_pool = 0;
    }


    function deposit(uint256 amount) external payable {
        require(msg.sender.balance >= amount, "Insufficient balance.");
        Loan memory new_loan = Loan(amount,0, block.timestamp);
        total_supply += amount;
        _update_lenders(msg.sender, amount);
    }


    function borrow(uint256 amount) external {
        require(address(this).balance >= amount);// dev: Insufficient balance in Contract
        Loan memory new_loan = Loan(amount,0, block.timestamp);
        _update_borrowers(new_loan, amount);
        msg.sender.transfer(amount);
    }

    function _update_borrowers(Loan memory new_loan, uint256 amount) internal {
        Borrower storage borrower = borrowers[msg.sender];
         borrower.loan_count = borrower.loan_count + 1;
         borrower.amount_borrowed += amount;
         loans[msg.sender].push(new_loan);
    }

    function _update_lenders(address _lender_address, uint256 amount) internal {
        Lender storage lender = lenders[_lender_address];
        lender.amount_lent += amount;
        rewards_at_deposit[_lender_address] = rewards_pool;
    }

    function withdraw(uint256 amount) external {
        require(address(this).balance >= amount);
        require(lenders[msg.sender].amount_lent >= amount);
        lenders[msg.sender].amount_lent -= amount;
        total_supply -= amount;
        msg.sender.transfer(amount);
    }

    function withdraw_fees() external {
          uint256 deposited = lenders[msg.sender].amount_lent;
          uint256 reward = deposited * (rewards_pool - rewards_at_deposit[msg.sender]);
          accumulated_earnings[msg.sender] = reward;
          withdraw_fees_(accumulated_earnings[msg.sender], msg.sender);
    }

    function withdraw_fees_(uint256 to_pay, address addr_to_pay) private {
          require(accumulated_earnings[addr_to_pay]>0);
          accumulated_earnings[addr_to_pay] = 0;
          payable(addr_to_pay).transfer(to_pay/(10**precision));
    }

    function repay_full_loan(uint256 loan_idx) external payable {
        require(borrowers[msg.sender].amount_borrowed > 0);
        uint256 total_fee = get_fee_accumulated_on_loan(loan_idx);
        uint256 total_to_repay = loans[msg.sender][loan_idx].amount_borrowed + total_fee;
        require(msg.value >= total_to_repay);
        if(msg.value > total_to_repay){
          uint256 change = msg.value - total_to_repay;
          borrowers[msg.sender].amount_borrowed = 0;
          msg.sender.transfer(change);
        }
        require(total_fee>0);
        send_fees_to_pool(total_fee);
    }

    function percent(uint256 numerator, uint256 denominator, uint256 precision) public view returns(uint quotient) {
             // caution, check safe-to-multiply here
            uint256 _numerator  = numerator * 10 ** (precision+1);
            // with rounding of last digit
            uint256 _quotient =  ((_numerator / denominator) + 5) / 10;
            return ( _quotient);
    }

    function send_fees_to_pool(uint256 fees_received) private {
      require(fees_received>0);
      require(total_supply>0);
      rewards_pool = rewards_pool + percent(fees_received,total_supply,precision);
    }

    function get_loans_count() external view returns (uint256){
      return borrowers[msg.sender].loan_count;
    }

    function get_borrowed_amount() external view returns (uint256){
      return borrowers[msg.sender].amount_borrowed;
    }

    function get_loan_amount(uint256 loan_id) external view returns (uint256){
      return loans[msg.sender][loan_id].amount_borrowed;
    }

    function get_loan_timestamp(uint256 loan_id) external view returns (uint256){
      return loans[msg.sender][loan_id].timestamp;
    }

    function get_fee_accumulated_on_loan(uint256 loan_id) public view returns (uint256){
      uint256 start_time =  loans[msg.sender][loan_id].timestamp;
      uint256 amount_borrowed =  loans[msg.sender][loan_id].amount_borrowed;
      require(start_time>0);
      uint256 total_fee = (block.timestamp - start_time) * FEE;
      //TO DO: add adjustment for amount borrowed
      return total_fee;
    }

    function get_lender_weight() external view returns (uint256){
      return lenders[msg.sender].last_weight;
    }

    function get_lent_amount() external view returns (uint256){
      return lenders[msg.sender].amount_lent;
    }

    function get_accumulated_earnings() external view returns (uint256){
      uint256 deposited = lenders[msg.sender].amount_lent;
      uint256 reward = deposited * (rewards_pool - rewards_at_deposit[msg.sender]);
      return reward;
    }

    function get_total_supply() external view returns (uint256){
      return total_supply;
    }

    receive() external payable { }

}
