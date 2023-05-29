def create_collections_if_not_exist(db, collections_name):
	db_collections = list(db.list_collections())
	for coll_name in collections_name:
		collection_exists = list(filter(
			lambda x: x['name'] == coll_name,
			db_collections
		))
		if not collection_exists:
			db.create_collection(name=coll_name)
			print(f'Database: Collection "{coll_name}" created!')




from config import Config
from pymongo import MongoClient

client = MongoClient(Config.MONGODB_URI)
db = client[Config.MONGODB_DB_NAME]
create_collections_if_not_exist(
	db=db,
	collections_name=[
		'users',
		'medias'
	]
)
users = db.users
medias = db.medias


from ._start import start
from ._music import music