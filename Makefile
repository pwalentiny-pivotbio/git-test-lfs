ARTIFACT_BUCKET := git-lfs-artifacts-3ja5fr4
CF_TEMPLATE := cloudformation.yaml
CF_TEMPLATE_PACKAGED := cloudformation-packaged.yaml
LAMBDA_FUNCTIONS := $(wildcard lambda_*.py)
STACK_NAME := git-lfs-api

.PHONY: all
all: $(CF_TEMPLATE_PACKAGED)

.PHONY: deploy
deploy: $(CF_TEMPLATE_PACKAGED)
	@aws cloudformation deploy --template-file ./$(CF_TEMPLATE_PACKAGED) --stack-name $(STACK_NAME) --capabilities CAPABILITY_IAM

.PHONY: events
events:
	@aws cloudformation describe-stack-events --stack-name $(STACK_NAME)

$(CF_TEMPLATE_PACKAGED): $(CF_TEMPLATE) $(LAMBDA_FUNCTIONS)
	@aws cloudformation package --template-file ./$(CF_TEMPLATE) --s3-bucket $(ARTIFACT_BUCKET) --output-template-file $(CF_TEMPLATE_PACKAGED)