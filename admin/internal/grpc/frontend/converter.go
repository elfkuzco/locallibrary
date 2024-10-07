package frontend

import (
	"github.com/elfkuzco/locallibrary/admin/internal/models"
	"github.com/elfkuzco/locallibrary/grpc/golang/frontend"
)

// Create a book model from the gRPC response.
func createBookFromResponse(response *frontend.BookDetail) *models.Book {
	book := &models.Book{
		BookBase: models.BookBase{
			ISBN:          response.Isbn,
			Title:         response.Title,
			PublisherName: response.PublisherName,
			Summary:       response.Summary,
			Categories:    response.Categories,
		},
		CreatedAt: response.CreatedAt.AsTime(),
		Copies:    []*models.BookInstance{},
	}
	for _, bookCopy := range response.Copies {
		bCopy := &models.BookInstance{
			ID:         bookCopy.Id,
			BorrowerID: bookCopy.BorrowerId,
			Available:  bookCopy.IsAvailable,
		}
		if bookCopy.DueDate != nil {
			dueDate := bookCopy.DueDate.AsTime()
			bCopy.DueDate = &dueDate
		}
		book.Copies = append(book.Copies, bCopy)
	}
	return book
}
