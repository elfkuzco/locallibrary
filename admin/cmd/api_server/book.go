package main

import (
	"net/http"

	"github.com/elfkuzco/locallibrary/admin/internal/json"
	"github.com/elfkuzco/locallibrary/admin/internal/models"
	"github.com/go-chi/chi/v5"
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
		app.statusConflictResponse(w, r, err)
		return
	}
	err = json.WriteJSON(w, http.StatusOK, response, nil)
	if err != nil {
		app.serverErrorResponse(w, r, err)
	}

}

func (app *application) RemoveBook(w http.ResponseWriter, r *http.Request) {
	isbn := chi.URLParam(r, "isbn")
	err := app.frontendgRPCClient.RemoveBook(r.Context(), isbn)
	if err != nil {
		app.badRequestResponse(w, r, err)
		return
	}
	err = json.WriteJSON(w, http.StatusOK, map[string]string{"status": "ok"}, nil)
	if err != nil {
		app.serverErrorResponse(w, r, err)
	}

}
