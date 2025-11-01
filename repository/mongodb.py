from pymongo import MongoClient
import uuid
from typing import Dict, List

class MongoDBHandler:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="wt", collection_name="latex"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def create_document(self, document_name: str, original_text: str, latex_code: str, user_name: str) -> str:
        """Insert a new document and return its session_id."""
        session_id = str(uuid.uuid4())
        data = {
            "document_name": document_name,
            "session_id": session_id,
            "user_name": user_name,
            "original_text": original_text,
            "latex_code": latex_code,
            "history": []
        }
        try:
            self.collection.insert_one(data)
            return session_id
        except Exception as e:
            raise RuntimeError(e)

    def read_documents(self, query: dict = {}) -> list:
        """Find all documents that match the query."""
        documents = list(self.collection.find(query))
        for doc in documents:
            doc["_id"] = str(doc["_id"])
        return documents

    def read_by_session(self, session_id: str) -> dict | None:
        """Find a single document by its session_id."""
        document = self.collection.find_one({"session_id": session_id})
        if document:
            document["_id"] = str(document["_id"])
        return document

    def update_document(self, session_id: str, updates: dict) -> int:
        """
        Update fields (like original_text or latex_code) for a given session_id.
        Example:
            updates = {"latex_code": "...", "original_text": "..."}
        """
        result = self.collection.update_one(
            {"session_id": session_id},
            {"$set": updates}
        )
        return result.modified_count

    def add_history(self, session_id: str, new_message: dict) -> int:
        """
        Append a new message to the 'history' array.
        new_message format:
        {
            "messageno": int,
            "user_prompt": str,
            "llm_prompt": str
        }
        """
        result = self.collection.update_one(
            {"session_id": session_id},
            {"$push": {"history": new_message}}
        )
        return result.modified_count

    def delete_document(self, session_id: str) -> int:
        """Delete a document by session_id."""
        result = self.collection.delete_one({"session_id": session_id})
        return result.deleted_count

    def drop_collection(self):
        """Drop the entire collection."""
        self.collection.drop()
