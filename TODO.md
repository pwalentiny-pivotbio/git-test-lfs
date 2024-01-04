* Implement verify callback
* Validate the hash of newly created objects
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
