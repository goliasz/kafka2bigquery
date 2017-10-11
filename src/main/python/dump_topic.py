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
from kafka import KafkaConsumer, SimpleConsumer
import os.path
import subprocess

def gzip_yesterday(yesterday):
  #print "gzip_yesterday"
  out = None
  fname = args.target_folder+"/"+args.target_file+"_"+yesterday+".json"  
  if os.path.isfile(fname):
    #check_call('gzip '+fname)
    cmd = ("gzip__"+fname).split("__")
    out = subprocess.check_output(cmd)    
  return out

def save():
  #print "save"

  # Kafka
  consumer = KafkaConsumer(bootstrap_servers=args.kafka_bootstrap_srvs, group_id=args.kafka_group_id)
  consumer.subscribe([args.kafka_source_topic])

  for msg in consumer:
    #
    indata = json.loads(msg.value)
    #print indata
    #
    today = str(datetime.today())[0:10]
    yesterday = datetime.strftime(datetime.now() - timedelta(1), '%Y%m%d')
    #
    #print today
    #
    file_name = args.target_folder+"/"+args.target_file+"_"+today.replace("-","")+".json"
    with open(file_name, 'a') as the_file:
      the_file.write(json.dumps(indata)+'\n')
    #
    if args.gzip_yesterday == "yes":
      gzip_yesterday(yesterday)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description="Dump topic")
  parser.add_argument('--kafka_bootstrap_srvs', default="localhost:9092")
  parser.add_argument('--kafka_group_id', default="backup_topic")
  parser.add_argument('--kafka_source_topic', default="good")
  parser.add_argument('--target_folder', default="data")
  parser.add_argument('--target_file', default="good")
  parser.add_argument('--gzip_yesterday', default="yes")
  #
  args = parser.parse_args()
  #
  save()
