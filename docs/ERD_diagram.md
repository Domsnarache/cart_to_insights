# Entity-Relationship Diagram (ERD) & Schema Architecture

## 1. Relational Architecture Diagram

The Olist e-commerce database contains nine relational tables centered on `orders`, which connects customers, line items, payments, sellers, and reviews.

```mermaid
erDiagram
    CUSTOMERS ||--o{ ORDERS : "places (1:N)"
    ORDERS ||--|{ ORDER_ITEMS : "contains (1:N)"
    ORDERS ||--|{ ORDER_PAYMENTS : "paid_by (1:N)"
    ORDERS ||--o{ ORDER_REVIEWS : "reviewed_in (1:N)"
    PRODUCTS ||--o{ ORDER_ITEMS : "ordered_as (1:N)"
    SELLERS ||--o{ ORDER_ITEMS : "fulfilled_by (1:N)"
    PRODUCT_CATEGORY_TRANSLATION ||--o{ PRODUCTS : "translates (1:N)"
    GEOLOCATION ||--o{ CUSTOMERS : "locates_by_zip (1:N)"
    GEOLOCATION ||--o{ SELLERS : "locates_by_zip (1:N)"

    CUSTOMERS {
        string customer_id PK "Unique per order"
        string customer_unique_id "Identifier across repeated purchases"
        string customer_zip_code_prefix FK
        string customer_city
        string customer_state
    }

    ORDERS {
        string order_id PK
        string customer_id FK
        string order_status
        timestamp order_purchase_timestamp
        timestamp order_approved_at
        timestamp order_delivered_carrier_date
        timestamp order_delivered_customer_date
        timestamp order_estimated_delivery_date
    }

    ORDER_ITEMS {
        string order_id FK
        int order_item_id PK "Line item sequence number"
        string product_id FK
        string seller_id FK
        timestamp shipping_limit_date
        float price
        float freight_value
    }

    ORDER_PAYMENTS {
        string order_id FK
        int payment_sequential PK
        string payment_type
        int payment_installments
        float payment_value
    }

    ORDER_REVIEWS {
        string review_id PK
        string order_id FK
        int review_score
        string review_comment_title
        string review_comment_message
        timestamp review_creation_date
        timestamp review_answer_timestamp
    }

    PRODUCTS {
        string product_id PK
        string product_category_name FK
        int product_name_lenght
        int product_description_lenght
        int product_photos_qty
        float product_weight_g
        float product_length_cm
        float product_height_cm
        float product_width_cm
    }

    SELLERS {
        string seller_id PK
        string seller_zip_code_prefix FK
        string seller_city
        string seller_state
    }

    PRODUCT_CATEGORY_TRANSLATION {
        string product_category_name PK "Portuguese category name"
        string product_category_name_english "English translation"
    }

    GEOLOCATION {
        string geolocation_zip_code_prefix
        float geolocation_lat
        float geolocation_lng
        string geolocation_city
        string geolocation_state
    }
```

---

## 2. Table-by-Table Architectural Description

| Table Name | Primary Role | Key Identifiers (PK / FK) | Business Importance |
| :--- | :--- | :--- | :--- |
| **`orders`** | Core Fact Table | **PK:** `order_id`<br>**FK:** `customer_id` | Tracks lifecycle timestamps (purchase, approval, dispatch, delivery, estimated delivery). |
| **`customers`** | Customer Dimension | **PK:** `customer_id`<br>**Ref:** `customer_unique_id` | Differentiates distinct purchase transactions from repeat unique buyers. |
| **`order_items`** | Line Items Fact Table | **Composite PK:** `(order_id, order_item_id)`<br>**FKs:** `product_id`, `seller_id` | Individual products inside an order, prices, and shipping logistics costs. |
| **`order_payments`** | Payments Fact Table | **Composite PK:** `(order_id, payment_sequential)`<br>**FK:** `order_id` | Payment methods (credit card, boleto, voucher), installments, and paid amounts. |
| **`order_reviews`** | Customer Sentiment | **PK:** `review_id`<br>**FK:** `order_id` | 1-5 star ratings and customer text feedback. Critical for satisfaction analysis. |
| **`products`** | Product Dimension | **PK:** `product_id`<br>**FK:** `product_category_name` | Physical attributes, dimensions, and category classifications. |
| **`sellers`** | Seller Dimension | **PK:** `seller_id` | Seller locations (city, state, zip) for fulfillment route optimization. |
| **`product_category_name_translation`** | Localization Lookup | **PK:** `product_category_name` | Translates Portuguese product taxonomy into standardized English names. |
| **`geolocation`** | Spatial Dimension | **Key:** `geolocation_zip_code_prefix` | Latitudes and longitudes for geographical density and delivery mapping. |

---

## 3. Critical Data Engineering Relationships & Notes

1. `customer_id` vs `customer_unique_id`:
   - In Olist, `customer_id` is assigned per order (ephemeral transaction key).
   - `customer_unique_id` identifies the actual human behind repeat transactions. This distinction is mandatory for repeat customer analysis and customer lifetime value (CLV).

2. Composite keys in line items and payments:
   - Multiple items in a single order share the same `order_id`; they are uniquely indexed by `order_item_id`.
   - Customers can pay using multiple vouchers or mixed payment methods; indexed by `payment_sequential`.

3. Date & timestamp formats:
   - All 5 timestamps in the `orders` table (`purchase`, `approved_at`, `carrier_date`, `delivered_date`, `estimated_delivery_date`) must be cast to `datetime64[ns]` in Pandas / `DATETIME` in SQL for valid delivery duration and delay calculations.
