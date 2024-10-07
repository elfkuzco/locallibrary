package json

import (
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"strings"
)

// Reads the JSON payload from the request body. Returns a more descriptive error
// than Go's default error messages due to failure in Marshalling
func ReadJSON(w http.ResponseWriter, r *http.Request, dst interface{}) error {
	maxBytes := 1_048_576 * 2 // limit size of the request data to 2MB
	r.Body = http.MaxBytesReader(w, r.Body, int64(maxBytes))
	// Initialize the decoder and disallow decoding of unknown values
	dec := json.NewDecoder(r.Body)
	dec.DisallowUnknownFields()
	err := dec.Decode(dst)
	if err != nil {
		var syntaxError *json.SyntaxError
		var unmarshalTypeError *json.UnmarshalTypeError
		var invalidUnmarshalError *json.InvalidUnmarshalError

		switch {
		// Check for errors using errors.As() and
		// return more desriptive error messages
		case (errors.As(err, &syntaxError)):
			return fmt.Errorf("body contains badly-formed JSON (at character %d)", syntaxError.Offset)
		case (errors.Is(err, io.ErrUnexpectedEOF)):
			return errors.New("body contains badly malformed JSON")
		case errors.As(err, &unmarshalTypeError):
			if unmarshalTypeError.Field != "" {
				return fmt.Errorf("body contains incorrect JSON type for field %q", unmarshalTypeError.Field)
			}
			return fmt.Errorf("body contains incorrect JSON type (at character %d)", unmarshalTypeError.Offset)
		case errors.Is(err, io.EOF):
			return errors.New("body must not be empty")
		// If the JSON contains a field which cannot be mapped to the
		// target destination, then Decode() will now return an error
		// message in the format "json:unknown field '<name>'".
		// We check for this, extract the field name from the
		// error, an.d interpolate into our custom error message.
		case strings.HasPrefix(err.Error(), "json: unknown field "):
			fieldName := strings.TrimPrefix(err.Error(), "json: unknown field ")
			return fmt.Errorf("body contains unknown key %s", fieldName)
		// If the request body exceeds 1MB in size, the decode will
		// now fail with the error "http: request body too large"
		case err.Error() == "http: request body too large":
			return fmt.Errorf("body must not be larger than %d bytes", maxBytes)
		case errors.As(err, &invalidUnmarshalError):
			panic(err)
		default:
			return err
		}
	}

	// Call decode again, using a pointer to an empty anonymous struct
	// as the destination. If the request body only contained a single
	// JSON object, this will return an io.EOF error. So, if we get
	// anything else, we know that there is additional data in the
	// request body.
	err = dec.Decode(&struct{}{})
	if !errors.Is(err, io.EOF) {
		return errors.New("body must only contain a single JSON value")
	}
	return nil
}

// Takes the destination http.ResponseWriter, the http status code to send, the data
// to encode to JSON and a header map containing any additional HTTP headers we want
// to include in the response
func WriteJSON(w http.ResponseWriter, status int, data interface{}, headers http.Header) error {
	js, err := json.Marshal(data)
	if err != nil {
		return err
	}

	for key, value := range headers {
		w.Header()[key] = value
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	w.Write(js)

	return nil
}
