package proxy_repository

type ProxyRepository interface {
	GetProxy() (string, error)
}
