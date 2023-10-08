from database_conn import mongodb

mongodb.connect_db('MapleLeafs')
mongodb.connect_collection('teamDetails')
# mongodb.print_states()
mongodb.close_connection()

