from dotenv import load_dotenv
import os
import requests
import pandas as pd
import json

pd.set_option("display.max_rows", None)


class YNABInterface:
    def __init__(self, api_token):
        self._api_token = api_token
        self._headers = {"Authorization": f"Bearer {self._api_token}"}
        self._budget_id = os.environ.get("BUDGET_ID")
        self._account_ids = None
        self._transactions_df = None

    def get_all_transactions(
        self,
        start_date=None,
        end_date=None,
        filter_irrelevant=False,
        min_amount=None,
        max_amount=None,
    ):
        self.get_account_id_list()
        all_transactions = []

        # Aggregate transactions across accounts into single list
        for id in self._account_ids:
            transactions_url = f"https://api.youneedabudget.com/v1/budgets/{self._budget_id}/accounts/{id}/transactions"
            response = requests.get(transactions_url, headers=self._headers)
            print(response.json())
            account_transactions = response.json().get("data").get("transactions")
            all_transactions.extend(account_transactions)

        # Only keep date, amount, payee_name, and category for each transaction
        filtered_transactions = [
            {
                k: v
                for k, v in txn.items()
                if k in ["date", "amount", "payee_name", "category_name"]
            }
            for txn in all_transactions
        ]

        # Convert the filtered list of transactions to a DataFrame
        df = pd.DataFrame(filtered_transactions)

        # Convert to dollars
        df["amount"] = df["amount"].div(1000)

        # Make sure date column is datetime
        df["date"] = pd.to_datetime(df["date"])

        # Sort dataframe by date
        df = df.sort_values(by="date")

        # Convert to datetime if they're not None
        if start_date:
            start_date = pd.to_datetime(start_date)
        if end_date:
            end_date = pd.to_datetime(end_date)

        # Apply the filter based on the dates
        if start_date and end_date:
            df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]
        elif start_date:
            df = df[df["date"] >= start_date]
        elif end_date:
            df = df[df["date"] <= end_date]

        if filter_irrelevant:
            df = df[
                ~df["payee_name"].str.contains(
                    "transfer|chase credit crd epay|starting balance|wealthfront|payment thank you-mobile",
                    case=False,
                    na=False,
                )
            ]

        # Convert to float if they're not None
        if min_amount is not None:
            min_amount = float(min_amount)
        if max_amount is not None:
            max_amount = float(max_amount)

        # Apply the filter based on the amounts
        if min_amount is not None and max_amount is not None:
            df = df[(df["amount"] >= min_amount) & (df["amount"] <= max_amount)]
        elif min_amount is not None:
            df = df[df["amount"] >= min_amount]
        elif max_amount is not None:
            df = df[df["amount"] <= max_amount]

        self._transactions_df = df

        # Convert all Timestamp objects in 'date' column to strings
        df["date"] = df["date"].dt.strftime("%Y-%m-%d")

        # Convert DataFrame to list of dictionaries
        data = df.to_dict("records")

        # Convert list of dictionaries to JSON string with indentation
        json_data = json.dumps(data, indent=4)
        return json_data

    def get_account_id_list(self):
        accounts_url = (
            f"https://api.youneedabudget.com/v1/budgets/{self._budget_id}/accounts"
        )
        response = requests.get(accounts_url, headers=self._headers)
        accounts_list = response.json().get("data").get("accounts")
        account_ids = [
            account.get("id")
            for account in accounts_list
            if not account.get("closed", True)
        ]
        self._account_ids = account_ids
        return self._account_ids


if __name__ == "__main__":
    load_dotenv()
    api_token = os.getenv("YNAB_API_TOKEN")
    ynab_interface = YNABInterface(api_token)
    ynab_interface.get_account_id_list()
    ynab_interface.get_all_transactions(
        start_date="2023-07-01", end_date="2023-07-31", filter_irrelevant=True
    )
