#!/bin/bash

cd resources

zip -r code.zip .

cd ..

cdk deploy --require-approval never
