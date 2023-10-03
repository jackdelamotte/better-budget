import os
from dotenv import load_dotenv

import plaid
from plaid.model.payment_amount import PaymentAmount
from plaid.model.payment_amount_currency import PaymentAmountCurrency
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.recipient_bacs_nullable import RecipientBACSNullable
from plaid.model.payment_initiation_address import PaymentInitiationAddress
from plaid.model.payment_initiation_recipient_create_request import (
    PaymentInitiationRecipientCreateRequest,
)
from plaid.model.payment_initiation_payment_create_request import (
    PaymentInitiationPaymentCreateRequest,
)
from plaid.model.payment_initiation_payment_get_request import (
    PaymentInitiationPaymentGetRequest,
)
from plaid.model.link_token_create_request_payment_initiation import (
    LinkTokenCreateRequestPaymentInitiation,
)
from plaid.model.item_public_token_exchange_request import (
    ItemPublicTokenExchangeRequest,
)
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.asset_report_create_request import AssetReportCreateRequest
from plaid.model.asset_report_create_request_options import (
    AssetReportCreateRequestOptions,
)
from plaid.model.asset_report_user import AssetReportUser
from plaid.model.asset_report_get_request import AssetReportGetRequest
from plaid.model.asset_report_pdf_get_request import AssetReportPDFGetRequest
from plaid.model.auth_get_request import AuthGetRequest
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from plaid.model.identity_get_request import IdentityGetRequest
from plaid.model.investments_transactions_get_request_options import (
    InvestmentsTransactionsGetRequestOptions,
)
from plaid.model.investments_transactions_get_request import (
    InvestmentsTransactionsGetRequest,
)
from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.investments_holdings_get_request import InvestmentsHoldingsGetRequest
from plaid.model.item_get_request import ItemGetRequest
from plaid.model.institutions_get_by_id_request import InstitutionsGetByIdRequest
from plaid.model.transfer_authorization_create_request import (
    TransferAuthorizationCreateRequest,
)
from plaid.model.transfer_create_request import TransferCreateRequest
from plaid.model.transfer_get_request import TransferGetRequest
from plaid.model.transfer_network import TransferNetwork
from plaid.model.transfer_type import TransferType
from plaid.model.transfer_authorization_user_in_request import (
    TransferAuthorizationUserInRequest,
)
from plaid.model.ach_class import ACHClass
from plaid.model.transfer_create_idempotency_key import TransferCreateIdempotencyKey
from plaid.model.transfer_user_address_in_request import TransferUserAddressInRequest
from plaid.api import plaid_api

PLAID_CLIENT_ID = os.getenv("PLAID_CLIENT_ID")
PLAID_SECRET = os.getenv("PLAID_SECRET")
PLAID_ENV = os.getenv("PLAID_ENV", "sandbox")
PLAID_PRODUCTS = os.getenv("PLAID_PRODUCTS", "transactions").split(",")
PLAID_COUNTRY_CODES = os.getenv("PLAID_COUNTRY_CODES", "US").split(",")

host = plaid.Environment.Sandbox

if PLAID_ENV == "sandbox":
    host = plaid.Environment.Sandbox

if PLAID_ENV == "development":
    host = plaid.Environment.Development

if PLAID_ENV == "production":
    host = plaid.Environment.Production


def empty_to_none(field):
    value = os.getenv(field)
    if value is None or len(value) == 0:
        return None
    return value


PLAID_REDIRECT_URI = empty_to_none("PLAID_REDIRECT_URI")

configuration = plaid.Configuration(
    host=host,
    api_key={
        "clientId": PLAID_CLIENT_ID,
        "secret": PLAID_SECRET,
        "plaidVersion": "2020-09-14",
    },
)

api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

products = []
for product in PLAID_PRODUCTS:
    products.append(Products(product))

# TODO: storing this in memory okay for dev but for prod should be in a secure persistent data store
access_token = None
item_id = None


def info():
    global access_token
    global item_id
    return {
        "item_id": item_id,
        "access_token": access_token,
        "products": PLAID_PRODUCTS,
    }
    # return jsonify({
    #     'item_id': item_id,
    #     'access_token': access_token,
    #     'products': PLAID_PRODUCTS
    # })


if __name__ == "__main__":
    load_dotenv()
    print(info())
