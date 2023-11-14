package scraper

type Scraper interface {
	ScrapeNeighborsByLink(link string) (*FilmsScrapeData, error)
	ScrapeNeighborsByTitle(title string) (*FilmsScrapeData, error)
	Predict(prefix string) (*FilmsScrapeData, error)
}
