all: build/lambda_objects_batch_post.zip build/cloudformation.yaml

build/lambda_objects_batch_post.zip: lambda_objects_batch_post.py
	@mkdir -p build
	@zip build/lambda_objects_batch_post.zip lambda_objects_batch_post.py

build/cloudformation.yaml: cloudformation.yaml
	@mkdir -p build
	cp cloudformation.yaml build/cloudformation.yaml

deploy:
	@aws cloudformation deploy --template-file ./build/cloudformation.yaml --stack-name lfs-api --capabilities CAPABILITY_IAM