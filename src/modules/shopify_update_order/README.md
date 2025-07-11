# Shopify - Update Order

## Description
Allows updating a Shopify order — cancel it, cancel fulfillment, or place on hold.

## Inputs
- **Shopify Store Domain** (required)
- **Access Token** (required)
- **Select Order** (required): Choose the order to update
- **Order Update Action** (required): Options:
  - Cancel Order
  - Cancel Fulfillment
  - Put Fulfillment Order On Hold
- **Select Fulfillment Order ID** (required if applicable)
- **Hold Reason** (required only for hold status)
- **Hold Reason Notes** (optional)

## Behavior
- Dynamic UI visibility and validation depending on `Order Update Action`.
