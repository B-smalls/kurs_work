  select t_id, cost, date_sale, flight_number
  from ticket join departure using (d_id)
  where year(date_sale)='$input_year' and month(date_sale)='$input_month';
