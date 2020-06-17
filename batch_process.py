import pandas as pd
import datetime

def batch_process(input_file : str
                   , output_file : str
                   , prev_file : str
                   , fetch_function
                   , keys
                   , error_file : str = None
                   , merge_with_prev=True
                   , batch_size=100):

    outputs_list = []
    errors_list = []
    df = pd.read_csv(input_file)

    if prev_file:
        # See https://stackoverflow.com/questions/28901683/pandas-get-rows-which-are-not-in-other-dataframe
        pandas_merge_column = '_merge'
        prev_df = pd.read_csv(prev_file)
        prev_df = prev_df[keys]
        joint = pd.merge(df, prev_df, on=keys, how='left', indicator=True)
        df = joint[joint[pandas_merge_column] == 'left_only']
        df = df.drop(columns=[pandas_merge_column])

    print("About to process {items} items, time {time}".format(items=len(df)
                                                                , time=datetime.datetime.now()))
    item = 0;

    for _, i in df.iterrows():
        record = get_item_keys(i, keys_columns=keys)
        try:
            sample_output = fetch_function(i)
        except:
            if error_file:
                errors_list.append(record)
        record.append(sample_output)

        outputs_list.append(record)
        item += 1
        if item % batch_size == 0:
            output_df = pd.DataFrame(outputs_list)
            if len(output_df):
                output_df.columns = keys + ['output']

            output_df.to_csv(output_file, index=False)

            if error_file and len(output_df):
                errors_df = pd.DataFrame(errors_list)
                errors_df.columns = keys
                errors_df.to_csv(error_file, index=False)


            print("Processed {items} items, time {time}".format(items=item
                                                                , time=datetime.datetime.now()))

    output_df = pd.DataFrame(outputs_list)
    if len(output_df):
        output_df.columns = keys + ['output']

    if error_file and len(output_df):
        errors_df = pd.DataFrame(errors_list)
        errors_df.columns = keys
        errors_df.to_csv(error_file, index=False)

    if merge_with_prev and prev_file :
        output_df = pd.concat([prev_df, output_df])
    output_df.to_csv(output_file, index=False)

    return output_df


def get_item_keys(i, keys_columns):
    record = []
    for k in keys_columns:
        record.append(i[k])


    return record