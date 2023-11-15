package utils

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strings"
)

const (
	ProxyWhiteList = `./utils/proxywhite.txt`
)

func GetProxies() ([]string, error) {
	proxyFile, err := os.Open(ProxyWhiteList)
	if err != nil {
		return nil, err
	}
	defer proxyFile.Close()

	reader := bufio.NewReader(proxyFile)

	proxies := make([]string, 0, 100)
	props := make([]string, 0, 3)

	for i := 0; i < 3; i++ {
		line, err := reader.ReadString('\n')
		if err != nil {
			return nil, err
		}
		cuts := strings.Split(line, ": ")
		props = append(props, strings.TrimSpace(cuts[1]))
	}

	for {
		line, err := reader.ReadString('\n')
		if err == io.EOF {
			break
		}
		if err != nil {
			return nil, err
		}
		proxies = append(proxies, fmt.Sprintf("%s://%s:%s@%s", props[0], props[1], props[2], strings.TrimSpace(line)))
	}

	return proxies, nil
}
