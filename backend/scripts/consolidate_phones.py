import json
import pymysql
import os
from datetime import datetime

# Database connection details
DB_HOST = "kisanvani_mysql"
DB_USER = "root"
DB_PASS = "rootpassword"
DB_NAME = "kisanvani_db"

def consolidate_phones():
    try:
        # Connect to the database
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )

        with connection.cursor() as cursor:
            print("Fetching organisations...")
            cursor.execute("SELECT id, phone_number, secondary_phone, phone_numbers FROM organisations")
            orgs = cursor.fetchall()

            for org in orgs:
                org_id = org['id']
                legacy_phone = org['phone_number']
                legacy_secondary = org['secondary_phone']
                json_phones = org['phone_numbers']
                
                final_phone = None
                
                # logic to pick the best primary phone
                if legacy_phone:
                    final_phone = legacy_phone
                elif json_phones:
                    try:
                        phones_list = json.loads(json_phones)
                        if phones_list and isinstance(phones_list, list) and len(phones_list) > 0:
                            final_phone = phones_list[0]
                    except:
                        pass
                
                if final_phone:
                    print(f"Updating Org ID {org_id} with phone {final_phone}")
                    cursor.execute(
                        "UPDATE organisations SET phone_numbers = %s WHERE id = %s",
                        (final_phone, org_id)
                    )

            # Alter table to finalize consolidation
            print("Altering table schema...")
            # 1. Change phone_numbers column type to String(20)
            cursor.execute("ALTER TABLE organisations MODIFY COLUMN phone_numbers VARCHAR(20)")
            # 2. Drop legacy columns
            cursor.execute("ALTER TABLE organisations DROP COLUMN phone_number")
            cursor.execute("ALTER TABLE organisations DROP COLUMN secondary_phone")

        connection.commit()
        print("Successfully consolidated phone fields!")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    consolidate_phones()
