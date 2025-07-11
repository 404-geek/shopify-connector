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

        # Common data for both order types
        shop_domain = data.get("shop_domain")
        access_token = data.get("access_token")
        order_type = data.get("order_type")
        customer = data.get("customer", {})
        line_items = data.get("line_items", [])
        shipping_address = data.get("shipping_address", {})

        headers = {
            "X-Shopify-Access-Token": access_token,
            "Content-Type": "application/json"
        }

        payload = {}
        endpoint = ""

        if order_type == "complete":
            endpoint = f"https://{shop_domain}/admin/api/2023-10/orders.json"

            payload = {
                "order": {
                    "email": customer.get("email"),
                    "line_items": line_items,
                    "shipping_address": {
                        "first_name": shipping_address.get("first_name"),
                        "last_name": shipping_address.get("last_name"),
                        "address1": shipping_address.get("address1"),
                        "city": shipping_address.get("city"),
                        "province": shipping_address.get("province"),
                        "country": shipping_address.get("country"),
                        "zip": shipping_address.get("zip")
                    },
                    "financial_status": data.get("financial_status"),
                    "currency": data.get("currency", "USD"),
                    "send_receipt": data.get("send_receipt", False),
                    "send_fulfillment_receipt": False
                }
            }

        elif order_type == "draft":

            endpoint = f"https://{shop_domain}/admin/api/2023-10/draft_orders.json"

            payload = {
                "draft_order": {
                    "email": customer.get("email"),
                    "line_items": line_items,
                    "shipping_address": {
                        "first_name": shipping_address.get("first_name"),
                        "last_name": shipping_address.get("last_name"),
                        "address1": shipping_address.get("address1"),
                        "city": shipping_address.get("city"),
                        "province": shipping_address.get("province"),
                        "country": shipping_address.get("country"),
                        "zip": shipping_address.get("zip")
                    },
                    "customer": {
                        "first_name": customer.get("first_name"),
                        "last_name": customer.get("last_name"),
                        "email": customer.get("email")
                    },
                    "applied_discount": data.get("applied_discount"),
                    "send_invoice": data.get("send_invoice", False)
                }
            }
            if not payload["draft_order"]["applied_discount"]:
                del payload["draft_order"]["applied_discount"]

        else:
            return Response.error("Invalid order_type specified.")

        res = requests.post(endpoint, json=payload, headers=headers)
        res.raise_for_status()

        response_data = res.json()
        order_id = None

        if order_type == "complete" and "order" in response_data:
            order_id = response_data.get("order", {}).get("id")
        elif order_type == "draft" and "draft_order" in response_data:
            order_id = response_data.get("draft_order", {}).get("id")

        return Response(
            data=response_data,
            metadata={
                "message": f"Order ({order_type}) created successfully",
                "order_id": order_id
            }
        )

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_details = e.response.json()
                print(f"Shopify API Error: {error_details}")
                return Response.error(f"Shopify API Error: {json.dumps(error_details)}")
            except json.JSONDecodeError:
                return Response.error(f"An error occurred: {e.response.text}")
        return Response.error(str(e))
