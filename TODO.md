* ~~Re-write into cloudformation for easy deployment~~
* Create test requests for each endpoint
* Test each endpoint with the test request just to see that we are reaching the lambda backend
* Find or write a schema for APIMethodProjectRepoInfoLfsLocksVerifyPost's request model.
* Consider separating out APILambdaIAMRole into separate roles for each lambda and/or get more specific with the log groups they can write to.
* Transform the batch api request into parameters for the lambda using a mapping template
* Investigate if we can use presigned urls for putting files directly... or
* Use transforms to create an S3 integration for uploading and downloading files

