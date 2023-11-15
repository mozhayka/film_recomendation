package transport_repository

import (
	"net/http"
)

type TransportRepository interface {
	GetTransport() http.RoundTripper
}
