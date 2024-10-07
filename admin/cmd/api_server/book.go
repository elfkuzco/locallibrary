package main

import (
	"net/http"

	"github.com/elfkuzco/locallibrary/admin/internal/json"
	"github.com/elfkuzco/locallibrary/admin/internal/models"
)

func (app *application) AddBook(w http.ResponseWriter, r *http.Request) {
	var input models.BookBase
	var err error

	err = json.ReadJSON(w, r, &input)
	if err != nil {
		app.badRequestResponse(w, r, err)
		return
	}

	response, err := app.frontendgRPCClient.AddBook(r.Context(), &input)
	if err != nil {
		app.errorResponse(
			w, r, Error{
				Code:    http.StatusConflict,
				Message: err.Error(),
			})
		return
	}
	err = json.WriteJSON(w, http.StatusOK, response, nil)
	if err != nil {
		app.serverErrorResponse(w, r, err)
	}

}
