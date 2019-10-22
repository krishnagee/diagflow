# cloudinfrastructure automation
Public cloud infrastructure automation is enabled using pulumi , ansible or terraform. To take the automation to next level,we use 
CNN/RNN/Attention network to automate the recognition of resources and generate relevant scripts for the same. The project is inspired by the work Show, Attend and Tell paper (https://arxiv.org/abs/1502.03044)

The workflow designed for PoC comprises below stages

# Input : Architecture diagram in jpg/png image format (with required pixel resolution)

# stage 0  : Feature recognition (realized by CNN)
# stage 1  : Caption generation (realized by RNN/Embeddings)
# stage 1.5: Manual caption and resource verification/correction.
# stage 2  : Infrastructure scripts synthesis (here we use terraform/HCL as infrastructure script).
# stage 2.5: Manual sccript verification/amendment.
# stage 3  : Execution of infrastructure script (plan and execute)
# stage 4  : Generation of terraform graph (with resource dependency)

# Output : Generated terraform script, resource graph, image caption

# Toolsets requirements:
# Tensorflow 2.0
# python > 3.6
# React UI (if possible) available as container image.
# Flask python server(model serving) available as container image.
# Terraform > 0.12
# Airflow for training tf model pipeline
# Cloud storage for storing testing/training datesets, model protobuffer format.
# Kubernetes > v1.15
# Docker repository mounted over kubernetes.
# Any public cloud account details (to start with we use google cloud as example)


# Future plan: Integrate the infrastructure script output into the input architecture diagram, resulting in revised architecture diagram with specific details.


