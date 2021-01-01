from RunSQL import RunSQL


for i in range(1, 255):
    if i == 10 or i == 172 or i == 192: continue;
    for j in range(1, 255):
        for k in range(1, 255):
            for l in range(1, 255):
                json = {'ip': str(i) + '.' + str(j) + '.' + str(k) + '.' + str(l)}
                RunSQL.save(json, 'insert_iptable.sql')
