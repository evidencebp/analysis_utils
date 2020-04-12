import sys
CODE_PATH = "C:/Idan/GitHub/analysis_utils/"
sys.path.append(CODE_PATH)

import pytest
from twins_analysis import generate_twin_porfile_sql, generate_metrics_clause\
    , generate_twin_in_env_porfile_sql, generate_env_porfile_sql, generate_twins_match_stats_sql



def test_generate_twin_porfile_sql():

    actual = generate_twin_porfile_sql(source_data_set='ccp.classified_commits'
                       , twin_column='Author_email'
                       , metrics_dict= {'cnt' : 'count(*)'
                                , 'avg_ccp' : 'avg(ccp)'}
                       , prefix='churn_'
                       , time_column='year'
                       ).replace("'", "").replace("\n", "").replace(" ", "")

    expected = "drop table if exists churn_twin_porfile; \n\n     " \
               "create table churn_twin_porfile\n\n     parition by fake_date\n'\n '    " \
               "cluster by Author_email\n\n     as\n\n     " \
               "select\n\n     Author_email\n\n     , year\n\n     " \
               ",  avg(ccp) as avg_ccp, count(*) as cnt\n\n     , max(DATE('1980-01-01')) as  fake_date" \
               "\n\n     from\n\n     ccp.classified_commits\n\n     " \
               "group by\n\n     Author_email\n\n     , year\n\n     ;    \n\n     "
    expected = expected.replace("'", "").replace("\n", "").replace(" ", "")

    assert actual == expected

def test_generate_metrics_clause():
    metrics_dict = {'cnt' : 'count(*)'
                    , 'avg_ccp' : 'avg(ccp)'}

    actual = generate_metrics_clause(metrics_dict)
    expected = ' avg(ccp) as avg_ccp, count(*) as cnt'

    assert actual.replace("'", "").replace("\n", "") == expected.replace("'", "").replace("\n", "")


def test_generate_twin_in_env_porfile_sql():

    actual = generate_twin_in_env_porfile_sql(source_data_set='ccp.classified_commits'
                       , twin_column='Author_email'
                       , env_column='repo_name'
                       , metrics_dict= {'cnt' : 'count(*)'
                                , 'avg_ccp' : 'avg(ccp)'}
                       , prefix='churn_'
                       , time_column='year'
                       ).replace("'", "").replace("\n", "").replace(" ", "")

    expected = "drop table if exists churn_twin_in_env_porfile;     create table \n churn_twin_in_env_porfile" \
               "    parition by fake_date    cluster by Author_email, \n repo_name    as   " \
               "select    repo_name    , Author_email    , year    " \
               ",  \n avg(ccp) as avg_ccp, count(*) as cnt    , max(DATE(1980-01-01)) as  \n fake_date" \
               "    from    ccp.classified_commits    " \
               "group by    repo_name    , \n Author_email    , year    ;        "
    expected = expected.replace("'", "").replace("\n", "").replace(" ", "")

    assert actual == expected

def test_generate_env_porfile_sql():

    actual = generate_env_porfile_sql(source_data_set='ccp.classified_commits'
                       , env_column='repo_name'
                       , metrics_dict= {'cnt' : 'count(*)'
                                , 'avg_ccp' : 'avg(ccp)'}
                       , prefix='churn_'
                       , time_column='year'
                       ).replace("'", "").replace("\n", "").replace(" ", "")

    expected = "drop table if exists churn_env_porfile; \n\n     " \
               "create table churn_env_porfile\n\n     parition by fake_date\n'\n '    " \
               "cluster by repo_name\n\n     as\n\n     " \
               "select\n\n     repo_name\n\n     , year\n\n     " \
               ",  avg(ccp) as avg_ccp, count(*) as cnt\n\n     , max(DATE('1980-01-01')) as  fake_date" \
               "\n\n     from\n\n     ccp.classified_commits\n\n     " \
               "group by\n\n     repo_name\n\n     , year\n\n     ;    \n\n     "
    expected = expected.replace("'", "").replace("\n", "").replace(" ", "")

    assert actual == expected

def test_generate_twins_match_stats_sql():

    actual = generate_twins_match_stats_sql(source_data_set='ccp.classified_commits'
                       , env_column='repo_name'
                       , twin_column='Author_email'
                       , metric='avg_ccp'
                       , prefix='churn_'
                       ).replace("'", "").replace("\n", "").replace(" ", "")

    expected = "'\n'\n '    Select \n'\n '        env1.avg_ccp > env2.avg_ccp as env_higher\n'\n '" \
               "        , twin1.avg_ccp > twin2.avg_ccp as twin_higher\n'\n '" \
               "        , count(*) as cnt\n'\n '    " \
               "from\n'\n '        churn_twin_in_env_porfile as twin_in_env1\n'\n '" \
               "        join\n'\n '        churn_twin_in_env_porfile as twin_in_env2\n'\n '" \
               "        on\n'\n '        twin_in_env1.Author_email = twin_in_env2.Author_email\n'\n '" \
               "        and\n'\n '        twin_in_env1.repo_name <> twin_in_env2.repo_name\n'\n '" \
               "        join\n'\n '        churn_env_porfile as env1\n'\n '        on\n'\n '" \
               "        twin_in_env1.repo_name = env1.repo_name\n'\n '        join\n'\n '" \
               "        churn_env_porfile as env2\n'\n '        on\n'\n '        " \
               "twin_in_env2.repo_name = env2.repo_name\n'\n '        " \
               "group by\n'\n '        env_higher, twin_higher\n'\n '        " \
               "order by \n'\n '        env_higher, twin_higher\n'\n '    '"
    expected = expected.replace("'", "").replace("\n", "").replace(" ", "")

    assert actual == expected
