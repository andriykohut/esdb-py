import os
import sys

# this is because grpc_tools.protoc doesn't know how to put generated code into packages
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
