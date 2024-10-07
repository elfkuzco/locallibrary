package main

import (
	"flag"
	"fmt"
	"log"
	"log/slog"
	"os"
	"sync"

	"github.com/elfkuzco/locallibrary/admin/internal/grpc/frontend"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

type config struct {
	port                  int
	frontendServerAddress string
	mode                  string
}

type application struct {
	config             config
	wg                 sync.WaitGroup
	frontendgRPCClient *frontend.LocalLibraryFrontendClient
	logger             *slog.Logger
}

var (
	buildTime string // to hold the time the executable was built
	version   string // to hold the version number
)

func main() {
	var cfg config
	flag.IntVar(&cfg.port, "port", 80, "REST API server port")
	flag.StringVar(&cfg.mode, "environment", "development", "Environment (development|production)")
	flag.StringVar(&cfg.frontendServerAddress, "frontend-grpc-server-address",
		"localhost:50051", "Address of the frontend gRPC server.")
	// boolean to display version
	displayVersion := flag.Bool("version", false, "Display version and exit")

	flag.Parse()

	// If the version flag is true, print the version number and exit
	if *displayVersion {
		fmt.Printf("Version:\t%s\n", version)
		fmt.Printf("Build time:\t%s\n", buildTime)
		os.Exit(0)
	}
	// set up the application logger
	var logLevel = new(slog.LevelVar) // info by default
	if cfg.mode == "development" {
		logLevel.Set(slog.LevelDebug)
	} else {
		logLevel.Set(slog.LevelInfo)
	}
	logger := slog.New(slog.NewTextHandler(os.Stdout, &slog.HandlerOptions{Level: logLevel}))

	var opts []grpc.DialOption
	if cfg.mode == "development" {
		opts = append(opts, grpc.WithTransportCredentials(insecure.NewCredentials()))
	}

	conn, err := grpc.NewClient(cfg.frontendServerAddress, opts...)
	if err != nil {
		log.Fatalf("fail to dial: %v", err)
	}
	defer conn.Close()

	app := &application{
		config:             cfg,
		wg:                 sync.WaitGroup{},
		logger:             logger,
		frontendgRPCClient: frontend.NewClient(conn),
	}

	err = app.serve()
	if err != nil {
		logger.Error("error serving application", "err", err)
		os.Exit(1)
	}
}
