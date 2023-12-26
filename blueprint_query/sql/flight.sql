select flight_number, dep_city, ariv_city, dep_date_time, ariv_date_time
from departure join flight using (f_id)
where flight_number ='$input_flight_number'
