import pandas as pd
import datetime

def batch_process(input_file : str
                   , output_file : str
                   , prev_file : str
                   , fetch_function
                   , keys
                   , merge_with_prev=True
                   , batch_size=100):

    outputs_list = []
    df = pd.read_csv(input_file)

    if prev_file:
        # See https://stackoverflow.com/questions/28901683/pandas-get-rows-which-are-not-in-other-dataframe
        pandas_merge_column = '_merge'
        prev_df = pd.read_csv(prev_file)
        prev_df = prev_df[keys]
        joint = pd.merge(df, prev_df, on=keys, how='left', indicator=True)
        df = joint[joint[pandas_merge_column] == 'left_only']
        df = df.drop(columns=[pandas_merge_column])

    item = 0;

    for _, i in df.iterrows():
        sample_output = fetch_function(i)
        record = []
        for k in keys:
            record.append(i[k])
        record.append(sample_output)
        outputs_list.append(record)
        item += 1
        if item % batch_size == 0:
            output_df = pd.DataFrame(outputs_list)
            if len(output_df):
                output_df.columns = keys + ['output']

            output_df.to_csv(output_file, index=False)
            print("Processed {items} items, time {time}".format(items=item
                                                                , time=datetime.datetime.now()))

    output_df = pd.DataFrame(outputs_list)
    if len(output_df):
        output_df.columns = keys + ['output']

    if merge_with_prev and prev_file :
        output_df = pd.concat([prev_df, output_df])
    output_df.to_csv(output_file, index=False)

    return output_df
