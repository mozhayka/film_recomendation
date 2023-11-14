package modifiers

import "net/http"

func WithHeaders(headers http.Header) func(r *http.Request) {
	return func(req *http.Request) {
		req.Header = headers
	}
}

func WithCookies(cookies []*http.Cookie) func(r *http.Request) {
	return func(req *http.Request) {
		for _, cookie := range cookies {
			req.AddCookie(cookie)
		}
	}
}

func WithRequestModifiers(modifiers ...func(r *http.Request)) []func(r *http.Request) {
	return modifiers
}
