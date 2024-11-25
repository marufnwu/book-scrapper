from database import MySQLConnection
from scrapers import ScrapedItem
from .image import ImageUploader
from typing import List
import mysql.connector

class ItemUploader:
    def __init__(self) -> None:
        __db = MySQLConnection()
        self.__connection = __db.get_connection()
        self.__cursor = __db.get_cursor()
        
    def get_or_create_category_id(self, category_name):
        # Check if the category exists
        select_sql = "SELECT id FROM categories WHERE name = %s"
        self.__cursor.execute(select_sql, (category_name))
        result = self.__cursor.fetchone()
        
        if result:
            # If found, return the existing ID
            return result[0]
        else:
            # If not found, insert a new category
            print(f"Category not found, creating {category_name}")
            insert_sql = "INSERT INTO categories (name) VALUES (%s)"
            self.__cursor.execute(insert_sql, (category_name))
            
            # Fetch the ID of the newly inserted category
            return self.__cursor.lastrowid    
        
    def upload(self, items : List[ScrapedItem]):
        for item in items:
            print(f"Uploading item {item.name}")
            images = ImageUploader.upload(item.images)
            
            sql = f"SELECT id FROM items WHERE name= %s LIMIT 1"
            self.__cursor.execute(sql, (item.name,))
            result = self.__cursor.fetchone()
            if result:
                print(f"Item already exits, skipping {item.name}")
                continue
            
            #get or create category id
            category_id = self.get_or_create_category_id(item.category_name)

            
            val = (
                category_id, item.name, item.slug, item.sku, item.tags, item.sort_details,
                item.specification_name, item.specification_description, item.is_specification, item.details,
                images[0] if images else None,  # Use the first uploaded image as `photo`
                images[0] if images[0] else None,  # Use the second image as `thumbnail`
                item.discount_price, item.previous_price, item.stock, item.meta_keywords,
                item.meta_description, item.status, item.item_type
            )
            
            sql = """INSERT INTO items (
            category_id, name, slug, sku, tags, sort_details, specification_name, specification_description,
            is_specification, details, photo, thumbnail, discount_price, previous_price, stock,
            meta_keywords, meta_description, status, item_type
             ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
             
             
            try:
                self.__cursor.execute(sql, val)
                item_id = self.__cursor.lastrowid

                # Prepare the bulk insert for `galleries`
                if images:  # Ensure there are images to insert
                    gallery_sql = "INSERT INTO galleries (item_id, photo) VALUES (%s, %s)"
                    gallery_vals = [(item_id, image) for image in images]

                    # Execute batch insert
                    self.__cursor.executemany(gallery_sql, gallery_vals)
                
                self.__connection.commit()
                print(f"Rows affected: {self.__cursor.rowcount}")
            except mysql.connector.Error as err:
                print(f"Error executing query: {err}")           
        