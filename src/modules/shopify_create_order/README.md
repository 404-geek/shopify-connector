-----

# Shopify - Create Order

## Description

Creates a new **draft** or **complete** order in a Shopify store. This action uses customer details, shipping address, and line items to build the order. Additional options for financial status, discounts, and notifications are available depending on the selected order type.

-----

## Inputs

  - **Shopify Store Domain** (required): Your Shopify store's domain (e.g., `your-store.myshopify.com`).
  - **Admin API Access Token** (required): Your Shopify Admin API access token. The token should be kept secure.
  - **Order Type** (required): Choose the type of order to create.
      - `draft`: Creates a draft order.
      - `complete`: Creates a finalized order.
  - **Customer** (required): An object containing the customer's information.
      - `first_name`
      - `last_name`
      - `email`
  - **Line Items** (required): A list of products to include in the order. At least one line item is required.
    ```json
    [
      { "variant_id": "gid://shopify/ProductVariant/123456789", "quantity": 1 }
    ]
    ```
  - **Shipping Address** (optional): An object for the customer's shipping address.
      - `first_name`
      - `last_name`
      - `address1`
      - `city`
      - `province`
      - `country`
      - `zip`
  - **Financial Status** (optional): The order's financial status. **Used for 'Complete Orders' only**.
  - **Currency** (optional): The three-letter currency code (e.g., `USD`). **Used for 'Complete Orders' only**.
  - **Send Receipt** (optional): If true, sends an order receipt to the customer. **Used for 'Complete Orders' only**.
  - **Applied Discount** (optional): An object representing a discount. **Used for 'Draft Orders' only**.
    ```json
    {
        "description": "Summer Sale",
        "value": "10.0",
        "title": "10% Off"
    }
    ```
  - **Send Invoice** (optional): If true, sends an invoice for the draft order. **Used for 'Draft Orders' only**.

-----

## Outputs

  - **data**: The full JSON object returned by the Shopify API for the newly created order.
  - **metadata**: An object containing a success message and the `order_id` of the created order.
    ```json
    {
      "message": "Order (complete) created successfully",
      "order_id": 51474829574433
    }
    ```