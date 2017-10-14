#!/usr/bin/python

# Copyright KOLIBERO under one or more contributor license agreements.  
# KOLIBERO licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import time
import os
import uuid
import argparse
from datetime import datetime, timedelta
import os.path
import subprocess

def push_day(day):
  # We are appending day since we are assuming the table is partitioned
  table = args.bq_tab+day
  # If new table specified then we are skipping schema enforcement
  if args.new_bq_tab == "":
    print "table",table
    fname = args.data_folder+"/"+args.file_prefix+day+args.file_suffix 
    print "fname",fname
    cmd = (args.bq_location+'__--nouse_gce_service_account__--application_default_credential_file='+args.key_location+'__load__--noautodetect__--replace__--source_format=NEWLINE_DELIMITED_JSON__'+table+'__'+fname+'__'+args.bq_tab_schema).split("__")
    print "cmd:",cmd
    subprocess.check_call(cmd)
  else:
    table = args.new_bq_tab
    print "table",table
    fname = args.data_folder+"/"+args.file_prefix+day+args.file_suffix 
    print "fname",fname
    cmd = (args.bq_location+'__--nouse_gce_service_account__--application_default_credential_file='+args.key_location+'__load__--autodetect__--noreplace__--schema_update_option=ALLOW_FIELD_ADDITION__--schema_update_option=ALLOW_FIELD_RELAXATION__--source_format=NEWLINE_DELIMITED_JSON__'+table+'__'+fname).split("__")
    print "cmd:",cmd
    subprocess.check_call(cmd)


#
if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="Push day to BQ")
  parser.add_argument('--bq_location', default="/home/ubuntu/google-cloud-sdk/bin/bq")
  parser.add_argument('--key_location', default="/home/ubuntu/google/key.json")
  parser.add_argument('--file_prefix', default="good_")
  parser.add_argument('--file_suffix', default=".json.gz")
  parser.add_argument('--data_folder', default="data")
  parser.add_argument('--bq_tab_schema', default="src/main/json/table_schema.json")
  parser.add_argument('--bq_tab', default="project:dataset.table$")
  parser.add_argument('--rm_after_upload', default="no")
  parser.add_argument('--day', default="")
  parser.add_argument('--new_bq_tab', default="")
  #
  args = parser.parse_args()

  yesterday = datetime.strftime(datetime.now() - timedelta(1), '%Y%m%d')
  if args.day:
    push_day(args.day)
  else:
    push_day(yesterday)
