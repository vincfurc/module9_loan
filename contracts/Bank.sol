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
        uint weight;
        bool isValue;
    }

    struct Loan {
        uint amount_borrowed;
        uint amount_lent;
        uint timestamp;
    }

    mapping(address => Loan[]) loans;
    mapping(address => Borrower) public borrowers;
    mapping(address => Lender) lenders;

    address[] public lenders_;

    //fee per second
    uint FEE =  1 gwei;

    constructor() payable public {
    }


    function deposit(uint256 amount) public payable {
        require(msg.sender.balance >= amount, "Insufficient balance.");
        lenders_.push(msg.sender);
        lenders[msg.sender].amount_lent += amount;
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
         /* loans[msg.sender][borrower.loan_count].amount_borrowed = new_loan.amount_borrowed;
         loans[msg.sender][borrower.loan_count].timestamp = new_loan.timestamp; */
         }


    function withdraw(uint256 amount) public {
        require(address(this).balance >= amount);
        require(lenders[msg.sender].amount_lent >= amount);
        lenders[msg.sender].amount_lent -= amount;
        msg.sender.transfer(amount);
     }

    function repay_full_loan(uint loan_idx) public payable {
        require(borrowers[msg.sender].amount_borrowed > 0);
        uint total_fee = (block.timestamp - loans[msg.sender][loan_idx].timestamp) * 86400 * FEE;
        uint total_to_repay = borrowers[msg.sender].amount_borrowed + total_fee;
        require(msg.sender.balance >= total_to_repay);
        address(this).call{value:total_to_repay};
        borrowers[msg.sender].amount_borrowed = 0;
        Bank.distribute_fees(total_fee);
     }

     function calculate_weight(address _user_address) public view returns (uint256) {
        uint weight = lenders[_user_address].amount_lent / address(this).balance;
        return weight;
     }

    function total_available_to_borrow() public view returns (uint256) {
        return address(this).balance;
     }

    function distribute_fees(uint fees_paid) internal {
        for(uint8 i=0; i<= lenders_.length; i++){
            if (lenders[lenders_[i]].amount_lent>0) {
                address addr   = lenders_[i];
                uint256 weight = lenders[addr].weight;
                uint256 fee_share = fees_paid * weight;
                addr.call{value:fee_share};
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
      uint total_to_repay = loans[msg.sender][loan_id].amount_borrowed + total_fee;
      return total_fee;
    }

    receive() external payable { }

}
