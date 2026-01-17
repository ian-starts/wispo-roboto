from functools import lru_cache

from google.cloud import firestore


@lru_cache
def get_firestore_client() -> firestore.Client:
    return firestore.Client()


def set_location(user_id: int, lat: float, long: float) -> None:
    db = get_firestore_client()
    doc_ref = db.collection("locations").document(str(user_id))
    doc_ref.set({"lat": lat, "long": long})


def get_location(user_id: int) -> dict:
    db = get_firestore_client()
    doc_ref = db.collection("locations").document(str(user_id))
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    raise KeyError(f"Location not found for user {user_id}")
