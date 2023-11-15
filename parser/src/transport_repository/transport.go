package transport_repository

import (
	"context"
	"golang.org/x/time/rate"
	"net/http"
)

type Transport struct {
	transport http.RoundTripper
	limiter   *rate.Limiter
}

func (t *Transport) RoundTrip(req *http.Request) (*http.Response, error) {
	ctx := context.Background()

	err := t.limiter.Wait(ctx)
	if err != nil {
		return nil, err
	}

	return t.transport.RoundTrip(req)
}
