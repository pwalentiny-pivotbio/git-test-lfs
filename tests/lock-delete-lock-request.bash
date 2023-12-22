TESTS_PATH=$(dirname $(realpath $0))
APIGATEWAY=$(cat $TESTS_PATH/../.apigateway-invoke-url)
curl -X POST \
    --data @$TESTS_PATH/lock-delete-lock-request.json \
    -H 'Content-Type: application/vnd.git-lfs+json' \
    -H 'Accept: application/vnd.git-lfs+json' \
    "$APIGATEWAY/pwalentiny/repo.git/info/lfs/locks/12345678/unlock"