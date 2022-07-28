#!/usr/bin/env sh

until [ -f ./certs/ca/ca.crt ]
do
  echo "waiting for cert..."
  sleep 0.1
done
echo "Certificate found"