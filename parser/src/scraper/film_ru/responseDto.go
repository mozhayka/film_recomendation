package film_ru

type predictDto struct {
	//Maybe struct {
	//	Name  string `json:"name"`
	//	Count int    `json:"count"`
	//	Data  []struct {
	//		Nid        string `json:"nid"`
	//		Href       string `json:"href"`
	//		Year       string `json:"year"`
	//		ImageUrl   string `json:"image_url"`
	//		Director   string `json:"director"`
	//		Genres     string `json:"genres"`
	//		Countries  string `json:"countries"`
	//		Runtime    string `json:"runtime"`
	//		MovieType  string `json:"movie_type"`
	//		Type       string `json:"type"`
	//		FieldText  string `json:"field_text"`
	//		CleanTitle string `json:"clean_title"`
	//		IsSerial   bool   `json:"is_serial"`
	//		Title      string `json:"title"`
	//	} `json:"data"`
	//} `json:"maybe"`
	Movies struct {
		//Name            string `json:"name"`
		//Count           int    `json:"count"`
		//SearchLink      string `json:"search_link"`
		//SearchLinkTitle string `json:"search_link_title"`
		Data []struct {
			//Nid        string `json:"nid"`
			Href string `json:"href"`
			//Year       string `json:"year"`
			//ImageUrl   string `json:"image_url"`
			//Director   string `json:"director"`
			//Genres     string `json:"genres"`
			//Countries  string `json:"countries"`
			//Runtime    string `json:"runtime"`
			//MovieType  string `json:"movie_type"`
			//Type       string `json:"type"`
			//FieldText  string `json:"field_text"`
			CleanTitle string `json:"clean_title"`
			IsSerial   bool   `json:"is_serial"`
			//Title      string `json:"title"`
		} `json:"data"`
		//TotalFound string `json:"total_found"`
	} `json:"movies"`
	//Persona struct {
	//	Name            string `json:"name"`
	//	Count           int    `json:"count"`
	//	SearchLink      string `json:"search_link"`
	//	SearchLinkTitle string `json:"search_link_title"`
	//	Data            []struct {
	//		Nid        string      `json:"nid"`
	//		Href       string      `json:"href"`
	//		ImageUrl   string      `json:"image_url"`
	//		Director   interface{} `json:"director"`
	//		Genres     interface{} `json:"genres"`
	//		Countries  interface{} `json:"countries"`
	//		MovieType  string      `json:"movie_type"`
	//		Type       string      `json:"type"`
	//		FieldText  string      `json:"field_text"`
	//		CleanTitle string      `json:"clean_title"`
	//		IsSerial   interface{} `json:"is_serial"`
	//		Title      string      `json:"title"`
	//	} `json:"data"`
	//	TotalFound string `json:"total_found"`
	//} `json:"persona"`
	//Article struct {
	//	Name            string `json:"name"`
	//	Count           int    `json:"count"`
	//	SearchLink      string `json:"search_link"`
	//	SearchLinkTitle string `json:"search_link_title"`
	//	Data            []struct {
	//		Nid        string      `json:"nid"`
	//		Href       string      `json:"href"`
	//		ImageUrl   string      `json:"image_url"`
	//		Director   interface{} `json:"director"`
	//		Genres     interface{} `json:"genres"`
	//		Countries  interface{} `json:"countries"`
	//		MovieType  string      `json:"movie_type"`
	//		Type       string      `json:"type"`
	//		FieldText  string      `json:"field_text"`
	//		CleanTitle string      `json:"clean_title"`
	//		IsSerial   interface{} `json:"is_serial"`
	//		Title      string      `json:"title"`
	//	} `json:"data"`
	//	TotalFound string `json:"total_found"`
	//} `json:"article"`
	//Data struct {
	//	SearchStr string `json:"search_str"`
	//} `json:"data"`
	//UserMoviesLists string `json:"user_movies_lists"`
}
