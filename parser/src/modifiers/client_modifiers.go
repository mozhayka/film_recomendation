package modifiers

import (
	"net/http"
	"time"
)

func WithTimeout(timeout time.Duration) func(client *http.Client) {
	return func(client *http.Client) {
		client.Timeout = timeout
	}
}

func WithTransport(transport http.RoundTripper) func(client *http.Client) {
	return func(client *http.Client) {
		client.Transport = transport
	}
}
