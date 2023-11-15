package data_retriever

import (
	"net/http"
)

type DataRetriever interface {
	GetData(url string, buf interface{}, reqModifiers []func(*http.Request), respModifiers []func(r *http.Response, body []byte) error, clientModifiers ...func(client *http.Client)) error
}
