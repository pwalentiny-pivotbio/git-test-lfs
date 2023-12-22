* ~~Re-write into cloudformation for easy deployment~~
* ~~Create test requests for each endpoint~~
* ~~Test each endpoint with the test request just to see that we are reaching the lambda backend~~
    * ~~Fix errors when making requests to POST /{project}/{repo}/info/lfs/locks/{id}/unlock~~
    * Fix errors when making requests to GET /{project}/{repo}/info/lfs/locks
* Test the git CLI against the API for pushing objects, to see what breaks
* Test the git CLI against the API for pulling objects, to see what breaks
* Find or write a schema for APIMethodProjectRepoInfoLfsLocksVerifyPost's request model.
* Consider separating out APILambdaIAMRole into separate roles for each lambda and/or get more specific with the log groups they can write to.
* Transform the batch api request into parameters for the lambda using a mapping template
* Investigate if we can use presigned urls for putting files directly... or
* Use transforms to create an S3 integration for uploading and downloading files

