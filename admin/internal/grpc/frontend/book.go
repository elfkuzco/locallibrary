package frontend

import (
	"context"

	"github.com/elfkuzco/locallibrary/admin/internal/models"
	"github.com/elfkuzco/locallibrary/grpc/golang/frontend"
)

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

// Remove a book from the catalogue
func (f *LocalLibraryFrontendClient) RemoveBook(ctx context.Context, isbn string) error {
	var err error
	_, err = f.client.RemoveBook(ctx, &frontend.RemoveBookRequest{Isbn: isbn})
	if err != nil {
		return err
	}
	return err
}
