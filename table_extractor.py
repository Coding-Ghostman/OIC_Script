import pdfplumber
import pandas as pd
import base64
import io


def merge_rows(df):
    try:
        df.reset_index(drop=True, inplace=True)  # Reset index to start from 0
        merged_df = df.groupby((df.index - 1) // 2).agg(lambda x: " ".join(map(str, x)))
        return merged_df[1:]
    except:
        print("Exception in Merge Rows")
        return df


def config_headers(merged_list):
    try:
        prefixes = ["local", "trans", "inter", "tarmac", "ect"]
        prefix = ""
        new = []
        occurance = 0
        for i, item in enumerate(merged_list):
            if item == "SL Wt":
                prefix = ""

            if item in "Bulk Wt":
                occurance = occurance + 1
                prefix = prefixes[occurance - 1]
            item = prefix + item
            new.append(item)
        return new
    except:
        print("Exception in Config Headers")
        return merged_list


def remove_duplicates_replace_empty(df, column_name):
    try:
        # Copy the original DataFrame to avoid modifying the original
        df_copy = df.copy()

        # Find duplicate values in the specified column
        duplicates_mask = df_copy.duplicated(subset=[column_name], keep="first")

        # Replace duplicate values with empty string
        df_copy.loc[duplicates_mask, column_name] = ""
        return df_copy
    except:
        print("Exception in Remove Duplicates Replace Empty")
        return df


def table_to_base64(pdf_content):
    main_df = pd.DataFrame()
    with pdfplumber.open(io.BytesIO(pdf_content)) as pdf:
        for i in range(2, 5):
            page = pdf.pages[i]
            tables = page.extract_tables(
                table_settings={
                    "vertical_strategy": "explicit",
                    "horizontal_strategy": "text",
                    "explicit_vertical_lines": [
                        14,
                        34,
                        91,
                        158,
                        215,
                        266,
                        318,
                        368,
                        416,
                        472,
                        510,
                        554,
                        598,
                        640,
                        686,
                        732,
                        774,
                        818,
                        870,
                        918,
                        978,
                        1010,
                        1050,
                        1110,
                    ],
                    "min_words_horizontal": 10,
                    "explicit_horizontal_lines": [153, 609],
                    "snap_y_tolerance": 4,
                    "intersection_x_tolerance": 10,
                }
            )
            list1 = tables[0][0]
            list2 = tables[0][1]
            merged_list = [
                list1[i] + "" + list2[i] for i in range(len(list1))
            ]  # Added space between elements
            merged_list = config_headers(merged_list)
            df = pd.DataFrame(tables[0][2:], columns=merged_list)
            main_df = pd.concat([main_df, df], ignore_index=True)

    # Additional operations on main_df
    try:
        df = main_df.iloc[-2]
        df["S/N"] = ""
        df["Flt Date /Flt No"] = "T" + df["Flt Date /Flt No"]
        main_df = main_df.iloc[:-2]
        main_df = remove_duplicates_replace_empty(main_df, "S/N")
        main_df = merge_rows(main_df)
        main_df = pd.concat([main_df, df.set_axis(main_df.columns).to_frame().T])
    except:
        print("Exception in Additional Operations")

    try:
        # Convert DataFrame to CSV and then to base64
        csv_data = main_df.to_csv(index=False).encode("utf-8")
        base64_content = base64.b64encode(csv_data).decode("utf-8")
        return base64_content
    except:
        print("Exception in Convert DataFrame to CSV and then to base64")
