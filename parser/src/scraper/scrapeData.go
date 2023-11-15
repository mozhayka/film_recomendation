package scraper

type FilmsScrapeData struct {
	Movie             Film   `json:"movie"`
	RecommendedMovies []Film `json:"recommended_movies"`
}

type Film struct {
	Title string `json:"title"`
	Link  string `json:"link"`
}
