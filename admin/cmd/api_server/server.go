package main

import (
	"context"
	"errors"
	"fmt"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"
)

func (app *application) serve() error {
	srv := &http.Server{
		Addr:    fmt.Sprintf(":%d", app.config.port),
		Handler: app.routes(),
		// Add Idle, Read and Write timeouts to the server
		IdleTimeout:  time.Minute,
		ReadTimeout:  5 * time.Second,
		WriteTimeout: 10 * time.Second,
	}

	// channel to receive any errors returned by the graceful Shutdown()
	// function.
	shutdownError := make(chan error)

	go func() {
		quit := make(chan os.Signal, 1)
		// Listen for incoming SIGINT and SIGTERM signals
		// and relay them to the quit channel. Any other signal will
		// not be caught by signal.Notify() and will retain their
		// default behaviour
		signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)

		// Read the signal from the quit channel
		s := <-quit
		app.logger.Info("caught a signal", "signal", s)

		// Create a context with a 5-second timeout
		ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
		defer cancel()

		// Call Shutdown() on the server, passing in the context.
		// Shutdown() will return nil if the graceful shutdown was successful,
		// or an error (which may happen because of a problem closing the
		// listeners, or because the shutdown didn't complete before the 5-second
		// context deadline is hit).
		// We relay this return value to the shutdownError channel
		err := srv.Shutdown(ctx)
		if err != nil {
			shutdownError <- err
		}
		app.logger.Info("waiting for background tasks to complete")

		// Block until our WaitGroup counter is zero --- essentially blocking
		// until the background goroutines have finished. Then, we return nil
		// on the shutdownError channel, to indicate that the shutdown complted
		// without any issues
		app.wg.Wait()
		shutdownError <- nil
	}()

	app.logger.Info("Starting server", "port", app.config.port, "mode", app.config.mode)

	// Calling Shutdown() on our server will cause ListenAndServe() to immediately
	// return a http.ErrServerClosed error. So, if we see this error, it is actually
	// good thing and an indication	that the graceful shutdown has started. So, we
	// check specifically for this, only returning the error it is NOT
	// http.ErrServerClosed

	err := srv.ListenAndServe()
	if !errors.Is(err, http.ErrServerClosed) {
		return err
	}

	// Otherwise, we wait to receive the return value from Shutdown() on the
	// shutdownError channel. If return value is an error, we know that there was
	// a problem with the graceful shutdown and we return  the error.

	err = <-shutdownError
	if err != nil {
		return err
	}

	app.logger.Info("Stopped server")
	return nil
}
