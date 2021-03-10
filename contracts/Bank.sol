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

    address[] public lenders_;
    uint256 public total_supply;

    //fee per second
    uint256 internal FEE =  1 gwei;

    constructor() payable public {
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
        lenders_.push(_lender_address);
        Lender storage lender = lenders[_lender_address];
        lender.amount_lent += amount;
        /* lender.weight = calculate_weight(_lender_address, amount); */
        /* lender.weight = lenders[_lender_address].amount_lent / (address(this).balance + amount ); */

       }

    function withdraw(uint256 amount) external {
        require(address(this).balance >= amount);
        require(lenders[msg.sender].amount_lent >= amount);
        lenders[msg.sender].amount_lent -= amount;
        total_supply -= amount;
        msg.sender.transfer(amount);
     }

     function withdraw_fees() external {
         require(accumulated_earnings[msg.sender] > 0);
         uint256 to_pay = accumulated_earnings[msg.sender];
         accumulated_earnings[msg.sender] = 0;
         msg.sender.transfer(to_pay);
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
        distribute_fees(total_fee);
     }

    function distribute_fees(uint256 fees_received) private {
        require(fees_received>0);
        for(uint256 i=0; i< lenders_.length; i++){
            if (lenders[lenders_[i]].amount_lent>0) {
                address addr   = get_lender_address(i);
                uint256 weight = calculate_weight(addr);
                lenders[lenders_[i]].last_weight = weight;
                uint256 fee_share = (fees_received * weight)/100;
                accumulated_earnings[addr] += fee_share;
            }
        }
    }

    function calculate_weight(address _lender_address) public view returns (uint256) {
       uint256 weight = (100 * lenders[_lender_address].amount_lent) / total_supply;
       return weight;
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
      require(start_time>0);
      uint256 total_fee = (block.timestamp - start_time) * FEE;
      //uint256 total_to_repay = loans[msg.sender][loan_id].amount_borrowed + total_fee;
      return total_fee;
    }

    function get_number_of_lenders() external view returns (uint256){
      return lenders_.length;
    }

    function get_lender_address(uint256 i) public view returns (address){
      return lenders_[i];
    }

    function get_lender_weight() external view returns (uint256){
      return lenders[msg.sender].last_weight;
    }

    function get_lent_amount() external view returns (uint256){
      return lenders[msg.sender].amount_lent;
    }

    function get_accumulated_earnings() external view returns (uint256){
      return accumulated_earnings[msg.sender];
    }

    function get_total_supply() external view returns (uint256){
      return total_supply;
    }

    receive() external payable { }

}
