import sys
CODE_PATH = "C:/Idan/GitHub/analysis_utils/"
sys.path.append(CODE_PATH)

import pytest
from twins_analysis import generate_twin_porfile_sql, generate_metrics_clause\
    , generate_twin_in_env_porfile_sql, generate_env_porfile_sql, generate_twins_match_stats_sql



def test_generate_twin_porfile_sql():

    metrics_dict = {'cnt': {'code':'count(*)', 'the_higher_the_better': True}
        , 'avg_ccp': {'code':'avg(ccp)', 'the_higher_the_better': True}}

    actual = generate_twin_porfile_sql(source_data_set='ccp.classified_commits'
                       , twin_column='Author_email'
                       , metrics_dict=metrics_dict
                       , prefix='churn_'
                       ).replace("'", "").replace("\n", "").replace(" ", "")

    expected = "'drop table if exists ccp.churn_twin_porfile; \n'\n '    create table ccp.churn_twin_porfile\n'\n '" \
               "    partition by fake_date\n'\n '    cluster by Author_email\n'\n '    as\n'\n '    " \
               "select\n'\n '    Author_email\n'\n '    \n'\n '    ,  avg(ccp) as avg_ccp, count(*) as cnt" \
               "\n'\n     , max(DATE('1980-01-01')) as  fake_date\n\n '    " \
               "from\n'\n '    ccp.classified_commits\n'\n '    " \
               "group by\n'\n '    Author_email\n'\n '    \n'\n '    \n'\n '    ;    \n'\n '    "
    expected = expected.replace("'", "").replace("\n", "").replace(" ", "")

    assert actual == expected

def test_generate_metrics_clause():
    metrics_dict = {'cnt': {'code':'count(*)', 'the_higher_the_better': True}
        , 'avg_ccp': {'code':'avg(ccp)', 'the_higher_the_better': True}}

    actual = generate_metrics_clause(metrics_dict)
    expected = ' avg(ccp) as avg_ccp, count(*) as cnt'

    assert actual.replace("'", "").replace("\n", "") == expected.replace("'", "").replace("\n", "")


def test_generate_twin_in_env_porfile_sql():

    metrics_dict = {'cnt': {'code':'count(*)', 'the_higher_the_better': True}
        , 'avg_ccp': {'code':'avg(ccp)', 'the_higher_the_better': True}}

    actual = generate_twin_in_env_porfile_sql(source_data_set='ccp.classified_commits'
                       , twin_column='Author_email'
                       , env_column='repo_name'
                       , metrics_dict=metrics_dict
                       , prefix='churn_'
                       ).replace("'", "").replace("\n", "").replace(" ", "")

    expected = "drop table if exists ccp.churn_twin_in_env_porfile; \n'\n '    " \
               "create table ccp.churn_twin_in_env_porfile\n'\n '    partition by fake_date\n'\n '    " \
               "cluster by repo_name, Author_email\n'\n '    as\n'\n '    " \
               "select\n'\n '    repo_name\n'\n '    , Author_email\n'\n '    \n'\n '    " \
               ",  avg(ccp) as avg_ccp, count(*) as cnt\n'\n     , max(DATE('1980-01-01')) as  fake_date\n\n '    " \
               "from\n'\n '    ccp.classified_commits\n'\n '    " \
               "group by\n'\n '    repo_name\n'\n '    , Author_email\n'\n '    \n'\n '    \n'\n '    ;    \n'\n '    "
    expected = expected.replace("'", "").replace("\n", "").replace(" ", "")

    assert actual == expected

def test_generate_env_porfile_sql():

    metrics_dict = {'cnt': {'code':'count(*)', 'the_higher_the_better': True}
        , 'avg_ccp': {'code':'avg(ccp)', 'the_higher_the_better': True}}

    actual = generate_env_porfile_sql(source_data_set='ccp.classified_commits'
                       , env_column='repo_name'
                       , metrics_dict=metrics_dict
                       , prefix='churn_'
                       ).replace("'", "").replace("\n", "").replace(" ", "")

    expected = "drop table if exists ccp.churn_env_porfile; \n'\n '    " \
               "create table  ccp.churn_env_porfile\n'\n '    partition by fake_date\n'\n '    " \
               "cluster by repo_name\n'\n '    as\n'\n '    " \
               "select\n'\n '    repo_name\n'\n '    \n'\n '    ,  avg(ccp) as avg_ccp, count(*) as cnt\n'\n " \
               "    , max(DATE('1980-01-01')) as  fake_date\n\n '    " \
               "from\n'\n '    ccp.classified_commits\n'\n '    " \
               "group by\n'\n '    repo_name\n'\n '    \n'\n '    \n'\n '    ;    \n'\n '    "
    expected = expected.replace("'", "").replace("\n", "").replace(" ", "")

    assert actual == expected

def test_generate_twins_match_stats_sql():

    actual = generate_twins_match_stats_sql(env_column='repo_name'
                       , twin_column='Author_email'
                       , metric='avg_ccp'
                       , prefix='churn_'
                       , schema='ccp'
                       ).replace("'", "").replace("\n", "").replace(" ", "")

    expected = "\n'\n '    Select \n'\n '        \n'\n '        env1.avg_ccp > env2.avg_ccp  as env_improved\n'\n '" \
               "        , twin_in_env1.avg_ccp > twin_in_env2.avg_ccp  as twin_improved\n'\n '        " \
               ", count(*) as cnt\n'\n '        " \
               ", count(distinct twin_in_env1.Author_email) as twins_cnt\n'\n '        " \
               ", count(distinct twin_in_env1.repo_name) as envs_cnt\n'\n '    " \
               "from\n'\n '        ccp.churn_twin_in_env_porfile as twin_in_env1\n'\n '        " \
               "join\n'\n '        ccp.churn_twin_in_env_porfile as twin_in_env2\n'\n '        " \
               "on\n'\n '        twin_in_env1.Author_email = twin_in_env2.Author_email\n'\n '        " \
               "and\n'\n '        twin_in_env1.repo_name <> twin_in_env2.repo_name\n'\n '        " \
               "join\n'\n '        ccp.churn_env_porfile as env1\n'\n '        on\n'\n '        " \
               "twin_in_env1.repo_name = env1.repo_name\n'\n '        join\n'\n '        " \
               "ccp.churn_env_porfile as env2\n'\n '        on\n'\n '        " \
               "twin_in_env2.repo_name = env2.repo_name\n'\n '        " \
               "group by\n'\n '                \n'\n '        env_improved, twin_improved\n'\n '        " \
               "order by\n'\n '         \n'\n '        env_improved, twin_improved\n'\n '        ;\n'\n '    "
    expected = expected.replace("'", "").replace("\n", "").replace(" ", "")

    assert actual == expected
