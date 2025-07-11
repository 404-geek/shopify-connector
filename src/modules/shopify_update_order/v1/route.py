import requests
from flask import request as flask_request
from workflows_cdk import Response, Request
from main import router


import requests
from flask import request as flask_request
from workflows_cdk import Response, Request
from main import router


@router.route("/content", methods=["POST"])
def content():
    try:
        req = Request(flask_request)
        data = req.data
        form_data = data.get("form_data", {})
        content_object_names = data.get("content_object_names", [])
        content_objects = []

        shop_domain = form_data.get("shop_domain")
        access_token = form_data.get("access_token")

        if isinstance(content_object_names, list) and content_object_names and isinstance(content_object_names[0], dict):
            content_object_names = [obj.get("id") for obj in content_object_names if "id" in obj]

        if not shop_domain or not access_token:
            return Response(data={"content_objects": content_objects})

        headers = {
            "X-Shopify-Access-Token": access_token,
            "Content-Type": "application/json"
        }

        if "orders" in content_object_names:
            url = f"https://{shop_domain}/admin/api/2023-10/orders.json?limit=50"
            res = requests.get(url, headers=headers)
            res.raise_for_status()
            orders = res.json().get("orders", [])

            order_choices = [
                {
                    "value": {"id": str(order["id"]), "label": order["name"]},
                    "label": f"{order['name']} — {order['created_at'][:10]}"
                }
                for order in orders
            ]

            content_objects.append({
                "content_object_name": "orders",
                "data": order_choices
            })

        return Response(data={"content_objects": content_objects})

    except Exception as e:
        return Response.error(str(e))


@router.route("/execute", methods=["POST"])
def execute():
    try:
        req = Request(flask_request)
        data = req.data

        shop_domain = data.get("shop_domain")
        access_token = data.get("access_token")
        update_action = data.get("update_action")

        headers = {
            "X-Shopify-Access-Token": access_token,
            "Content-Type": "application/json"
        }

        if not shop_domain or not access_token or not update_action:
            return Response.error("Missing required parameters.")

        # Extract order info
        order = data.get("order", {})
        order_id = order.get("id")

        if update_action == "cancel_order":
            if not order_id:
                return Response.error("Order ID is required for cancelling the order.")

            url = f"https://{shop_domain}/admin/api/2023-10/orders/{order_id}/cancel.json"
            res = requests.post(url, headers=headers, json={})
            res.raise_for_status()

            return Response(
                data=res.json(),
                metadata={"message": f"Order {order_id} cancelled successfully."}
            )

        elif update_action == "cancel_fulfillment":
            fulfillment_order_id = data.get("fulfillment_order_id")
            if not fulfillment_order_id:
                return Response.error("Fulfillment Order ID is required for cancelling fulfillment.")

            url = f"https://{shop_domain}/admin/api/2023-10/fulfillment_orders/{fulfillment_order_id}/cancel.json"
            res = requests.post(url, headers=headers, json={})
            res.raise_for_status()

            return Response(
                data=res.json(),
                metadata={"message": f"Fulfillment order {fulfillment_order_id} cancelled."}
            )

        elif update_action == "put_on_hold":
            fulfillment_order_id = data.get("fulfillment_order_id")
            hold_reason = data.get("hold_reason", "other")
            reason_notes = data.get("reason_notes", "")

            if not fulfillment_order_id:
                return Response.error("Fulfillment Order ID is required for hold action.")

            url = f"https://{shop_domain}/admin/api/2023-10/fulfillment_orders/{fulfillment_order_id}/hold.json"
            payload = {
                "fulfillment_hold": {
                    "reason": hold_reason,
                    "reason_notes": reason_notes
                }
            }
            res = requests.post(url, headers=headers, json=payload)
            res.raise_for_status()

            return Response(
                data=res.json(),
                metadata={"message": f"Fulfillment order {fulfillment_order_id} put on hold."}
            )

        else:
            return Response.error(f"Unknown update action: {update_action}")

    except Exception as e:
        return Response.error(str(e))