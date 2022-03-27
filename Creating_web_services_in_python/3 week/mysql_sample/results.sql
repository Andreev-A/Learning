use test
set names utf8;

-- 1. Выбрать все товары (все поля)
SELECT * FROM product

-- 2. Выбрать названия всех автоматизированных складов
SELECT name FROM store WHERE is_automated = 1

-- 3. Посчитать общую сумму в деньгах всех продаж
SELECT SUM(total) FROM sale

-- 4. Получить уникальные store_id всех складов, с которых была хоть одна продажа
SELECT DISTINCT store_id FROM sale

-- 5. Получить уникальные store_id всех складов, с которых не было ни одной продажи
SELECT store_id FROM store WHERE store_id NOT IN (SELECT DISTINCT store_id FROM sale)

-- 6. Получить для каждого товара название и среднюю стоимость единицы товара avg(total/quantity), если товар не продавался, он не попадает в отчет.
SELECT product.name, AVG(total/quantity) FROM sale JOIN product ON product.product_id = sale.product_id GROUP BY product.name

-- 7. Получить названия всех продуктов, которые продавались только с единственного склада
SELECT product.name FROM sale JOIN product ON product.product_id = sale.product_id GROUP BY product.name HAVING COUNT(DISTINCT store_id) = 1

-- 8. Получить названия всех складов, с которых продавался только один продукт
SELECT store.name FROM sale JOIN store ON sale.store_id = store.store_id GROUP BY store.name HAVING COUNT(DISTINCT product_id) = 1

-- 9. Выберите все ряды (все поля) из продаж, в которых сумма продажи (total) максимальна (равна максимальной из всех встречающихся)
SELECT * FROM sale WHERE total = (SELECT MAX(total) FROM sale)

-- 10. Выведите дату самых максимальных продаж, если таких дат несколько, то самую раннюю из них
SELECT date FROM sale GROUP BY date ORDER BY SUM(total) DESC limit 1

-- #####################################################################################################################
-- Решение задания от преподавателей по MySQL
-- #####################################################################################################################
use test
set names uft8;

-- 1. Выбрать все товары (все поля)
select * from product

-- 2. Выбрать названия всех автоматизированных складов
select name from store where is_automated = 1

-- 3. Посчитать общую сумму в деньгах всех продаж
select sum(total) from sale

-- 4. Получить уникальные store_id всех складов, с которых была хоть одна продажа
select distinct(store_id) from sale

-- 5. Получить уникальные store_id всех складов, с которых не было ни одной продажи
select store_id from store natural left join sale where sale.store_id is null

-- 6. Получить для каждого товара название и среднюю стоимость единицы товара avg(total/quantity), если товар не продавался, он не попадает в отчет.
select name, avg(total/quantity) from product natural join sale group by product_id


-- 7. Получить названия всех продуктов, которые продавались только с единственного склада
select name from product natural join sale group by product_id having count(distinct store_id) = 1

-- 8. Получить названия всех складов, с которых продавался только один продукт
select name from store natural join sale group by store_id having count(distinct product_id) = 1

-- 9. Выберите все ряды (все поля) из продаж, в которых сумма продажи (total) максимальна (равна максимальной из всех встречающихся)
select * from sale where total = (select max(total) from sale);

-- 10. Выведите дату самых максимальных продаж, если таких дат несколько, то самую раннюю из них
select date from sale group by date order by sum(total) DESC, date ASC LIMIT 1
