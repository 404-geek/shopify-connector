import json
import requests
from flask import request as flask_request
from workflows_cdk import Response, Request
from main import router


# @router.route("/schema", methods=["POST"])
# def schema():
#     try:
#         request = Request(flask_request)
#         data = request.data
#         form_data = data.get("form_data", {})
#
#         print("here")
#         order_mode = form_data.get("order_mode", "structured")
#
#
#
#         with open("src/modules/create_order/v1/schema.json") as f:
#             base_schema = json.load(f)
#
#         updated_fields = []
#         for field in base_schema["fields"]:
#             if order_mode == "structured":
#                 if field["id"] in ["customer_email", "shipping_address", "line_items"]:
#                     field["ui_options"] = field.get("ui_options", {})
#                 if field["id"] == "raw_order_json":
#                     field["ui_options"] = { "ui_widget": "hidden" }
#             elif order_mode == "raw_json":
#                 if field["id"] in ["customer_email", "shipping_address", "line_items"]:
#                     field["ui_options"] = { "ui_widget": "hidden" }
#                 if field["id"] == "raw_order_json":
#                     field["ui_options"] = { "ui_widget": "CodeblockWidget", "language": "json" }
#             updated_fields.append(field)
#
#         base_schema["fields"] = updated_fields
#         return Response(data=base_schema)
#
#     except Exception as e:
#         print(str(e))
#         return Response.error(str(e))

@router.route("/execute", methods=["POST"])
def execute():
    try:
        req = Request(flask_request)
        data = req.data

        shop_domain = data.get("shop_domain")
        access_token = data.get("access_token")
        shipping_address = data.get("shipping_address", {})
        customer_email = data.get("customer_email")

        line_items = data.get("line_items")

        print(line_items)


        payload = {
            "order": {
                "email": customer_email,
                "currency": "USD",
                "financial_status": "paid",
                "send_receipt": False,
                "send_fulfillment_receipt": False,
                "inventory_behaviour": "bypass",
                "line_items": line_items,
                "shipping_address": {
                    "name": shipping_address.get("name"),
                    "address1": shipping_address.get("address1"),
                    "city": shipping_address.get("city"),
                    "country": shipping_address.get("country"),
                    "zip": shipping_address.get("zip")
                }
            }
        }

        headers = {
            "X-Shopify-Access-Token": access_token,
            "Content-Type": "application/json"
        }


        res = requests.post(f"https://{shop_domain}/admin/api/2023-10/orders.json", json=payload, headers=headers)
        res.raise_for_status()

        return Response(data=res.json(), metadata={"message": "Order created successfully"})

    except Exception as e:
        print(str(e))
        return Response.error(str(e))

