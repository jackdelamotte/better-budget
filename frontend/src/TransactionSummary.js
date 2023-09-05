// TransactionSummary.js
import React from "react";
import { PieChart } from "@mui/x-charts/PieChart";
import { Box, Paper, Typography } from "@mui/material";

function TransactionSummary({ data }) {
  if (data === null) return;

  // Calculate the sum of amounts by category
  const categorySumMap = {};
  data.forEach((item) => {
    const categoryName = item.category_name;
    categorySumMap[categoryName] =
      (categorySumMap[categoryName] || 0) + -1 * item.amount;
  });

  // Prepare data for the PieChart
  const chartData = Object.entries(categorySumMap).map(([label, value]) => ({
    label,
    value,
  }));

  const totalAmount = data
    ? data.reduce(
        (total, item) => total + (item.amount < 0 ? item.amount : 0),
        0
      )
    : 0;

  const amountEarned = data
    ? data.reduce(
        (total, item) => total + (item.amount > 0 ? item.amount : 0),
        0
      )
    : 0;

  const percentageSaved = (amountEarned / totalAmount) * -100;

  return (
    <div>
      <Box p={2}>
        <Typography variant="h6">Transaction Summary</Typography>
        <p>Total Amount: ${totalAmount}</p>
        <p>Amount Earned: ${amountEarned}</p>
        <p>Percentage Saved: ${percentageSaved}</p>
      </Box>
      <Paper
        elevation={3}
        style={{
          width: "600px",
          margin: "auto",
          padding: "16px",
          height: "400px",
        }}
      >
        <PieChart
          series={[
            {
              data: chartData,
              //innerRadius: ,
              outerRadius: 100,
              //paddingAngle: 1,
              cornerRadius: 5,
              startAngle: -90,
              endAngle: 360,
              cx: 150,
              cy: 150,
            },
          ]}
        />
      </Paper>
    </div>
  );
}

export default TransactionSummary;
