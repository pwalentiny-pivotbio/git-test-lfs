* In Batch API
    * Return object error 410 is S3 returns a delete marker when downloading
    * Return HTTP error 401 for missing credentials - technically this is the authentication TODO
    * Return HTTP error 403 for read-only on upload - probably won't  use this for a while
    * Return HTTP error 422 for one or more of the objects in the request. This means that none of the requested objects to upload are valid.
    * Read through optional codes
    * ~~Return object error 409 if hash algo is anything other than sha256~~
    * ~~Return object error 404 for missing objects~~
* Implement lock API
* Find or write a schema for APIMethodProjectRepoInfoLfsLocksVerifyPost's request model.
* Consider separating out APILambdaIAMRole into separate roles for each lambda and/or get more specific with the log groups they can write to.
* Make use of ${AWS::StackName} so more than one environment can be deployed per account
* Fix tests so we can run it from any directory (or from vscode)
* See if we need to sanitize inputs for APIMethodProjectRepoInfoLfsObjectsBatchPost's RequestTemplates
* In lambda_objects_batch_post._object_exists, handle the missing bucket exception sanely
* Figure out authentication for the API
    * Can we use cognito (maybe connected to GitHub oauth like circleci)?
    * Maybe we just start with apikeys in the basic auth header via RequestTemplates or something.
    * Figure out how to use credentials manager for our LFS config
* Look into automating documentation
    * Sphinx?
* Web UI
    * Object import/export from external LFS
    * User management
    * Object management (CRUD)
* Create a project website
    * Publish new versions
    * Quickstart guide
    * Deployment video
    * Documentation
* ~~Implement verify callback~~ - I don't think we need this after adding the sha256 hash check to S3
* ~~Validate the hash of newly created objects~~
* ~~Fix S3 object store bucket logging~~
* ~~Re-write into cloudformation for easy deployment~~
* ~~Create test requests for each endpoint~~
* ~~Test each endpoint with the test request just to see that we are reaching the lambda backend~~
    * ~~Fix errors when making requests to POST /{project}/{repo}/info/lfs/locks/{id}/unlock~~
    * ~~Fix errors when making requests to GET /{project}/{repo}/info/lfs/locks~~
* ~~Test the git CLI against the API for pushing objects, to see what breaks~~
    * ~~Solve the missing authentication token problem~~
    * ~~No errors, but no files were uploaded either.  Return a valid response to get an actual upload.~~
* ~~Flush out the build and deploy scripts so I can separate out python scripts from cloudformation.~~
* ~~Create an S3 bucket to store objects~~
* ~~Test the git CLI against the API for pulling objects, to see what breaks~~
* ~~Transform the batch api request into parameters for the lambda using a mapping template~~
* ~~Investigate if we can use presigned urls for putting files directly... or~~
* ~~Use transforms to create an S3 integration for uploading and downloading files~~
