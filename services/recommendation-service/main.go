// TrailHead Supply Co. — Recommendation Engine
// Stack: Go 1.22, standard library net/http only (no framework, no external deps)
//
// Calls the Catalogue Service to build "you might also like" suggestions
// using category affinity + a lightweight popularity score. This mirrors
// how a real recommendation service sits *beside* the catalogue rather
// than owning product data itself.
package main

import (
	"encoding/json"
	"log"
	"math/rand"
	"net/http"
	"os"
	"sort"
	"time"

	"github.com/prometheus/client_golang/prometheus/promhttp"
)

type Product struct {
	ID       string   `json:"id"`
	Name     string   `json:"name"`
	Category string   `json:"category"`
	Price    float64  `json:"price"`
	Image    string   `json:"image"`
	Tags     []string `json:"tags"`
}

type productList struct {
	Items []Product `json:"items"`
}

type Recommendation struct {
	Product Product `json:"product"`
	Score   float64 `json:"score"`
	Reason  string  `json:"reason"`
}

var (
	catalogueURL = getEnv("CATALOGUE_SERVICE_URL", "http://localhost:8001")
	serviceName  = "recommendation-service"
	version      = getEnv("SERVICE_VERSION", "1.0.0")
	startTime    = time.Now()
	httpClient   = &http.Client{Timeout: 3 * time.Second}
)

func getEnv(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}

func fetchCatalogue() ([]Product, error) {
	resp, err := httpClient.Get(catalogueURL + "/api/products")
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	var pl productList
	if err := json.NewDecoder(resp.Body).Decode(&pl); err != nil {
		return nil, err
	}
	return pl.Items, nil
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]interface{}{
		"status":         "UP",
		"service":        serviceName,
		"version":        version,
		"uptime_seconds": time.Since(startTime).Seconds(),
	})
}

// recommendationsHandler returns items from the same category as the
// given product, ranked by a pseudo-popularity score, excluding the
// product itself. Falls back to cross-category "trending" picks if the
// category has fewer than 3 companions.
func recommendationsHandler(w http.ResponseWriter, r *http.Request) {
	productID := r.URL.Query().Get("productId")
	if productID == "" {
		http.Error(w, `{"error":"productId query param is required"}`, http.StatusBadRequest)
		return
	}

	all, err := fetchCatalogue()
	if err != nil {
		log.Printf("catalogue fetch failed: %v", err)
		http.Error(w, `{"error":"catalogue service unavailable"}`, http.StatusBadGateway)
		return
	}

	var source *Product
	for i := range all {
		if all[i].ID == productID {
			source = &all[i]
			break
		}
	}
	if source == nil {
		http.Error(w, `{"error":"product not found"}`, http.StatusNotFound)
		return
	}

	seed := hashSeed(productID)
	rnd := rand.New(rand.NewSource(seed))

	var recs []Recommendation
	for _, p := range all {
		if p.ID == source.ID {
			continue
		}
		score := 0.0
		reason := "trending"
		if p.Category == source.Category {
			score += 0.6
			reason = "same category: " + p.Category
		}
		for _, t1 := range p.Tags {
			for _, t2 := range source.Tags {
				if t1 == t2 {
					score += 0.15
					reason = "shared style: " + t1
				}
			}
		}
		score += rnd.Float64() * 0.2 // popularity jitter, deterministic per product
		recs = append(recs, Recommendation{Product: p, Score: round2(score), Reason: reason})
	}

	sort.Slice(recs, func(i, j int) bool { return recs[i].Score > recs[j].Score })
	if len(recs) > 4 {
		recs = recs[:4]
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]interface{}{
		"productId":       productID,
		"recommendations": recs,
	})
}

func hashSeed(s string) int64 {
	var h int64 = 0
	for _, c := range s {
		h = h*31 + int64(c)
	}
	return h
}

func round2(f float64) float64 {
	return float64(int(f*100)) / 100
}

func withCORS(next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", "*")
		next(w, r)
	}
}

func main() {
	port := getEnv("PORT", "8002")

	mux := http.NewServeMux()
	mux.HandleFunc("/health", withCORS(healthHandler))
	mux.HandleFunc("/api/recommendations", withCORS(recommendationsHandler))
	mux.Handle("/metrics", promhttp.Handler())

	log.Printf("%s v%s listening on :%s (catalogue=%s)", serviceName, version, port, catalogueURL)
	if err := http.ListenAndServe(":"+port, mux); err != nil {
		log.Fatal(err)
	}
}
