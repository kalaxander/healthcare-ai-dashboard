import sqlite3
import re
# Assuming your llm_engine.py exposes a function like generate_sql_response
try:
    from llm_engine import generate_sql_response 
except ImportError:
    # Fallback definition so the script can run independently for testing
    def generate_sql_response(prompt):
        print("[Mock LLM] Generating mock response for testing...")
        return "```sql\nSELECT p.name, c.condition FROM patients p JOIN clinical_records c ON p.patient_id = c.patient_id WHERE c.status = 'Critical';\n```"

# ... existing code ...
DB_PATH = "healthcare.db"

def get_database_schema():
    """
    Dynamically extracts the schema from the SQLite database.
    """
    schema_str = ""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            schema_str += f"\nTable: {table_name}\n"
            
            # Get columns
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            col_details = []
            for col in columns:
                col_name = col[1]
                col_type = col[2]
                is_pk = " PRIMARY KEY" if col[5] == 1 else ""
                col_details.append(f"{col_name} ({col_type}{is_pk})")
            schema_str += f"Columns: {', '.join(col_details)}\n"
            
            # Get foreign keys
            cursor.execute(f"PRAGMA foreign_key_list({table_name});")
            fks = cursor.fetchall()
            for fk in fks:
                schema_str += f"Foreign Key: {table_name}.{fk[3]} = {fk[2]}.{fk[4]}\n"
                
        conn.close()
    except Exception as e:
        return f"Error reading schema: {e}"
        
    return schema_str.strip()

def extract_sql(llm_output):
    """
    Dynamically extracts the schema from the SQLite database.
    """
    schema_str = ""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            schema_str += f"\nTable: {table_name}\n"
            
            # Get columns
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            col_details = []
            for col in columns:
                col_name = col[1]
                col_type = col[2]
                is_pk = " PRIMARY KEY" if col[5] == 1 else ""
                col_details.append(f"{col_name} ({col_type}{is_pk})")
            schema_str += f"Columns: {', '.join(col_details)}\n"
            
            # Get foreign keys
            cursor.execute(f"PRAGMA foreign_key_list({table_name});")
            fks = cursor.fetchall()
            for fk in fks:
                schema_str += f"Foreign Key: {table_name}.{fk[3]} = {fk[2]}.{fk[4]}\n"
                
        conn.close()
    except Exception as e:
        return f"Error reading schema: {e}"
        
    return schema_str.strip()


def extract_sql(llm_output):
    """
    Extracts the SQL query from the LLM's raw text output using regex.
    """
    md_pattern = r"```(?:sql|sqlite)?\s*(.*?)\s*```"
    match = re.search(md_pattern, llm_output, re.IGNORECASE | re.DOTALL)
    
    if match:
        return match.group(1).strip()
    
    raw_pattern = r"(SELECT.*?;)"
    match = re.search(raw_pattern, llm_output, re.IGNORECASE | re.DOTALL)
    
    if match:
        return match.group(1).strip()
        
    return None

def execute_and_print_query(query):
    """
    Executes the cleaned SQL query safely against SQLite and prints tabular results.
    """
    conn = None
    try:
        # Connect to the local SQLite database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Extract column names from the cursor description for the header
        col_names = [description[0] for description in cursor.description]
        
        print("\n" + "="*50)
        print(" QUERY RESULTS")
        print("="*50)
        
        # Basic tabular formatting
        header = " | ".join(f"{col:<15}" for col in col_names)
        print(header)
        print("-" * len(header))
        
        if not results:
            print("No records found.")
        else:
            for row in results:
                print(" | ".join(f"{str(item):<15}" for item in row))
                
        print("="*50 + "\n")
        
    except sqlite3.Error as e:
        print(f"\n[!] SQLite Execution Error: {e}")
    finally:
        if conn:
            conn.close()

def main():
    # 1. Define the user's natural language request
    user_query = "Show me the names and conditions of patients who are in critical condition"
    print(f"User Request: '{user_query}'\n")
    
    # 2. Build the prompt with the schema
    schema = get_database_schema()
    prompt = f"""You are an expert SQL assistant. Given the following SQLite database schema:
    {schema}
    
    Write a valid SQLite query to answer the following request:
    "{user_query}"
    
    Return ONLY the SQL code. Do not include any explanations.
    """
    
    # 3. Pass to the LLM (Integration with llm_engine.py)
    print("Sending prompt to Qwen2.5-Coder-1.5B...")
    
    raw_llm_response = generate_sql_response(prompt)
    
    # 4. Extract and clean the SQL
    print("Extracting SQL...")
    sql_query = extract_sql(raw_llm_response)
    
    if sql_query:
        print(f"\n[+] Extracted Query:\n{sql_query}")
        # 5. Execute against DB
        execute_and_print_query(sql_query)
    else:
        print("\n[-] Error: Could not extract a valid SQL query from the LLM output.")
        print(f"Raw Output:\n{raw_llm_response}")

if __name__ == "__main__":
    main()