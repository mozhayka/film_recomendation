package scraper

type FilmsScrapeData struct {
	Films []Film `json:"films"`
}

type Film struct {
	Name string `json:"name"`
	Link string `json:"link"`
}
