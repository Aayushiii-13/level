vimport pandas as pd

def transform_levels(df):
    # Extract numeric part from "level X"
    df['level_num'] = df['Split_level'].str.extract(r'(\d+)').astype(int)

    # Apply transformation rules
    df['new_level_num'] = df['level_num'].apply(lambda x: x if x <= 2 else x - 1)

    # Update Split_level
    df['Split_level'] = 'level ' + df['new_level_num'].astype(str)

    # Update parent_level (one level above new split level)
    df['parent_level'] = df['new_level_num'].apply(
        lambda x: '' if x <= 1 else f'level {x-1}'
    )

    # Drop internal helper columns
    df.drop(columns=['level_num', 'new_level_num'], inplace=True)

    return df


# -------------------------------
# MAIN FUNCTION
# -------------------------------

def process_file(input_path, output_path):
    # Read input file (auto-detect CSV or Excel)
    if input_path.endswith('.csv'):
        df = pd.read_csv(input_path)
    else:
        df = pd.read_excel(input_path)

    # Apply transformation
    df_transformed = transform_levels(df)

    # Save output
    if output_path.endswith('.csv'):
        df_transformed.to_csv(output_path, index=False)
    else:
        df_transformed.to_excel(output_path, index=False)

    print(f"Processing complete.\nOutput saved to: {output_path}")


# -------------------------------
# Example Usage
# -------------------------------

input_file = "input.xlsx"      # your input file name
output_file = "output.xlsx"    # desired output file name

process_file(input_file, output_file)
