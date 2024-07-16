# Ideas behind a SchemaSet object and representing databases

Just like there is a DataFrame for a single table a, SchemaSet contains data and relationships between tables, and is a searchable, in-memory object that can abstract the work required between them.

All of this work hinges on libraries like DuckDB, Pandas, Polars, and Ibis-framework. 

Like Ibis, we want the DataFrames themselves to be engines we can replace as needed.

The core of every schema is three DataFrames: 'File', 'Entry', and 'Line' -- this can be extended, but it represents the core pieces of a stack trace or log file we wish to break down. See [ER Diagram](./data-structure-notes.md#entity-relationship-diagram) in the data structure notes, for a visualization and more detail.

Each of these entities has relationships between each other that make create precise, flexible, and comprehensive reporting possible.

A SchemaSet helps build each DataFrame and add the relationship between them. Then, feeds these items into DuckDB, where a copy of the database is made and 'cached' on file using SQLite as the db format.

This is a rough idea of how the API might look.

```python

tables = {
    "table1": {
        "columns": {"col1": to_str,"col2": to_float},  
        # all column definitions start with 
        "foreign_keys": {
            "fk_table": "table2", # show table to link to table1
            "fk_column": "id", # indicate the foreign key col
            "local_key": "table2_id" # incide the local key col to match on the foreign key
            "key_binder": foreign_key_builder()  # add the function that can build the foriegn key relationship in each row
            # no need to add foreign key columns to the "columns" key, as those will be appended to the columns list when tables are made

        },
        }
}

df_engine = "pandas"

SchemaSet(tables, df_engine)
```