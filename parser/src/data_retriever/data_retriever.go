package data_retriever

import (
	"compress/gzip"
	"encoding/json"
	"io"
	"net/http"
	"parser/src/transport_repository"
)

type dataRetriever struct {
	transportRepo transport_repository.TransportRepository
}

func NewDataRetriever(transportRepo transport_repository.TransportRepository) *dataRetriever {
	return &dataRetriever{
		transportRepo: transportRepo,
	}
}

func (dr *dataRetriever) GetData(
	url string, buf interface{},
	reqModifiers []func(*http.Request),
	respModifiers []func(r *http.Response, body []byte) error,
	clientModifiers ...func(client *http.Client),
) error {
	req, err := http.NewRequest(http.MethodGet, url, nil)
	if err != nil {
		return err
	}

	for _, modifier := range reqModifiers {
		modifier(req)
	}

	var resp *http.Response
	for i := 0; i < 5; i++ {
		resp, err = dr.do(req, clientModifiers...)
		if err == nil {
			break
		}

	}
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	var body []byte

	if resp.Header.Get("Content-Encoding") == "gzip" {
		r, err := gzip.NewReader(resp.Body)
		if err != nil {
			return err
		}
		defer r.Close()
		body, err = io.ReadAll(r)
		if err != nil {
			return err
		}
	} else {
		body, err = io.ReadAll(resp.Body)
		if err != nil {
			return err
		}
	}

	for _, modifier := range respModifiers {
		err = modifier(resp, body)
		if err != nil {
			return err
		}
	}

	if buf == nil {
		return nil
	}

	return json.Unmarshal(body, buf)
}

func (dr *dataRetriever) do(req *http.Request, clientModifiers ...func(client *http.Client)) (*http.Response, error) {
	client := http.DefaultClient

	client.Transport = dr.transportRepo.GetTransport()
	for _, modifier := range clientModifiers {
		modifier(client)
	}

	return client.Do(req)
}
