package ivi

type PredictDto struct {
	Result []struct {
		//Categories       []int    `json:"categories,omitempty"`
		//ContentPaidTypes []string `json:"content_paid_types,omitempty"`
		//Country          int      `json:"country,omitempty"`
		//ExtraProperties  struct {
		//} `json:"extra_properties,omitempty"`
		//Genres       []int   `json:"genres,omitempty"`
		//Hru          *string `json:"hru,omitempty"`
		Id int `json:"id,omitempty"`
		//Kind         int    `json:"kind,omitempty"`
		ObjectType string `json:"object_type"`
		//Restrict     *int   `json:"restrict,omitempty"`
		Title string `json:"title,omitempty"`
		//UsedToBePaid bool   `json:"used_to_be_paid,omitempty"`
		//Years        []int  `json:"years,omitempty"`
		//Year         int    `json:"year,omitempty"`
		//Name         string `json:"name,omitempty"`
		//PersonTypes  []struct {
		//	Id    int    `json:"id"`
		//	Title string `json:"title"`
		//} `json:"person_types,omitempty"`
		//Current struct {
		//	Category string    `json:"category"`
		//	End      time.Time `json:"end"`
		//	Start    time.Time `json:"start"`
		//	Title    string    `json:"title"`
		//} `json:"current,omitempty"`
	} `json:"result"`
}
