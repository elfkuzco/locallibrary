package models

import "time"

type BookInstance struct {
	ID         string     `json:"id"`
	Available  bool       `json:"is_available"`
	BorrowerID *string    `json:"borrower_id"`
	DueDate    *time.Time `json:"due_date"`
}

type BookBase struct {
	ISBN          string   `json:"isbn"`
	Title         string   `json:"title"`
	PublisherName string   `json:"publisher_name"`
	Summary       *string  `json:"summary"`
	Categories    []string `json:"categories"`
}

type Book struct {
	BookBase
	CreatedAt time.Time       `json:"created_at"`
	Copies    []*BookInstance `json:"copies"`
}
