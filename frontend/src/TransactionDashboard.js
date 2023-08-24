import React, { useState } from "react";
import TransactionsTable from "./TransactionsTable";
import TransactionSummary from "./TransactionSummary";

function TransactionDashboard() {
  const [data, setData] = useState(null);

  return (
    <div>
      <TransactionsTable data={data} setData={setData} />
      <TransactionSummary data={data} />
    </div>
  );
}

export default TransactionDashboard;
