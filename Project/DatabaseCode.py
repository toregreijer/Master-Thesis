import sqlite3

sqlite_file = 'the_great_db.sqlite'
field1 = 'datetime'
field2 = 'unit_id'
field3 = 'function'
field4 = 'description'
field5 = 'medium'
field6 = 'value'
field7 = 'unit'
field8 = 'manufacturer'
field9 = 'subunit'
field10 = 'tariff'
field11 = 'storage'
t = 'table'


def open_and_store(m):
    """
    Open a connection to the db and store the provided mbus telegram.
    :param m: the mbus telegram to store
    """
    unit_id = m.fields['id']
    tables = []
    conn, c = connect()
    c.execute('SELECT name FROM sqlite_master WHERE type="table"')
    for item in c.fetchall():
        tables.append(item[0])
    if unit_id in tables:
        print('Table {} exists, nothing new required.'.format(unit_id))
    else:
        print('Table {} does not exist, creating new table.'.format(unit_id))
        c.execute('CREATE TABLE {tn!r} ('
                  '{fn1} DATETIME DEFAULT CURRENT_TIMESTAMP, '
                  '{fn2} TEXT, '
                  '{fn3} TEXT, '
                  '{fn4} TEXT, '
                  '{fn5} TEXT, '
                  '{fn6} TEXT, '
                  '{fn7} TEXT, '
                  '{fn8} TEXT, '
                  '{fn9} TEXT, '
                  '{fn10} TEXT, '
                  '{fn11} TEXT  '
                  ')'
                  .format(tn=unit_id,
                          fn1=field1,
                          fn2=field2,
                          fn3=field3,
                          fn4=field4,
                          fn5=field5,
                          fn6=field6,
                          fn7=field7,
                          fn8=field8,
                          fn9=field9,
                          fn10=field10,
                          fn11=field11))
    for b in m.data_blocks:
        c.execute('INSERT INTO {tn!r} ('
                  '{fn2}, '
                  '{fn3}, '
                  '{fn4}, '
                  '{fn5}, '
                  '{fn6}, '
                  '{fn7}, '
                  '{fn8}, '
                  '{fn9}, '
                  '{fn10}, '
                  '{fn11}) '
                  'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
                  .format(tn=unit_id,
                          fn2=field2,
                          fn3=field3,
                          fn4=field4,
                          fn5=field5,
                          fn6=field6,
                          fn7=field7,
                          fn8=field8,
                          fn9=field9,
                          fn10=field10,
                          fn11=field11
                          ),
                  (
                      m.fields['id'],       # Unit ID
                      b[1],                 # Function
                      b[2],                 # Description
                      m.fields['medium'],   # Medium
                      b[3],                 # Value
                      b[4],                 # Unit
                      m.fields['mf'],       # Manufacturer
                      b[5],                 # Subunit
                      b[6],                 # Tariff
                      b[7],                 # Storage
                  ))
    disconnect(conn)


def connect():
    """ Create a connection to an SQLite database file. """
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    return conn, c


def disconnect(conn):
    """ Commit changes and close connection to the database.
    :param conn: the connection object """
    conn.commit()
    conn.close()
