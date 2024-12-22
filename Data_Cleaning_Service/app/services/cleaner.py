import pandas as pd
import os
import uuid

from Data_Cleaning_Service.app.db.config import RAW_DATA_PATH, CLEANED_DATA_PATH


def merge_to_one_csv(global_file, rand_file, output_file):
    """
    Merges two terrorism CSV files into one unified CSV file with additional fields and replaces all eventid with UUIDs.
    Ensures that missing data is filled with appropriate default values.
    """
    print(f"Processing and Merging Files: {global_file}, {rand_file}")

    # File paths
    global_file_path = os.path.join(RAW_DATA_PATH, global_file)
    rand_file_path = os.path.join(RAW_DATA_PATH, rand_file)

    try:
        # Load Global Terrorism Database CSV
        global_data = pd.read_csv(global_file_path, encoding='iso-8859-1')

        # Handle split date fields in global_data
        global_data['date'] = global_data.apply(
            lambda row: f"{int(row['iyear']):04d}-{int(row['imonth']):02d}-{int(row['iday']):02d}"
            if pd.notna(row['iyear']) and pd.notna(row['imonth']) and pd.notna(row['iday'])
            else pd.NA,
            axis=1
        )

        # Replace all `eventid` with new UUIDs
        global_data['eventid'] = global_data.apply(lambda _: str(uuid.uuid4()), axis=1)

        # Drop the original date-related columns
        global_data.drop(columns=['iyear', 'imonth', 'iday'], inplace=True)

        # Load RAND Database CSV
        rand_data = pd.read_csv(rand_file_path, encoding='iso-8859-1')

        # Standardize RAND columns to match Global Terrorism Database
        additional_columns = {
            'eventid': None,  # Will be handled separately
            'region_txt': "Unknown",
            'latitude': pd.NA,
            'longitude': pd.NA,
            'attacktype1_txt': "Unknown",
            'attacktype2_txt': "Unknown",
            'targtype1_txt': "Unknown",
            'targtype2_txt': "Unknown",
            'targtype3_txt': "Unknown",
            'targsubtype1_txt': "Unknown",
            'targsubtype2_txt': "Unknown",
            'targsubtype3_txt': "Unknown",
            'gsubname': "Unknown",
            'gname2': "Unknown",
            'gsubname2': "Unknown",
            'success': False,
            'suicide': False,
            'extended': False,
            'motive': "Unknown",
            'target1': "Unknown"
        }
        rand_data = rand_data.rename(columns={
            'Date': 'date',
            'City': 'city',
            'Country': 'country_txt',
            'Perpetrator': 'gname',
            'Weapon': 'weaptype1_txt',
            'Injuries': 'nwound',
            'Fatalities': 'nkill',
            'Description': 'summary'
        })

        # Add missing columns to RAND data with default values
        for col, default_value in additional_columns.items():
            if col not in rand_data.columns:
                rand_data[col] = default_value

        # Replace all `eventid` in RAND data with new UUIDs
        rand_data['eventid'] = rand_data.apply(lambda _: str(uuid.uuid4()), axis=1)

        # Combine both datasets into one
        combined_data = pd.concat([global_data, rand_data], ignore_index=True)

        # Fill missing values
        combined_data.fillna({
            'region_txt': "Unknown",
            'city': "Unknown",
            'country_txt': "Unknown",
            'latitude': 0,
            'longitude': 0,
            'attacktype1_txt': "Unknown",
            'attacktype2_txt': "Unknown",
            'targtype1_txt': "Unknown",
            'targtype2_txt': "Unknown",
            'targtype3_txt': "Unknown",
            'targsubtype1_txt': "Unknown",
            'targsubtype2_txt': "Unknown",
            'targsubtype3_txt': "Unknown",
            'gname': "Unknown",
            'gsubname': "Unknown",
            'gname2': "Unknown",
            'gsubname2': "Unknown",
            'motive': "Unknown",
            'target1': "Unknown",
            'success': False,
            'suicide': False,
            'extended': False,
            'nkill': 0,
            'nwound': 0
        }, inplace=True)

        # Clean combined data
        combined_data['date'] = pd.to_datetime(combined_data['date'], errors='coerce')
        combined_data['nkill'] = combined_data['nkill'].fillna(0).astype(int)
        combined_data['nwound'] = combined_data['nwound'].fillna(0).astype(int)

        # Select and order relevant columns
        final_data = combined_data[[  # Expanded to include all requested fields
            'eventid', 'date', 'country_txt', 'region_txt', 'city', 'latitude', 'longitude',
            'attacktype1_txt', 'attacktype2_txt',
            'targtype1_txt', 'targtype2_txt', 'targtype3_txt',
            'targsubtype1_txt', 'targsubtype2_txt', 'targsubtype3_txt',
            'gname', 'gsubname', 'gname2', 'gsubname2',
            'success', 'suicide', 'extended', 'motive',
            'target1', 'weaptype1_txt', 'nkill', 'nwound', 'summary'
        ]]

        # Save the combined file
        output_path = os.path.join(CLEANED_DATA_PATH, output_file)
        final_data.to_csv(output_path, index=False)
        print(f"Merged data saved to: {output_path}")
        return output_path

    except Exception as e:
        print(f"Error processing and merging files: {e}")
        return None

if __name__ == "__main__":
    # Example usage
    # merge_to_one_csv(
    #     "globalterrorismdb_0718dist-1000 rows.csv",
    #     "RAND_Database_of_Worldwide_Terrorism_Incidents - 5000 rows.csv",
    #     "merged_terrorism_data.csv"
    # )




    merge_to_one_csv(
        "global_terrorism_db.csv",
        "RAND_Database_of_Worldwide_Terrorism_Incidents.csv",
        "merged_terrorism_big_data.csv"
    )