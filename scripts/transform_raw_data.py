import polars as pl


def unnest_and_explode(df: pl.DataFrame) -> pl.DataFrame:
    while True:
        struct_cols = [col for col in df.columns if df[col].dtype == pl.Struct]
        list_struct_cols = [col for col in df.columns if df[col].dtype == pl.List(pl.Struct) and (col != 'SalesRankings' and col != 'CompetitivePricing_NumberOfOfferListings')]
        
        if not struct_cols and not list_struct_cols:
            break
        
        for col in struct_cols:
            df = df.with_columns(pl.col(col).name.map_fields(lambda s: str(col) + '_' + s)).unnest(str(col))
        
        for col in list_struct_cols:
            df = df.explode(col)
    
    return df
