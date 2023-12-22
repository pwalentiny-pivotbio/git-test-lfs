APIGATEWAY=$(cat .apigateway-invoke-url)
curl -X POST \
    --data @batch-download-request.json \
    -H 'Content-Type: application/vnd.git-lfs+json' \
    -H 'Accept: application/vnd.git-lfs+json' \
    "$APIGATEWAY/pwalentiny/repo.git/info/lfs/objects/batch"