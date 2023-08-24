import React from "react";

function TransactionSummary({ data }) {
  // Calculate the sum of amounts
  const totalAmount = data
    ? data.reduce((total, item) => total + item.amount, 0)
    : 0;

  return (
    <div>
      <h2>Transaction Summary</h2>
      <p>Total Amount: ${totalAmount}</p>
    </div>
  );
}

export default TransactionSummary;
