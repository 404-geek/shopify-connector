import requests

from flask import request as flask_request
from workflows_cdk import Response, Request
from main import router


@router.route("/content", methods=["POST"])
def content():
    try:

        print("Here")


        req = Request(flask_request)
        data = req.data
        form_data = data.get("form_data", {})
        content_object_names = data.get("content_object_names", [])
        content_objects = []

        shop_domain = form_data.get("shop_domain")
        access_token = form_data.get("access_token")

        if isinstance(content_object_names,
                      list) and content_object_names and isinstance(
            content_object_names[0], dict):
            content_object_names = [obj.get("id") for obj in content_object_names if
                                    "id" in obj]


        if not shop_domain or not access_token:
            return Response(data={"content_objects": content_objects})

        headers = {
            "X-Shopify-Access-Token": access_token,
            "Content-Type": "application/json"
        }

        if "products" in content_object_names:
            res = requests.get(f"https://{shop_domain}/admin/api/2023-10/products.json", headers=headers)
            res.raise_for_status()
            products = res.json().get("products", [])

            product_choices = [
                {
                    "value": {
                        "id": str(prod["id"]),
                        "label": prod["title"]  # 🛠 this fixes the dropdown display
                    },
                    "label": prod["title"]
                }
                for prod in products
            ]

            content_objects.append({
                "content_object_name": "products",
                "data": product_choices
            })

        if "variants" in content_object_names:
            selected_product = form_data.get("product", {})
            product_id = selected_product.get("id")

            if product_id:
                res = requests.get(f"https://{shop_domain}/admin/api/2023-10/products/{product_id}/variants.json", headers=headers)
                res.raise_for_status()
                variants = res.json().get("variants", [])

                variant_choices = [
                    {
                        "value": {
                            "id": str(var["id"]),
                            "label": f"{var['title']} – ${var['price']}"
                        },
                        "label": f"{var['title']} – ${var['price']}"
                    }
                    for var in variants
                ]

                content_objects.append({
                    "content_object_name": "variants",
                    "data": variant_choices
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
        variant = data.get("variant", {})
        new_price = data.get("new_price")

        variant_id = variant.get("id")
        if not variant_id:
            return Response.error("Variant ID is missing.")

        url = f"https://{shop_domain}/admin/api/2023-10/variants/{variant_id}.json"
        headers = {
            "X-Shopify-Access-Token": access_token,
            "Content-Type": "application/json"
        }

        payload = {
            "variant": {
                "id": variant_id,
                "price": new_price
            }
        }

        response = requests.put(url, headers=headers, json=payload)
        response.raise_for_status()

        return Response(data=response.json(), metadata={"message": "Price updated successfully"})

    except Exception as e:
        return Response.error(str(e))