-- CREATE DATABASE spare_parts_assessment;

-- CREATE TABLE suppliers (
--     supplier_id INT PRIMARY KEY,
--     supplier_name VARCHAR(100),
--     city VARCHAR(50)
-- );

-- CREATE TABLE parts (
--     part_id INT PRIMARY KEY,
--     part_name VARCHAR(100),
--     category VARCHAR(50),
--     unit_price DECIMAL(10,2),
--     stock_qty INT
-- );

-- CREATE TABLE purchase_orders (
--     po_id INT PRIMARY KEY,
--     supplier_id INT REFERENCES suppliers(supplier_id),
--     order_date DATE,
--     status VARCHAR(30)
-- );

-- CREATE TABLE purchase_order_items (
--     po_item_id INT PRIMARY KEY,
--     po_id INT REFERENCES purchase_orders(po_id),
--     part_id INT REFERENCES parts(part_id),
--     quantity INT
-- );

-- INSERT INTO suppliers VALUES
-- (1,'Axis Components','Rajkot'),
-- (2,'Prime Industrial','Pune'),
-- (3,'Nova Engineering','Coimbatore'),
-- (4,'Delta Supply Works','Bhubaneswar'),
-- (5,'Mektron Systems','Nashik'),
-- (6,'Cobalt Traders','Surat');


-- INSERT INTO parts VALUES
-- (101,'Bearing Set','Mechanical',1250,38),
-- (102,'Control Relay','Electrical',850,60),
-- (103,'Hydraulic Seal','Mechanical',420,95),
-- (104,'Temperature Sensor','Electronics',1850,24),
-- (105,'Drive Belt','Mechanical',760,42),
-- (106,'PLC Module','Electronics',5400,10),
-- (107,'Fuse Pack','Electrical',290,120);

-- INSERT INTO purchase_orders VALUES
-- (1001,1,'2026-10-01','Received'),
-- (1002,2,'2026-10-02','Pending'),
-- (1003,3,'2026-10-03','Received'),
-- (1004,1,'2026-10-05','Pending'),
-- (1005,5,'2026-10-06','Cancelled');

-- INSERT INTO purchase_order_items VALUES
-- (1,1001,101,10),
-- (2,1001,103,20),
-- (3,1002,102,15),
-- (4,1002,104,6),
-- (5,1003,105,12),
-- (6,1003,107,30),
-- (7,1004,106,2),
-- (8,1005,103,10);


-- SELECT * FROM parts WHERE category='Mechanical'

-- SELECT * FROM parts 
-- WHERE unit_price>1000
-- ORDER BY unit_price DESC

-- SELECT category,AVG(unit_price)
-- FROM parts
-- GROUP BY category

-- SELECT category,SUM(stock_qty)
-- FROM parts
-- GROUP BY category

-- SELECT s.supplier_name,po.order_date,po.status
-- FROM suppliers s
-- JOIN purchase_orders po
-- ON s.supplier_id=po.supplier_id

-- SELECT po.po_id,p.part_name,poi.quantity,p.unit_price
-- FROM parts p
-- JOIN purchase_order_items poi
-- on p.part_id=poi.part_id
-- JOIN purchase_orders po
-- ON poi.po_id=po.po_id

-- SELECT po.po_id,p.part_name,poi.quantity,p.unit_price,poi.quantity * p.unit_price AS line_total
-- FROM parts p
-- JOIN purchase_order_items poi
-- on p.part_id=poi.part_id
-- JOIN purchase_orders po
-- ON poi.po_id=po.po_id

-- SELECT s.supplier_id,s.supplier_name,po.po_id
-- FROM suppliers s
-- LEFT JOIN purchase_orders po
-- ON s.supplier_id=po.supplier_id

-- SELECT s.supplier_id,s.supplier_name,po.po_id
-- FROM suppliers s
-- LEFT JOIN purchase_orders po
-- ON s.supplier_id=po.supplier_id 
-- WHERE po.supplier_id IS NULL

-- CREATE VIEW purchase_order_summary AS
-- SELECT po.po_id,s.supplier_name,p.part_name,poi.quantity,p.unit_price,
-- poi.quantity*p.unit_price AS line_total,po.status
-- FROM suppliers s
-- JOIN purchase_orders po
-- ON s.supplier_id=po.supplier_id
-- JOIN purchase_order_items poi
-- ON po.po_id=poi.po_id
-- JOIN parts p
-- ON poi.part_id=p.part_id;

-- SELECT * FROM purchase_order_summary 
-- WHERE status='Pending'

-- CREATE OR REPLACE FUNCTION calculate_part_discount
-- (unit_price DECIMAL)
-- RETURNS DECIMAL
-- LANGUAGE plpgsql
-- AS $$
-- BEGIN
-- 	IF unit_price>=2000 THEN
-- 		RETURN  unit_price *0.10;
-- 	ELSE
-- 		RETURN 0;
-- 	END IF;
-- END;
-- $$;

-- SELECT calculate_part_discount(2000)

-- CREATE OR REPLACE FUNCTION final_part_discount
-- (unit_price DECIMAL)
-- RETURNS DECIMAL
-- LANGUAGE plpgsql
-- AS $$
-- BEGIN
-- 	RETURN unit_price-calculate_part_discount(unit_price);
-- END;
-- $$;

-- -- SELECT final_part_discount(2000)

-- CREATE OR REPLACE PROCEDURE update_po_status
-- (p_po_id INT,
-- p_status VARCHAR)
-- LANGUAGE plpgsql
-- AS $$
-- BEGIN
-- 	UPDATE purchase_orders
-- 	SET status=p_status
-- 	WHERE po_id=p_po_id;
-- END;
-- $$;

-- CALL update_po_status(1005,'Pending');

-- SELECT * FROM purchase_orders


-- SELECT final_part_discount(2000)

CREATE OR REPLACE PROCEDURE mark_old_pending_orders()
LANGUAGE plpgsql
AS $$
BEGIN
	UPDATE purchase_orders
	SET status='Received'
	WHERE status='Pending ' AND  order_date < '2026-10-04';
END;
$$;

CALL mark_old_pending_orders();

SELECT * FROM purchase_orders




