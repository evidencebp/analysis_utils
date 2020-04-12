import os
import pandas as pd
from typing import Dict

def analyze_twins_file(twins_file
                               , match_column
                               , mismatch_column
                               , time_column='year'
                               , minimal_time=-1):
    df = pd.read_csv(twins_file)
    df = df[df[time_column]> minimal_time]
    df['pairs'] = df[match_column] + df[mismatch_column]
    df['match_ratio'] = df[match_column] / df.cap_pairs

    print(df)

    return df

def generate_twins_sql(source_data_set
                       , twin_column
                       , env_column
                       , metrics_dict
                       , prefix
                       , output_file
                       , time_column='year'
                       ):
    f = open(output_file, "w")
    f.write(generate_env_porfile_sql(source_data_set
                   , env_column
                   , metrics_dict
                   , prefix
                   , time_column))
    f.write("\n")
    f.write(generate_twin_in_env_porfile_sql(source_data_set
                       , twin_column
                       , env_column
                       , metrics_dict
                       , prefix
                       , time_column))
    f.write("\n")

    for metric in metrics_dict:
        f.write(generate_twins_match_stats_sql(twin_column
                       , env_column
                       , metric
                       , prefix))
    f.close()


def generate_twin_porfile_sql(source_data_set : str
                       , twin_column : str
                       , metrics_dict : Dict
                       , prefix : str
                       , time_column : str ='year'
                       ) -> str:

    table_name = prefix + 'twin_porfile'

    drop_sql = 'drop table if exists {};'.format(table_name)

    create_sql = """
    create table {}
    parition by fake_date
    cluster by {}
    as
    select
    {}
    , {}
    , {}
    , max(DATE('1980-01-01')) as  fake_date
    from
    {}
    group by
    {}
    , {}
    ;    
    """.format(table_name
               , twin_column
               , twin_column
               , time_column
               , generate_metrics_clause(metrics_dict)
               , source_data_set
               , twin_column
               , time_column
               )

    generation_sql = drop_sql + " " + create_sql

    return generation_sql

def generate_metrics_clause(metrics_dict : Dict) -> str:

    clauses = []
    for i in sorted(metrics_dict.keys()):
        clauses.append(" {} as {}".format(metrics_dict[i]
                                         , i))
    return ",".join(clauses)


def generate_env_porfile_sql(source_data_set
                   , env_column
                   , metrics_dict
                   , prefix
                   , time_column : str ='year'):
    table_name = prefix + 'env_porfile'

    drop_sql = 'drop table if exists {};'.format(table_name)

    create_sql = """
    create table {}
    parition by fake_date
    cluster by {}
    as
    select
    {}
    , {}
    , {}
    , max(DATE('1980-01-01')) as  fake_date
    from
    {}
    group by
    {}
    , {}
    ;    
    """.format(table_name
               , env_column
               , env_column
               , time_column
               , generate_metrics_clause(metrics_dict)
               , source_data_set
               , env_column
               , time_column
               )

    generation_sql = drop_sql + " " + create_sql

    return generation_sql

def generate_twin_in_env_porfile_sql(source_data_set
                       , twin_column
                       , env_column
                       , metrics_dict
                       , prefix
                       , time_column='year'):
    table_name = prefix + 'twin_in_env_porfile'

    drop_sql = 'drop table if exists {};'.format(table_name)

    create_sql = """
    create table {}
    parition by fake_date
    cluster by {}, {}
    as
    select
    {}
    , {}
    , {}
    , {}
    , max(DATE('1980-01-01')) as  fake_date
    from
    {}
    group by
    {}
    , {}
    , {}
    ;    
    """.format(table_name
               , twin_column
               , env_column
               , env_column
               , twin_column
               , time_column
               , generate_metrics_clause(metrics_dict)
               , source_data_set
               , env_column
               , twin_column
               , time_column
               )

    generation_sql = drop_sql + " " + create_sql

    return generation_sql


def generate_twins_match_stats_sql(twin_column
                       , env_column
                       , metric
                       , prefix):
    sql = """
    Select 
        env1.{metric} > env2.{metric} as env_higher
        , twin1.{metric} > twin2.{metric} as twin_higher
        , count(*) as cnt
    from
        {twin_in_env} as twin_in_env1
        join
        {twin_in_env} as twin_in_env2
        on
        twin_in_env1.{twin_column} = twin_in_env2.{twin_column}
        and
        twin_in_env1.{env_column} <> twin_in_env2.{env_column}
        join
        {env} as env1
        on
        twin_in_env1.{env_column} = env1.{env_column}
        join
        {env} as env2
        on
        twin_in_env2.{env_column} = env2.{env_column}
        group by
        env_higher, twin_higher
        order by 
        env_higher, twin_higher
    """.format(metric=metric
               , twin_in_env=prefix + 'twin_in_env_porfile'
               , twin_column=twin_column
               , env_column=env_column
               , env=prefix + 'env_porfile'
               )

    return sql

