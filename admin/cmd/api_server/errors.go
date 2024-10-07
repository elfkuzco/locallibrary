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
	log.Output(2, trace)
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

func (app *application) failedValidationResponse(w http.ResponseWriter, r *http.Request, e map[string]string) {
	err := Error{
		Code:   http.StatusUnprocessableEntity,
		Errors: e,
	}
	app.errorResponse(w, r, err)
}

func (app *application) notFoundResponse(w http.ResponseWriter, r *http.Request) {
	err := Error{
		Code:    http.StatusNotFound,
		Message: "Resource with specified ID does not exist",
	}
	app.errorResponse(w, r, err)
}

func (app *application) invalidAuthenticationTokenResponse(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("WWW-Authenticate", "Bearer")

	err := Error{
		Code:    http.StatusUnauthorized,
		Message: "Invalid or missing authentication token",
	}
	app.errorResponse(w, r, err)
}

func (app *application) authenticationRequiredResponse(w http.ResponseWriter, r *http.Request) {
	err := Error{
		Code:    http.StatusUnauthorized,
		Message: "You must be authenticated to access this resource",
	}
	app.errorResponse(w, r, err)
}

func (app *application) invalidStudentCreationTokenResponse(w http.ResponseWriter, r *http.Request) {
	err := Error{
		Code:    http.StatusUnauthorized,
		Message: "Invalid or missing creation token",
	}
	app.errorResponse(w, r, err)
}

func (app *application) rateLimitExceededResponse(w http.ResponseWriter, r *http.Request) {
	message := "rate limit exceeded"
	app.errorResponse(w, r, Error{
		Code:    http.StatusTooManyRequests,
		Message: message,
	})
}
