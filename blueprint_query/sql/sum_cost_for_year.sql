select year(date_sale), sum(cost) from ticket where year(date_sale)='$input_year' group by d_id;

