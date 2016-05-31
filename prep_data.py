from __future__ import print_function

from sqlalchemy import create_engine
from cubes.tutorial.sql import create_table_from_csv
import time

s_time = time.time()

FACT_TABLE = "FB_POSTS_DATA"
FACT_TABLE2 = "KEYWORDS_DATA"

print("preparing data...\n")

engine = create_engine('sqlite:///myData.sqlite')

create_table_from_csv(engine,
                      "fb_posts_data.csv",
                      table_name=FACT_TABLE,
                      fields=[
			    ("id", "string"),
                            ("name", "string"),
                            ("description", "string"),
                            ("message", "string"),
                            ("category", "string"),
			    ("like", "integer"),
                            ("share", "integer"),
                            ("comment", "integer"),
                            ("ctr", "float")
			])

create_table_from_csv(engine,
                      "keywords_data.csv",
                      table_name=FACT_TABLE2,
                      fields=[
			    ("id", "string"),
                            ("keywords", "string"),
			    ("like", "integer"),
                            ("share", "integer"),
                            ("comment", "integer"),
                            ("ctr", "float")
                        ]
                  )

print("done.\nfile myData.sqlite created\n")

t_time = time.time() - s_time

print('Time taken: %0.2f seconds\n' % t_time)

