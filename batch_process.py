import pandas as pd
import datetime

class BatchProcessor:
    def __init__(self
                   , input_file: str
                   , output_file: str
                   , prev_file: str
                   , fetch_function
                   , keys
                   , error_file : str = None
                   , merge_with_prev=True
                   , batch_size=100
                   , output_column='output'
                   , pause_function=None):

        self.input_file = input_file
        self.output_file = output_file
        self.prev_file = prev_file
        self.fetch_function = fetch_function
        self.keys = keys
        self.error_file = error_file
        self.merge_with_prev = merge_with_prev
        self.batch_size = batch_size
        self.output_column = output_column
        self.pause_function = pause_function


    def process(self):

        outputs_list = []
        errors_list = []
        df = pd.read_csv(self.input_file)

        if self.prev_file:
            # See https://stackoverflow.com/questions/28901683/pandas-get-rows-which-are-not-in-other-dataframe
            pandas_merge_column = '_merge'
            prev_df = pd.read_csv(self.prev_file)
            prev_df = prev_df[self.keys]
            joint = pd.merge(df
                             , prev_df
                             , on=self.keys
                             , how='left'
                             , indicator=True)
            df = joint[joint[pandas_merge_column] == 'left_only']
            df = df.drop(columns=[pandas_merge_column])

        print("About to process {items} items, time {time}".format(items=len(df)
                                                                    , time=datetime.datetime.now()))
        item = 0;

        for _, i in df.iterrows():
            record = BatchProcessor.get_item_keys(i
                                                  , keys_columns=self.keys)
            try:
                sample_output = self.fetch_function(i)
                record.append(sample_output)
                outputs_list.append(record)
            except:
                if self.error_file:
                    errors_list.append(BatchProcessor.get_item_keys(i
                                                  , keys_columns=self.keys))

            item += 1
            if item % self.batch_size == 0:
                self.write_results(errors_list
                                   , outputs_list)

                print("Processed {items} items, time {time}".format(items=item
                                                                    , time=datetime.datetime.now()))
                if self.pause_function:
                    self.pause_function()

        output_df = pd.DataFrame(outputs_list)
        if len(output_df):
            output_df.columns = self.keys + [self.output_column]

        self.write_results(errors_list
                           , outputs_list)

        if self.merge_with_prev and self.prev_file :
            output_df = pd.concat([prev_df
                                      , output_df])
        output_df.to_csv(self.output_file
                         , index=False)

        return output_df

    def write_results(self
                      , errors_list
                      , outputs_list):
        self.list_to_file(outputs_list
                          , columns=self.keys + [self.output_column]
                          , output_file=self.output_file)
        if self.error_file and len(errors_list):
            self.list_to_file(errors_list
                              , columns=self.keys
                              , output_file=self.error_file)

    def list_to_file(self
                     , outputs_list
                     , columns
                     , output_file):
        output_df = pd.DataFrame(outputs_list)
        if len(output_df):
            output_df.columns = columns
        output_df.to_csv(output_file
                         , index=False)
        return output_df

    @staticmethod
    def get_item_keys(i, keys_columns):
        record = []
        for k in keys_columns:
            record.append(i[k])

        return record