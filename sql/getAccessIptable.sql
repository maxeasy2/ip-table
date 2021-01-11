SELECT seq, ip
from ip_table
where value = 'Y'
limit :rowcnt offset :offset