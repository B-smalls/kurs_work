select order_id, order_date, dep_city, name_airport_dep, ariv_city, name_airport_ariv,
dep_date_time, ariv_date_time , place, cost
from user_orders join orders_list using (order_id) join ticket using(t_id) join departure using(d_id) join flight using(f_id)
where user_id = '$user_id'