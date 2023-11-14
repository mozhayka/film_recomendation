package client

import (
	"compress/gzip"
	"encoding/json"
	"io"
	"net/http"
	"time"
)

type DataRetriever struct {
	*http.Client
}

func NewClient() *DataRetriever {
	return &DataRetriever{
		Client: http.DefaultClient,
	}
}

func (c *DataRetriever) WithTimeout(timeout time.Duration) {
	c.Client.Timeout = timeout
}

func (c *DataRetriever) WithTransport(transport http.RoundTripper) {
	c.Client.Transport = transport
}

func (c *DataRetriever) GetData(url string, buf interface{}, reqModifiers []func(*http.Request), respModifiers []func(r *http.Response, body []byte) error) error {
	req, err := http.NewRequest(http.MethodGet, url, nil)
	if err != nil {
		return err
	}
	resp, err := c.do(req, reqModifiers...)
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

func (c DataRetriever) do(req *http.Request, reqModifiers ...func(r *http.Request)) (*http.Response, error) {
	for _, modifier := range reqModifiers {
		modifier(req)
	}
	return c.Client.Do(req)
}
