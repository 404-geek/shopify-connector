import json
import requests
from flask import request as flask_request
from workflows_cdk import Response, Request
from main import router


@router.route("/execute", methods=["POST"])
def execute():
    try:
        req = Request(flask_request)
        data = req.data

        shop_domain = data.get("shop_domain")
        access_token = data.get("access_token")
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
                "line_items": line_items
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

