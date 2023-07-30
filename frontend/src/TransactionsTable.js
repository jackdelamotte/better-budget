import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from "@mui/material";

function TransactionsTable() {
  const [data, setData] = useState(null);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:5000/transactions")
      .then((response) => setData(response.data))
      .catch((error) => console.error(error));
  }, []);

  if (data === null) return "Loading...";

  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Date</TableCell>
            <TableCell align="right">Amount</TableCell>
            <TableCell align="right">Payee Name</TableCell>
            <TableCell align="right">Category Name</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {data.map((row, index) => (
            <TableRow key={index}>
              <TableCell component="th" scope="row">
                {row.date}
              </TableCell>
              <TableCell align="right">{row.amount}</TableCell>
              <TableCell align="right">{row.payee_name}</TableCell>
              <TableCell align="right">{row.category_name}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}

export default TransactionsTable;
