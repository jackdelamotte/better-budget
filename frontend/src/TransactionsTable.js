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
  TextField,
  FormControlLabel,
  Switch,
  Grid,
} from "@mui/material";
import "./TransactionsTable.css";
import FilterListIcon from "@mui/icons-material/FilterList";

function TransactionsTable() {
  const [data, setData] = useState(null);
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [hideIrrelevant, setHideIrrelevant] = useState(false);
  const [minAmount, setMinAmount] = useState("");
  const [maxAmount, setMaxAmount] = useState("");

  useEffect(() => {
    // Build the URL with query parameters
    let url = "http://127.0.0.1:5001/transactions?";
    if (startDate) url += `startDate=${startDate}&`;
    if (endDate) url += `endDate=${endDate}&`;
    if (hideIrrelevant) url += "filterIrrelevant=true&";
    if (minAmount) url += `minAmount=${minAmount}&`;
    if (maxAmount) url += `maxAmount=${maxAmount}&`;

    axios
      .get(url)
      .then((response) => setData(response.data))
      .catch((error) => console.error(error));
  }, [startDate, endDate, hideIrrelevant, minAmount, maxAmount]); // Rerun the effect when filters change

  const handleStartDateChange = (event) => setStartDate(event.target.value);
  const handleEndDateChange = (event) => setEndDate(event.target.value);
  const handleHideIrrelevantChange = (event) =>
    setHideIrrelevant(event.target.checked);
  const handleMinAmountChange = (event) => setMinAmount(event.target.value);
  const handleMaxAmountChange = (event) => setMaxAmount(event.target.value);

  if (data === null) return "Loading...";

  return (
    <div>
      <Paper elevation={3} className="filter-bar">
        <Grid container spacing={0} justifyContent="space-between">
          <Grid item>
            <FilterListIcon />
          </Grid>

          <Grid item xs={2}>
            <TextField
              label="Start Date"
              type="date"
              value={startDate}
              onChange={handleStartDateChange}
              InputLabelProps={{
                shrink: true,
                style: { fontSize: 10 },
              }}
              inputProps={{ style: { fontSize: 10, padding: "6px" } }}
              fullWidth
            />
          </Grid>
          <Grid item xs={2}>
            <TextField
              label="End Date"
              type="date"
              value={endDate}
              onChange={handleEndDateChange}
              InputLabelProps={{
                shrink: true,
                style: { fontSize: 10 },
              }}
              inputProps={{ style: { fontSize: 10, padding: "6px" } }}
              fullWidth
            />
          </Grid>
          <Grid item xs={2}>
            <TextField
              label="Minimum Amount"
              type="number"
              value={minAmount}
              onChange={handleMinAmountChange}
              InputLabelProps={{
                style: { fontSize: 10 },
              }}
              inputProps={{ style: { fontSize: 10, padding: "6px" } }}
              fullWidth
            />
          </Grid>
          <Grid item xs={2}>
            <TextField
              label="Maximum Amount"
              type="number"
              value={maxAmount}
              onChange={handleMaxAmountChange}
              InputLabelProps={{
                style: {
                  fontSize: 10,
                },
              }}
              inputProps={{
                style: {
                  fontSize: 10,
                  padding: "6px",
                },
              }}
              fullWidth
            />
          </Grid>
          <Grid item xs={2}>
            <FormControlLabel
              control={
                <Switch
                  checked={hideIrrelevant}
                  onChange={handleHideIrrelevantChange}
                />
              }
              label="Hide Irrelevant Transactions"
            />
          </Grid>
        </Grid>
      </Paper>
      <TableContainer component={Paper} className="table-container">
        <Table>
          <TableHead>
            <TableRow>
              <TableCell align="right">Date</TableCell>
              <TableCell align="right">Amount</TableCell>
              <TableCell align="right">Payee Name</TableCell>
              <TableCell align="right">Category Name</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {data.map((row, index) => (
              <TableRow key={index}>
                <TableCell align="right">{row.date}</TableCell>
                <TableCell align="right">{row.amount}</TableCell>
                <TableCell align="right">{row.payee_name}</TableCell>
                <TableCell align="right">{row.category_name}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
}

export default TransactionsTable;
