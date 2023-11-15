package transport_repository

import (
	"container/ring"
	"golang.org/x/time/rate"
	"net/http"
	"net/url"
	"parser/utils"
	"sync"
)

type transportRepository struct {
	mu         sync.Mutex
	transports *ring.Ring
}

func NewTransportRepository() *transportRepository {
	proxies, _ := utils.GetProxies()

	repo := &transportRepository{
		mu:         sync.Mutex{},
		transports: ring.New(len(proxies)),
	}

	for _, proxy := range proxies {
		prUrl, _ := url.Parse(proxy)
		repo.transports.Value = &Transport{
			transport: &http.Transport{
				Proxy: http.ProxyURL(prUrl),
			},
			limiter: rate.NewLimiter(5, 1),
		}
		repo.transports = repo.transports.Next()
	}

	return repo
}

func (r *transportRepository) GetTransport() http.RoundTripper {
	r.mu.Lock()
	defer r.mu.Unlock()

	tr := r.transports.Value.(*Transport)
	r.transports = r.transports.Next()
	return tr
}
