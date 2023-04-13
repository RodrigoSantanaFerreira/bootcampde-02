--Querys no Athena

-- Clientes com mais vendas
    SELECT c.name, SUM(o.total) as total_sales
    FROM processed_orders o
    JOIN processed_customers c ON o.customer_id = c.id
    GROUP BY c.name
    ORDER BY total_sales DESC;

-- Categorias mais vendidas
    SELECT p.category, SUM(o.total) as total_sales
    FROM processed_orders o
    JOIN processed_products p ON o.product_id = p.id
    GROUP BY p.category
    ORDER BY total_sales DESC;

-- Número de pedidos por cliente em ordem decrescente:

    SELECT processed_customers.name, COUNT(processed_orders.id) AS num_orders
    FROM processed_orders
    JOIN processed_customers ON processed_orders.customer_id = processed_customers.id
    GROUP BY processed_customers.name
    ORDER BY num_orders DESC;

-- Média de gastos por pedido em ordem decrescente de média:

    SELECT processed_customers.name, AVG(processed_orders.total) AS avg_order_total
    FROM processed_orders
    JOIN processed_customers ON processed_orders.customer_id = processed_customers.id
    GROUP BY processed_customers.name
    ORDER BY avg_order_total DESC;

-- Quantidade total de produtos vendidos por categoria de produto em ordem decrescente:

    SELECT processed_products.category, SUM(processed_orders.quantity) AS total_quantity
    FROM processed_orders
    JOIN processed_products ON processed_orders.product_id = processed_products.id
    GROUP BY processed_products.category
    ORDER BY total_quantity DESC;