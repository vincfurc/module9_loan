// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.6.6;

/**
 * @title loan
 * @dev borrow and loan money
 */

contract Bank {

    struct Borrower {
        uint amount_borrowed;
        uint weight;
        uint loan_count;
        //bool isValue;
    }

    struct Lender {
        uint amount_lent;
        uint last_weight;
        /* bool isValue; */
    }

    struct Loan {
        uint amount_borrowed;
        uint amount_lent;
        uint timestamp;
    }

    mapping(address => Borrower) public borrowers;
    mapping(address => Lender) public lenders;
    mapping(address => Loan[]) loans;
    mapping(address => Loan[]) deposits;

    address[] public lenders_;
    uint total_supply;

    //fee per second
    uint FEE =  1 gwei;

    constructor() payable public {
    }


    function deposit(uint256 amount) public payable {
        require(msg.sender.balance >= amount, "Insufficient balance.");
        Loan memory new_loan = Loan(amount,0, block.timestamp);
        total_supply += amount;
        _update_lenders(msg.sender, amount);
     }


    function borrow(uint256 amount) public {
        require(address(this).balance >= amount);
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

    function withdraw(uint256 amount) public {
        require(address(this).balance >= amount);
        require(lenders[msg.sender].amount_lent >= amount);
        lenders[msg.sender].amount_lent -= amount;
        total_supply -= amount;
        msg.sender.transfer(amount);
     }

    function repay_full_loan(uint loan_idx) public payable {
        require(borrowers[msg.sender].amount_borrowed > 0);
        uint total_fee = get_fee_accumulated_on_loan(loan_idx);
        uint total_to_repay = loans[msg.sender][loan_idx].amount_borrowed + total_fee;
        require(msg.value >= total_to_repay);
        if(msg.value > total_to_repay){
          uint change = msg.value - total_to_repay;
          borrowers[msg.sender].amount_borrowed = 0;
          msg.sender.transfer(change);
        }
        distribute_fees(total_fee);
     }

     function calculate_weight(address _lender_address) public view returns (uint256) {
        uint weight = lenders[_lender_address].amount_lent / total_supply;
        return weight;
     }

    function total_available_to_borrow() public view returns (uint256) {
        return address(this).balance;
     }

    function distribute_fees(uint fees_received) internal {
      /* payable(lenders_[0]).transfer(fees_paid); */
        for(uint8 i=0; i< lenders_.length; i++){
            if (lenders[lenders_[i]].amount_lent>0) {
                address addr   = lenders_[i];
                uint256 weight = calculate_weight(addr);
                lenders[lenders_[i]].last_weight = weight;
                uint256 fee_share = fees_received * weight;
                fees_received = 0;
                payable(addr).transfer(fee_share);
            }
        }

    }

    function get_loans_count() public view returns (uint256){
      return borrowers[msg.sender].loan_count;
    }

    function get_borrowed_amount() public view returns (uint256){
      return borrowers[msg.sender].amount_borrowed;
    }

    function get_loan_amount(uint loan_id) public view returns (uint){
      return loans[msg.sender][loan_id].amount_borrowed;
    }

    function get_loan_timestamp(uint loan_id) public view returns (uint){
      return loans[msg.sender][loan_id].timestamp;
    }

    function get_fee_accumulated_on_loan(uint loan_id) public view returns (uint){
      uint start_time =  loans[msg.sender][loan_id].timestamp;
      require(start_time>0);
      uint total_fee = (block.timestamp - start_time) * FEE;
      //uint total_to_repay = loans[msg.sender][loan_id].amount_borrowed + total_fee;
      return total_fee;
    }

    function get_number_of_lenders() public view returns (uint){
      return lenders_.length;
    }

    function get_lender_address(uint i) public view returns (address){
      return lenders_[i];
    }

    function get_lender_weight() public view returns (uint){
      return lenders[msg.sender].last_weight;
    }

    function get_lent_amount() public view returns (uint){
      return lenders[msg.sender].amount_lent;
    }

    receive() external payable { }

}
