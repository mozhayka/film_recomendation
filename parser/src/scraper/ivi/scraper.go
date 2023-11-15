package ivi

import (
	"bytes"
	"fmt"
	"github.com/PuerkitoBio/goquery"
	"net/http"
	"net/url"
	"parser/src/data_retriever"
	modifiers2 "parser/src/modifiers"
	scraperPkg "parser/src/scraper"
	"regexp"
	"strings"
)

const (
	baseUrl            = "https://www.ivi.tv"
	predictUrlTemplate = "https://api2.ivi.ru/mobileapi/autocomplete/common/v7/?object_type=content&object_type=semantic_query&object_type=person&object_type=telecast&object_type=tvchannel&app_version=870&fields=object_type%2Cperson_types%2Cname%2Ctitle%2Cid%2Chru%2Ccategories%2Cposter_originals%2Ckind%2Crestrict%2Ccontent_paid_types%2Cpreorderable%2Cfake%2Cused_to_be_paid%2Ccountry%2Cyear%2Cduration_minutes%2Cgenres%2Cyears%2Cextra_properties.future_svod%2Cextra_properties.future_est%2Cextra_properties.future_avod%2Cextra_properties.future_tvod%2Cextra_properties.soon_ivi%2Ctvchannel_id%2Ctvchannel_title%2Ctvchannel_hru%2Cstart%2Cend%2Ccategory%2Clive%2Ccurrent&limit=9&query={{query}}&withpreorderable=1"
	filmUrlTemplate    = baseUrl + "/watch/%d"
)

type scraper struct {
	client data_retriever.DataRetriever
}

func NewScraper(client data_retriever.DataRetriever) *scraper {
	return &scraper{
		client: client,
	}
}

func (s *scraper) ScrapeNeighborsByLink(link string) (*scraperPkg.FilmsScrapeData, error) {

	var res *scraperPkg.FilmsScrapeData

	err := s.client.GetData(link, nil, setHeaders(), modifiers2.WithResponseModifiers(
		modifiers2.WithStatusCodeChecker(),
		func(r *http.Response, body []byte) error {
			var err error
			res, err = parseFilms(body)
			return err
		}))
	if err != nil {
		return nil, err
	}

	res.Movie.Link = link

	return res, nil
}

func (s *scraper) ScrapeNeighborsByTitle(title string) (*scraperPkg.FilmsScrapeData, error) {
	pr, err := s.Predict(title)
	if err != nil {
		return nil, err
	}

	if len(pr.RecommendedMovies) == 0 {
		return nil, fmt.Errorf("no films found")
	}

	u := pr.RecommendedMovies[0].Link

	return s.ScrapeNeighborsByLink(u)

}

func (s *scraper) Predict(prefix string) (*scraperPkg.FilmsScrapeData, error) {
	u := strings.ReplaceAll(predictUrlTemplate, "{{query}}", url.QueryEscape(prefix))
	var result predictDto
	err := s.client.GetData(u, &result, setHeaders(), modifiers2.WithResponseModifiers(modifiers2.WithStatusCodeChecker()))
	if err != nil {
		return nil, err
	}

	res := &scraperPkg.FilmsScrapeData{
		Movie: scraperPkg.Film{
			Title: prefix,
		},
		RecommendedMovies: []scraperPkg.Film{},
	}
	for _, film := range result.Result {
		if film.ObjectType == "video" {
			res.RecommendedMovies = append(res.RecommendedMovies, scraperPkg.Film{
				Title: film.Title,
				Link:  fmt.Sprintf(filmUrlTemplate, film.Id),
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
		RecommendedMovies: []scraperPkg.Film{},
	}

	doc.Find("li[class='breadCrumbs__item']").Each(func(i int, s *goquery.Selection) {
		span := s.Find("span")
		if span == nil {
			return
		}
		res.Movie.Title = span.Text()
	})

	doc.Find("a[data-test='watch_also_item']").Each(func(i int, s *goquery.Selection) {
		l, ok := s.Attr("href")
		if !ok || !isFilmLink(l) {
			return
		}

		title := s.Find("span[class='nbl-slimPosterBlock__titleText']").Text()

		res.RecommendedMovies = append(res.RecommendedMovies, scraperPkg.Film{
			Title: title,
			Link:  baseUrl + l,
		})
	})

	return res, nil
}

func setHeaders() []func(r *http.Request) {
	return modifiers2.WithRequestModifiers(
		modifiers2.WithHeaders(
			http.Header{
				"Host":            []string{"www.ivi.tv"},
				"User-Agent":      []string{"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"},
				"Accept":          []string{"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"},
				"Accept-Language": []string{"ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3"},
				"Accept-Encoding": []string{"gzip, deflate, br"},
				"Referer":         []string{"https://www.ivi.tv/?ivi_search"},
			},
		),
	)
}

func isFilmLink(s string) bool {
	re := regexp.MustCompile(`^/watch/(\d+)$`)

	return re.MatchString(s)
}
