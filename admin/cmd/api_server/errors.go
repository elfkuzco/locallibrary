package main

import (
	"fmt"
	"log"
	"net/http"
	"runtime/debug"

	"github.com/elfkuzco/locallibrary/admin/internal/json"
)

type Error struct {
	Code    int               `json:"code"`
	Message string            `json:"message,omitempty"`
	Errors  map[string]string `json:"errors,omitempty"`
}

func (app *application) errorResponse(w http.ResponseWriter, r *http.Request, e Error) {
	err := json.WriteJSON(w, e.Code, e, nil)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
	}
}

func (app *application) serverErrorResponse(w http.ResponseWriter, r *http.Request, err error) {
	trace := fmt.Sprintf("%s\n%s", err.Error(), debug.Stack())
	err = log.Output(2, trace)
	if err != nil {
		app.logger.Error("error building trace error ouput", "err", err)
	}
	app.errorResponse(w, r, Error{
		Code:    http.StatusInternalServerError,
		Message: "the server encountered a problem and could not process the request",
	})
}

func (app *application) badRequestResponse(w http.ResponseWriter, r *http.Request, e error) {
	err := Error{
		Code:    http.StatusBadRequest,
		Message: e.Error(),
	}
	app.errorResponse(w, r, err)
}
