from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
from app.core.config import settings


_connections_ready = False


def ensure_connection() -> None:
    global _connections_ready
    if _connections_ready:
        return
    connections.connect(
        alias="default",
        host=settings.MILVUS_HOST,
        port=settings.MILVUS_PORT,
    )
    _connections_ready = True


def get_or_create_memory_collection() -> Collection:
    ensure_connection()

    if utility.has_collection(settings.MILVUS_COLLECTION):
        collection = Collection(settings.MILVUS_COLLECTION)
        collection.load()
        return collection

    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="project_id", dtype=DataType.INT64),
        FieldSchema(name="source_type", dtype=DataType.VARCHAR, max_length=50),
        FieldSchema(name="source_ref", dtype=DataType.INT64),
        FieldSchema(name="chunk_type", dtype=DataType.VARCHAR, max_length=50),
        FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=8192),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=settings.EMBEDDING_DIM),
    ]
    schema = CollectionSchema(fields=fields, description="Novel memory chunks")
    collection = Collection(name=settings.MILVUS_COLLECTION, schema=schema)

    index_params = {
        "metric_type": "COSINE",
        "index_type": "IVF_FLAT",
        "params": {"nlist": 128},
    }
    collection.create_index(field_name="embedding", index_params=index_params)
    collection.load()
    return collection
