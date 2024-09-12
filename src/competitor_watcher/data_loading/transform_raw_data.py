import json
import polars as pl


def unnest_and_explode(df: pl.DataFrame) -> pl.DataFrame:
    while True:
        struct_cols = [col for col in df.columns if df[col].dtype == pl.Struct]
        list_struct_cols = [col for col in df.columns if df[col].dtype == pl.List(pl.Struct) and (col != 'SalesRankings' and col != 'NumberOfOfferListings')]
        
        if not struct_cols and not list_struct_cols:
            break
        
        for col in struct_cols:
            df = df.with_columns(pl.col(col).name.map_fields(lambda s: str(col) + '_' + s)).unnest(str(col))
        
        for col in list_struct_cols:
            df = df.explode(col)
    
    return df


def generate_schema_from_pl(polars_df: pl.DataFrame, list_struct_cols: list) -> str:
    schema = ""

    for col in polars_df.columns:
        if col in list_struct_cols:
            schema += f"{col}  JSON,\n"
        elif polars_df[col].dtype == pl.Utf8:
            schema += f"{col}  VARCHAR,\n"
        elif polars_df[col].dtype == pl.Float64:
            schema += f"{col}  FLOAT,\n"
        elif polars_df[col].dtype == pl.Int64:
            schema += f"{col}  INT,\n"
        elif polars_df[col].dtype == pl.Datetime:
            schema += f"{col}  TIMESTAMP,\n"
        elif polars_df[col].dtype == pl.Boolean:
            schema += f"{col}  BOOLEAN,\n"
        elif polars_df[col].dtype == pl.List(pl.Utf8):
            schema += f"{col}  TEXT[],\n"
        elif polars_df[col].dtype == pl.Null:
            schema += f"{col}  VARCHAR,\n"
        else:
            raise TypeError(f"Unknown type {polars_df[col].dtype} for column {col}")

    if schema.endswith(",\n"):
        schema = schema[:-2]
    
    return schema


def transform_pl_df_and_generate_schema(polars_df: pl.DataFrame) -> tuple[pl.DataFrame, str]:

    list_struct_cols = [col for col in polars_df.columns if polars_df[col].dtype == pl.List(pl.Struct)]
    
    for col in list_struct_cols:
        # Extract the column as a list of Python dictionaries (if it's not already in that form)
        data_as_dict = polars_df[col].to_list()

        # Convert each dictionary to a JSON string
        json_data = [json.dumps(item) for item in data_as_dict]

        # Create a new Series from the JSON data
        json_series = pl.Series(col, json_data)

        # Replace the original column with the new Series
        polars_df = polars_df.drop(col).with_columns(json_series)

    schema = generate_schema_from_pl(polars_df, list_struct_cols)
    
    return polars_df, schema


