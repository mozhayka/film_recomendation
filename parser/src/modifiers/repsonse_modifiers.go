package modifiers

import (
	"fmt"
	"net/http"
)

func WithStatusCodeChecker() func(r *http.Response, body []byte) error {
	return func(resp *http.Response, body []byte) error {
		if resp.StatusCode >= 200 && resp.StatusCode < 300 {
			return nil
		}
		return fmt.Errorf("unexpected status code: %d", resp.StatusCode)
	}
}

func WithResponseModifiers(modifiers ...func(r *http.Response, body []byte) error) []func(r *http.Response, body []byte) error {
	return modifiers
}
