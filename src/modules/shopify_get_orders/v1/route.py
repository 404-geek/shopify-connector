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
        limit = data.get("limit", 5)

        url = f"https://{shop_domain}/admin/api/2024-04/orders.json?limit={limit}"
        headers = {
            "X-Shopify-Access-Token": access_token,
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        orders = response.json().get("orders", [])

        # Filtered output
        result = []
        for order in orders:
            simplified = {
                "order_id": order.get("id"),
                "order_number": order.get("order_number"),
                "email": order.get("email"),
                "financial_status": order.get("financial_status"),
                "total_price": order.get("total_price"),
                "currency": order.get("currency"),
                "created_at": order.get("created_at"),
                "line_items": [
                    {
                        "name": item.get("name"),
                        "quantity": item.get("quantity"),
                        "price": item.get("price")
                    } for item in order.get("line_items", [])
                ]
            }
            result.append(simplified)

        return Response(
            data={"orders": result},
            metadata={"fetched_order_count": len(result)}
        )

    except Exception as e:
        return Response.error(str(e))
