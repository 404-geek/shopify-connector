# Shopify - Create Order

## Description
Creates a new Shopify order using customer email, shipping address, and product line items. Also supports pasting the complete order JSON.

## Inputs
- **Shopify Store Domain** (required): e.g., `stacksync.myshopify.com`
- **Access Token** (required): Shopify Admin API access token
- **Order Mode** (required): Select between structured form or raw JSON (`structured`, `raw_json`)
- **Order Type** (required): Choose `draft` or `completed`
- **Customer Email** (optional): Customer's email address
- **Shipping Address** (optional): 
  - Full Name
  - Address Line 1
  - City
  - Country
  - Zip Code
- **Product Items list JSON** (optional): Format:
  ```json
  [
    { "variant_id": 51474829574433, "quantity": 1 }
  ]
  ```
- **Raw Order JSON** (optional): Full Shopify order payload

## Notes
- If `Order Mode` is `structured`, the structured fields will be used.
- If `Order Mode` is `raw_json`, only `Raw Order JSON` is used.
