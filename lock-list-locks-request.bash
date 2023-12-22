APIGATEWAY=$(cat .apigateway-invoke-url)
curl -X GET \
    -H 'Accept: application/vnd.git-lfs+json' \
    "$APIGATEWAY/pwalentiny/repo.git/info/lfs/locks?path=&id=&cursor=&limit=&refspec="