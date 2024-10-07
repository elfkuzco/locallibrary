# pyright: strict, reportMissingTypeStubs=false,reportUnknownMemberType=false
from concurrent import futures

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from locallibrary_frontend_grpc import frontend_pb2_grpc

from locallibrary_frontend.db import upgrade_db_schema
from locallibrary_frontend.grpc.server import FrontendServicer
from locallibrary_frontend.settings import Settings


def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    frontend_pb2_grpc.add_LocalLibraryFrontendServicer_to_server(
        FrontendServicer(), server
    )
    server.add_insecure_port(f"[::]:{Settings.GRPC_SERVER_PORT}")
    upgrade_db_schema()
    server.start()
    server.wait_for_termination()
