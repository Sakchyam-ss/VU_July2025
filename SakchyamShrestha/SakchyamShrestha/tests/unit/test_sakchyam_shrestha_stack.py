import aws_cdk as core
import aws_cdk.assertions as assertions

from sakchyam_shrestha.sakchyam_shrestha_stack import SakchyamShresthaStack

# example tests. To run these tests, uncomment this file along with the example
# resource in sakchyam_shrestha/sakchyam_shrestha_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = SakchyamShresthaStack(app, "sakchyam-shrestha")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
