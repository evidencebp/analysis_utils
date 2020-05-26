import pandas as pd
import time

def batch_process(input_file : str
                   , output_file : str
                   , prev_file : str
                   , fetch_function
                   , key_function):

    outputs_list = []
    df = pd.read_csv(input_file)

    if prev_file:
        output_df = pd.read_csv(prev_file)
        extracted_emails = output_df.hashed_email.tolist()
        df = df[~df.author_email.isin(extracted_emails)]

    item = 0;

    for _, i in df.iterrows():
        sample_output = fetch_function()
        outputs_list.append((key_function(i)
                       , sample_output))
        item += 1
        if item % 100 == 0:
            output_df = pd.DataFrame(outputs_list)
            output_df.columns = ['key', 'output']

            output_df.to_csv(output_file, index=False)
            print("Processed {items} items, time {time}".format(items=item
                                                                , time=time.datetime.now().strftime("%H:%M:%S")))

    output_df = pd.DataFrame(outputs_list)
    output_df.columns = ['key', 'output']

    output_df.to_csv(output_file, index=False)

