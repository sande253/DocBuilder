from pymongo import MongoClient
from bson.objectid import ObjectId
import uuid 
from typing import List
class MongoDBHandler:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="wt", collection_name="latex"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

   
    def create_document(self, document_name :str , pages :List ,user_name:str) -> str:
        """Insert a new document and return its ID."""
        session_id=str(uuid.uuid4())
        data ={
            "document_name":document_name,
            "session_id":session_id,
            "user_name":user_name,
            "pages":[],
            "history":[]
        }
        try:
          result = self.collection.insert_one(data)
          return session_id
        except Exception as e :
            raise RuntimeError(e)
        

    # Read documents
    def read_documents(self, query: dict = {}) -> list:
        """Find all documents that match the query."""
        documents = list(self.collection.find(query))
        for doc in documents:
            doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
        return documents

    # Read a single document by ID
    def read_documents (self,query:dict={}):
        documents =list(self.collection.find(query))

        for doc in documents :
            doc["_id"]= str (doc["_id"])
        return documents 
    
    def readBySession(self, session_id ):
        documents = list(self.collection({"session_id":session_id}))

        if documents: 
            for doc in documents :
             doc["_id"]= str (doc["_id"])
        return documents 
    


    def read_by_id(self, doc_id: str) -> dict | None:
        """Find a single document by its ObjectId."""
        document = self.collection.find_one({"session_id": ObjectId(doc_id)})
        if document:
            document["_id"] = str(document["_id"])
        return document
    
    def get_pages(self, session_id: str) -> list:
        """
        Retrieve all pages for a given session_id.
        Returns a list of page objects:
        [
            { "pageno": 1, "original_text": "...", "latex_code": "...", "summary": "..." },
            ...
        ]
        """
        doc = self.collection.find_one({"session_id": session_id}, {"_id": 0, "pages": 1})
        return doc.get("pages", []) if doc else []


    def get_page(self, session_id: str, pageno: int) -> dict | None:
        """
        Retrieve a specific page by page number.
        """
        doc = self.collection.find_one(
            {"session_id": session_id, "pages.pageno": pageno},
            {"_id": 0, "pages.$": 1}
        )
        if doc and "pages" in doc:
            return doc["pages"][0]
        return None


    def get_summaries(self, session_id: str) -> list:
        """
        Retrieve only summaries of all pages for a given session_id.
        Returns a list of summaries (strings).
        """
        doc = self.collection.find_one({"session_id": session_id}, {"_id": 0, "pages.summary": 1})
        if not doc or "pages" not in doc:
            return []
        return [page.get("summary", "") for page in doc["pages"]]


    def add_page(self, session_id: str, new_page: dict, position: int | None = None) -> int:
        """
        Insert a new page into the 'pages' array.
        If position is None, append to the end.
        If position is an integer, insert at that index (0-based).
        
        new_page format:
        {
            "pageno": int,
            "original_text": str,
            "latex_code": str,
            "summary": str
        }
        """
        update_query = {
            "$push": {
                "pages": {
                    "$each": [new_page]
                }
            }
        }

        # Add position modifier only if user provides a specific index
        if position is not None:
            update_query["$push"]["pages"]["$position"] = position

        result = self.collection.update_one(
            {"session_id": session_id},
            update_query
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
    
    def update_page(self, session_id: str, page_number: int, updates: dict):
        """
        Update a specific page in the pages array.
        Example: updates = {"latex_code": "...", "summary": "..."}
        """
        update_fields = {f"pages.$.{k}": v for k, v in updates.items()}
        result = self.collection.update_one(
            {"session_id": session_id, "pages.pageno": page_number},
            {"$set": update_fields}
        )
        return result.modified_count

    def update_page_summary(self, session_id: str, pageno: int, new_summary: str) -> int:
        """Update the summary of a specific page by pageno."""
        result = self.collection.update_one(
            {"session_id": session_id, "pages.pageno": pageno},
            {"$set": {"pages.$.summary": new_summary}}
        )
        return result.modified_count
    
    def delete_document(self, session_id: str) -> int:
        """Delete a document by session_id."""
        result = self.collection.delete_one({"session_id": session_id})
        return result.deleted_count

    
    def drop_collection(self):
        """Drop the entire collection."""
        self.collection.drop()


    
