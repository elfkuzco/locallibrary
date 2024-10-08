package frontend

import (
	"github.com/elfkuzco/locallibrary/grpc/golang/frontend"
	"google.golang.org/grpc"
)

type LocalLibraryFrontendClient struct {
	client frontend.LocalLibraryFrontendClient
}

// Create a new connection to the frontend gRPC server
func NewClient(conn *grpc.ClientConn) *LocalLibraryFrontendClient {
	return &LocalLibraryFrontendClient{
		client: frontend.NewLocalLibraryFrontendClient(conn),
	}
}
