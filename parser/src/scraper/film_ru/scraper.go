package film_ru

import (
	"bytes"
	"fmt"
	"github.com/PuerkitoBio/goquery"
	"net/http"
	"net/url"
	"parser/src/client"
	modifiers2 "parser/src/modifiers"
	scraperPkg "parser/src/scraper"
	"strings"
)

const (
	baseUrl            = "https://www.film.ru"
	predictUrlTemplate = "https://www.film.ru/search/autocomplete/%s"
)

type scraper struct {
	client client.Client
}

func NewScraper(client client.Client) *scraper {
	return &scraper{
		client: client,
	}
}

func (s *scraper) ScrapeNeighborsByLink(link string) (*scraperPkg.FilmsScrapeData, error) {

	var res *scraperPkg.FilmsScrapeData

	err := s.client.GetData(link+"/similar", nil, setHeaders(), modifiers2.WithResponseModifiers(
		modifiers2.WithStatusCodeChecker(),
		func(r *http.Response, body []byte) error {
			var err error
			res, err = parseFilms(body)
			return err
		}))
	if err != nil {
		return nil, err
	}

	return res, nil
}

func (s *scraper) ScrapeNeighborsByTitle(title string) (*scraperPkg.FilmsScrapeData, error) {
	pr, err := s.Predict(title)
	if err != nil {
		return nil, err
	}

	if len(pr.Films) == 0 {
		return nil, fmt.Errorf("no films found")
	}

	u := pr.Films[0].Link

	return s.ScrapeNeighborsByLink(u)

}

func (s *scraper) Predict(prefix string) (*scraperPkg.FilmsScrapeData, error) {
	u := fmt.Sprintf(predictUrlTemplate, url.QueryEscape(prefix))
	var result predictDto
	err := s.client.GetData(u, &result, setHeaders(), modifiers2.WithResponseModifiers(modifiers2.WithStatusCodeChecker()))
	if err != nil {
		return nil, err
	}

	res := &scraperPkg.FilmsScrapeData{
		Films: []scraperPkg.Film{},
	}
	for _, film := range result.Movies.Data {
		if !film.IsSerial {
			res.Films = append(res.Films, scraperPkg.Film{
				Name: film.CleanTitle,
				Link: baseUrl + film.Href,
			})
		}
	}

	return res, nil
}

func parseFilms(body []byte) (*scraperPkg.FilmsScrapeData, error) {
	doc, err := goquery.NewDocumentFromReader(bytes.NewReader(body))
	if err != nil {
		return nil, err
	}

	res := &scraperPkg.FilmsScrapeData{
		Films: []scraperPkg.Film{},
	}

	doc.Find("div[class='block_movies wrapper_movies_similar']").Each(func(i int, s *goquery.Selection) {

		s.Find("a").Each(func(i int, s *goquery.Selection) {
			if _, ok := s.Attr("data-score"); !ok {
				return
			}

			l, ok := s.Attr("href")
			if !ok || !isFilmLink(l) {
				return
			}

			title, ok := s.Attr("title")
			if !ok {
				return
			}

			res.Films = append(res.Films, scraperPkg.Film{
				Name: title,
				Link: baseUrl + l,
			})

		})
	})

	return res, nil
}

func setHeaders() []func(r *http.Request) {
	return modifiers2.WithRequestModifiers(
		modifiers2.WithHeaders(
			http.Header{
				"Host":            []string{"www.film.ru"},
				"User-Agent":      []string{"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"},
				"Accept":          []string{"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"},
				"Accept-Language": []string{"ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3"},
				"Accept-Encoding": []string{"gzip, deflate, br"},
				"Referer":         []string{"https://www.film.ru/"},
			},
		),
	)
}

func isFilmLink(s string) bool {
	cuts := strings.Split(s, "/")

	if len(cuts) == 3 && cuts[1] == "movies" {
		return true
	}
	return false
}
