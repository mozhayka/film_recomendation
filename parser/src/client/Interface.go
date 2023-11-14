package client

import (
	"net/http"
	"time"
)

type Client interface {
	GetData(url string, buf interface{}, reqModifiers []func(*http.Request), respModifiers []func(r *http.Response, body []byte) error) error
	WithTransport(transport http.RoundTripper)
	WithTimeout(timeout time.Duration)
}
