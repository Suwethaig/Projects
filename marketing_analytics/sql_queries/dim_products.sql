-- Query to categorize products based on their price
-- The redundant 'Category' column has been removed

SELECT 
    ProductID,
    ProductName,
    Price,
    CASE
        WHEN price < 50 THEN 'Low'
        WHEN price BETWEEN 50 AND 200 THEN 'Medium'
        ELSE 'High'
    END AS PriceCategory
FROM 
    dbo.products;
