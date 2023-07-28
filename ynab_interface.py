from dotenv import load_dotenv
import os
import requests

class YNABInterface:
    def __init__(self, api_token):
        self._api_token = api_token
    
    def get_transactions(self):
        headers = {"Authorization": f"Bearer {self._api_token}"}
        budget_id = os.environ.get("BUDGET_ID")
        response = requests.get(f"https://api.youneedabudget.com/v1/budgets/{budget_id}/transactions", headers=headers)
        print("transactions:")
        print(response.json())


if __name__ == '__main__':
    load_dotenv()
    api_token = os.getenv('YNAB_API_TOKEN')
    ynab_interface = YNABInterface(api_token)
    ynab_interface.get_transactions()