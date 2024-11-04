-- Q4
select c.customer_name,
       count(o.order_id) order_counts
from public.orders o
         join public.customers c
              on c.customer_id = o.customer_id
group by c.customer_name;
-- Q5
select c.customer_name,
       sum(o.amount) order_amount
from public.orders o
         join public.customers c
              on c.customer_id = o.customer_id
where c.country = 'USA'
group by c.customer_name;
-- Q6
select c.customer_name,
       sum(o.amount) order_amount
from public.orders o
         join public.customers c
              on c.customer_id = o.customer_id
group by c.customer_name
order by order_amount desc
limit 3;
-- Q7
select c.country,
       count(distinct c.customer_id) users_counts,
       sum(o.amount)                 order_amount
from public.orders o
         join public.customers c
              on c.customer_id = o.customer_id
group by c.country;