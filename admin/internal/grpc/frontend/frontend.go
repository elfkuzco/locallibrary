package frontend

import (
	"context"

	"github.com/elfkuzco/locallibrary/admin/internal/models"
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

// Add a book to the library catalogue
func (f *LocalLibraryFrontendClient) AddBook(ctx context.Context, input *models.BookBase) (*models.Book, error) {
	var err error

	response, err := f.client.AddBook(ctx,
		&frontend.AddBookRequest{
			Isbn:          input.ISBN,
			Title:         input.Title,
			PublisherName: input.PublisherName,
			Categories:    input.Categories,
			Summary:       input.Summary,
		})

	if err != nil {
		return nil, err
	}
	return createBookFromResponse(response), nil
}
