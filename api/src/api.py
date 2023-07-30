from flask import Flask, Response, request
from flask_cors import CORS
from ynab_interface import YNABInterface
import os

app = Flask(__name__)
CORS(app)
api_token = os.getenv('YNAB_API_TOKEN')
ynab = YNABInterface(api_token=api_token)

@app.route('/transactions', methods=['GET'])
def get_transactions():
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')
    filter_irrelevant = bool(request.args.get('filterIrrelevant'))
    return Response(ynab.get_all_transactions(start_date=start_date, end_date=end_date, filter_irrelevant=filter_irrelevant), mimetype='application/json')

# @app.route('/items', methods=['POST'])
# def add_item():
#     item = request.get_json()
#     data.append(item)
#     return jsonify(item), 201

# @app.route('/items/<int:item_id>', methods=['GET'])
# def get_item(item_id):
#     item = next((item for item in data if item["id"] == item_id), None)
#     if item is None:
#         return jsonify({"error": "Item not found"}), 404
#     return jsonify(item)

# @app.route('/items/<int:item_id>', methods=['DELETE'])
# def delete_item(item_id):
#     global data
#     data = [item for item in data if item["id"] != item_id]
#     return '', 204

if __name__ == '__main__':
    app.run(debug=True)
