# Shopify Connector – Stacksync Integration

This custom Shopify connector enables seamless integration with your Shopify store through Stacksync workflows. It supports dynamic content loading and multiple operations across Products and Orders.

---

## ✅ Modules Included

1. **Update Variant Price**
2. **Update Order Notes/Tags**
3. **Create Order**

---

## Setup Requirements

To use any module, you must supply:

| Field         | Required | Description |
|---------------|----------|-------------|
| `shop_domain` | ✅       | Your Shopify store domain (e.g. `yourstore.myshopify.com`) |
| `access_token`| ✅       | Your private app token with the necessary Admin API scopes |

### Required Shopify API Scopes

| Scope             | Required for                      |
|------------------|------------------------------------|
| `read_products`  | Fetching products and variants     |
| `write_products` | Updating variant prices            |
| `read_orders`    | Fetching order list                |
| `write_orders`   | Creating or updating orders        |

---

## 🔄 Module: Update Variant Price

### Description:
Dynamically select a product → variant, view its current price inline, and update it.

### Inputs:

| Field          | Type    | Required | Description |
|----------------|---------|----------|-------------|
| `shop_domain`  | string  | ✅       | Shopify store domain |
| `access_token` | string  | ✅       | Admin token |
| `product`      | object  | ✅       | Dropdown – populated via `/products.json` |
| `variant`      | object  | ✅       | Dropdown – populated from selected product |
| `new_price`    | string  | ✅       | New price to apply |

> 💡 Variant dropdown shows current price like: `Small – $12.99`

---

## 🧾 Module: Update Order Notes/Tags

### Description:
Fetch a list of orders and allow editing of `note` and `tags` for a selected order.

### Inputs:

| Field          | Type    | Required | Description |
|----------------|---------|----------|-------------|
| `shop_domain`  | string  | ✅       | Shopify store domain |
| `access_token` | string  | ✅       | Admin token |
| `order`        | object  | ✅       | Dropdown of recent orders |
| `note`         | string  | ❌       | Optional note to add or update |
| `tags`         | string  | ❌       | Optional comma-separated tags |

> 📝 Uses `PUT /admin/api/2023-10/orders/{id}.json`

---

## 🆕 Module: Create Order

### Description:
Programmatically create a new order for a customer with selected product variants and quantities.

### Inputs:

| Field             | Type   | Required | Description |
|------------------|--------|----------|-------------|
| `shop_domain`    | string | ✅       | Shopify store domain |
| `access_token`   | string | ✅       | Admin token |
| `customer_email` | string | ✅       | Email of the buyer |
| `line_items`     | string (JSON) | ✅ | A JSON array of `variant_id` + `quantity` |
| `note`           | string | ❌       | Optional order note |
| `tags`           | string | ❌       | Comma-separated optional tags |

### Example format for `line_items`:

```json
[
  { "variant_id": 123456789, "quantity": 2 },
  { "variant_id": 987654321, "quantity": 1 }
]
