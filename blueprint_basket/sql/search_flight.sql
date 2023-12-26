select t_id, dep_city, name_airport_dep, ariv_city, name_airport_ariv, dep_date_time ,place, cost
FROM ticket join departure using (d_id) join flight using (f_id)
where dep_city = '$dep_city' and name_airport_dep = '$name_airport_dep' and ariv_city = '$ariv_city'
and  name_airport_ariv = '$name_airport_ariv' and date(dep_date_time)='$dep_date_time' and Fullname_passage is Null
