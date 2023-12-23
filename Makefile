# .PHONY: all
# all: build/lambda_objects_batch_post.zip build/cloudformation.yaml

# build/lambda_objects_batch_post.zip: lambda_objects_batch_post.py
# 	@mkdir -p build
# 	@zip build/lambda_objects_batch_post.zip lambda_objects_batch_post.py

# build/cloudformation.yaml: cloudformation.yaml
# 	@mkdir -p build
# 	cp cloudformation.yaml build/cloudformation.yaml


# GET_CLOUDFORMATION_EVAL = $(eval SHA = $(shell shasum -a 256 build/cloudformation.yaml | cut -f 1 -d ' '))
# .PHONY: deploy
# deploy: 
# 	$(eval cloudformation_SHA256 = $(shell shasum -a 256 build/cloudformation.yaml | cut -f 1 -d ' '))
# 	$(eval lambda_objects_batch_post_SHA256 = $(shell shasum -a 256 build/lambda_objects_batch_post.zip | cut -f 1 -d ' '))
# 	@echo $(cloudformation_SHA256)
# 	@echo $(lambda_objects_batch_post_SHA256)
# 	@aws s3 cp build/cloudformation.yaml s3://$(BUCKET)/$(cloudformation_SHA256).yaml
# 	@aws s3 cp build/cloudformation.yaml s3://$(BUCKET)/$(lambda_objects_batch_post_SHA256).yaml
# 	@aws cloudformation deploy --template-file ./build/cloudformation.yaml --stack-name lfs-api --capabilities CAPABILITY_IAM

ARTIFACT_BUCKET := git-lfs-artifacts-3ja5fr4
CF_TEMPLATE := cloudformation.yaml
CF_TEMPLATE_PACKAGED := cloudformation-packaged.yaml
LAMBDA_FUNCTIONS := $(wildcard lambda_*.py)

.PHONY: all
all: $(CF_TEMPLATE_PACKAGED)

$(CF_TEMPLATE_PACKAGED): $(CF_TEMPLATE) $(LAMBDA_FUNCTIONS)
	@aws cloudformation package --template-file ./$(CF_TEMPLATE) --s3-bucket $(ARTIFACT_BUCKET) --output-template-file $(CF_TEMPLATE_PACKAGED)

.PHONY: deploy
deploy: $(CF_TEMPLATE_PACKAGED)
	@aws cloudformation deploy --template-file ./$(CF_TEMPLATE_PACKAGED) --stack-name lfs-api --capabilities CAPABILITY_IAM