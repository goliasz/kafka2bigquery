# kafka2bigquery

## Test
```
$ nohup python src/main/python/dump_topic.py > test.lo 2>&1 & 
```

## BQ Location
```
/home/ubuntu/google-cloud-sdk/bin/bq
```

## Installl BQ
```
# Big Query
$ wget https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-169.0.0-linux-x86_64.tar.gz && \
  tar -xvzf google-cloud-sdk-169.0.0-linux-x86_64.tar.gz
$ cd google-cloud-sdk && ./install.sh -q
```

