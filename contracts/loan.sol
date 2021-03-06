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
        mapping(uint => Loan) loans;
    }

    struct Lender {
        uint amount_lent;
        uint weight;
    }

    struct Loan {
        uint amount_deposited;
        uint amount_lent;
        uint timestamp;
    }


    address payable owner;
    mapping(address => Borrower) borrowers;
    mapping(address => Lender) lenders;

    address[] public lenders_;

    //fee per second
    uint FEE =  1 gwei;

    constructor() public {
         owner = msg.sender;
    }


    function deposit (uint256 amount) public payable {
        require(msg.sender.balance >= amount, "Insufficient balance.");
        lenders_.push(msg.sender);
        payable(address(this)).transfer(amount);
        lenders[msg.sender].amount_lent += amount;
     }


    function borrow(uint256 amount) public returns (uint256)  {
        //User storage sender = users[msg.sender];
        require(address(this).balance >= amount);
        Loan memory new_loan = Loan(amount,0, block.timestamp);
        uint idx = borrowers[msg.sender].loan_count + 1;
        borrowers[msg.sender].loans[idx] = new_loan;
        borrowers[msg.sender].amount_borrowed += amount;
        msg.sender.call{value:amount};
        return idx;
     }


    function withdraw(uint256 amount) public {
        require(address(this).balance >= amount);
        require(lenders[msg.sender].amount_lent >= amount);
        lenders[msg.sender].amount_lent -= amount;
        msg.sender.call{value:amount};
     }

    function repay_full_loan(uint loan_idx) public payable {
        require(borrowers[msg.sender].amount_borrowed > 0);
        uint total_fee = (block.timestamp - borrowers[msg.sender].loans[loan_idx].timestamp) * 86400 * FEE;
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

    receive() external payable { }


}
