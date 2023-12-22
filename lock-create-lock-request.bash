APIGATEWAY=$(cat .apigateway-invoke-url)
curl -X POST \
    --data @lock-create-lock-request.json \
    -H 'Content-Type: application/vnd.git-lfs+json' \
    -H 'Accept: application/vnd.git-lfs+json' \
    "$APIGATEWAY/pwalentiny/repo.git/info/lfs/locks"