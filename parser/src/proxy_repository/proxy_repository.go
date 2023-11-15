package proxy_repository

import (
	"container/ring"
	"errors"
	"fmt"
	"net/http"
	"net/url"
	"parser/src/client"
	"parser/src/modifiers"
	"strings"
	"sync"
	"time"
)

type proxyRepository struct {
	proxies *ring.Ring
	mu      sync.Mutex
}

func NewProxyRepository() *proxyRepository {
	return &proxyRepository{
		mu: sync.Mutex{},
	}
}

func (r *proxyRepository) Run() error {
	err := r.updateProxyList()
	if err != nil {
		return err
	}

	l := r.proxies.Len()
	fmt.Println(l)

	ticker := time.NewTicker(10 * time.Minute)
	for {
		select {
		case <-ticker.C:
			err = r.updateProxyList()
			if err != nil {
				return err
			}

		default:
			time.Sleep(1 * time.Minute)
		}
	}
}

func (r *proxyRepository) GetProxy() proxy {
	r.mu.Lock()
	defer r.mu.Unlock()

	return r.proxies.Value.(proxy)
}

func (r *proxyRepository) updateProxyList() error {
	r.mu.Lock()
	defer r.mu.Unlock()

	proxies := struct {
		mu      sync.Mutex
		proxies map[string]proxy
	}{
		proxies: make(map[string]proxy),
		mu:      sync.Mutex{},
	}

	wg := sync.WaitGroup{}

	errs := make([]error, 0)
	for _, source := range proxySources {
		wg.Add(1)
		go func(source proxySource) {
			defer wg.Done()
			ps, err := getProxyList(source)
			if err != nil {
				errs = append(errs, err)
				return
			}

			localWg := sync.WaitGroup{}
			localWg.Add(len(ps))

			for _, p := range ps {
				go func(p proxy) {
					defer localWg.Done()
					if !checkProxy(p) {
						return
					}
					proxies.mu.Lock()
					if _, ok := proxies.proxies[p.host]; !ok {
						proxies.proxies[p.host] = p
					}
					proxies.mu.Unlock()
				}(p)
			}
			localWg.Wait()

		}(source)
	}

	wg.Wait()

	r.proxies = ring.New(len(proxies.proxies))
	for _, p := range proxies.proxies {
		r.proxies.Value = p
		r.proxies = r.proxies.Next()
	}

	return errors.Join(errs...)
}

func checkProxy(p proxy) bool {
	cl := client.NewDataRetriever()

	prUrl, err := url.Parse(fmt.Sprintf("%s://%s", p.scheme, p.host))
	if err != nil {
		return false
	}
	cl.WithTransport(&http.Transport{
		Proxy: http.ProxyURL(prUrl),
	})

	cl.WithTimeout(5 * time.Second)

	if err := cl.GetData("https://ip.me/", nil, nil, modifiers.WithResponseModifiers(modifiers.WithStatusCodeChecker())); err != nil {
		return false
	}
	return true
}

func getProxyList(ps proxySource) ([]proxy, error) {
	cl := client.NewDataRetriever()
	var rawProxies string

	if err := cl.GetData(ps.addr, nil, nil, modifiers.WithResponseModifiers(
		modifiers.WithStatusCodeChecker(),
		func(r *http.Response, body []byte) error {
			rawProxies = string(body)
			return nil
		}),
	); err != nil {
		return nil, err
	}

	addrs := strings.Split(rawProxies, "\n")

	proxies := make([]proxy, 0, len(addrs))

	for _, addr := range addrs {
		addr = strings.TrimSpace(addr)
		if addr == "" {
			continue
		}
		proxies = append(proxies, proxy{
			scheme: ps.scheme,
			host:   addr,
		})
	}

	return proxies, nil
}

var proxySources = []proxySource{
	{"https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt", "http"},
	{"https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/http.txt", "http"},
	{"https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/http.txt", "http"},
	{"https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt", "socks5"},
	{"https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/socks5.txt", "socks5"},
}

type proxySource struct {
	addr   string
	scheme string
}

type proxy struct {
	scheme string
	host   string
}
