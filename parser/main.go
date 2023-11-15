package main

import (
	"github.com/gin-gonic/gin"
	"net/http"
	"parser/src/data_retriever"
	"parser/src/scraper"
	"parser/src/scraper/film_ru"
	"parser/src/scraper/ivi"
	"parser/src/transport_repository"
)

type filmsRequest struct {
	By    string `json:"by" binding:"required,oneof=title link"`
	Query string `json:"query" binding:"required"`
}

type predictsRequest struct {
	Prefix string `json:"prefix" binding:"required"`
}

func main() {
	r := gin.Default()

	trasportRepo := transport_repository.NewTransportRepository()
	scrapers := make(map[string]scraper.Scraper)

	scrapers["ivi"] = ivi.NewScraper(data_retriever.NewDataRetriever(trasportRepo))
	scrapers["film_ru"] = film_ru.NewScraper(data_retriever.NewDataRetriever(trasportRepo))

	r.GET("/:source/films", func(c *gin.Context) {
		fr := filmsRequest{}

		source := c.Param("source")
		sc, ok := scrapers[source]
		if !ok {
			c.JSON(http.StatusBadRequest, gin.H{"error": "source not found"})
			return
		}

		if err := c.ShouldBindJSON(&fr); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}

		var res *scraper.FilmsScrapeData
		var err error

		switch fr.By {
		case "title":
			res, err = sc.ScrapeNeighborsByTitle(fr.Query)
		case "link":
			res, err = sc.ScrapeNeighborsByLink(fr.Query)
		}

		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}

		c.JSON(http.StatusOK, res)
	})

	r.GET("/:source/predicts", func(c *gin.Context) {
		pr := predictsRequest{}

		source := c.Param("source")
		sc, ok := scrapers[source]
		if !ok {
			c.JSON(http.StatusBadRequest, gin.H{"error": "source not found"})
			return
		}

		if err := c.ShouldBindJSON(&pr); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}

		res, err := sc.Predict(pr.Prefix)

		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}

		c.JSON(http.StatusOK, res)
	})

	r.Run()
}
