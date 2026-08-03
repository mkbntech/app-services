/**
 * TrailHead Supply Co. — Storefront UI
 * Stack: Node.js 20 + Express + EJS
 *
 * This service is the "backend for frontend": it renders HTML and fans
 * out to the three backend microservices (each on its own stack) to
 * assemble each page. No page ever talks to the backends directly.
 */
const express = require("express");
const axios = require("axios");
const path = require("path");

const app = express();
const PORT = process.env.PORT || 3000;

const CATALOGUE_URL = process.env.CATALOGUE_SERVICE_URL || "http://localhost:8001";
const RECOMMENDATION_URL = process.env.RECOMMENDATION_SERVICE_URL || "http://localhost:8002";
const REVIEW_URL = process.env.REVIEW_SERVICE_URL || "http://localhost:8003";

const http = axios.create({ timeout: 4000 });

// ---- prometheus metrics ----------------------------------------------
const client = require("prom-client");
const register = new client.Registry();
register.setDefaultLabels({ app: "ui-service" });
client.collectDefaultMetrics({ register });

const httpRequestDurationSeconds = new client.Histogram({
  name: "http_request_duration_seconds",
  help: "Duration of HTTP requests in seconds",
  labelNames: ["method", "route", "status_code"],
  buckets: [0.1, 0.3, 0.5, 0.7, 1, 3, 5, 7, 10]
});
register.registerMetric(httpRequestDurationSeconds);

app.use((req, res, next) => {
  const start = Date.now();
  res.on("finish", () => {
    const duration = (Date.now() - start) / 1000;
    let route = req.route ? req.route.path : req.path;
    if (!req.route) {
      route = route.replace(/\/\d+/g, "/:id").replace(/\/products\/[^\/]+/g, "/products/:id");
    }
    httpRequestDurationSeconds
      .labels(req.method, route || req.path, res.statusCode)
      .observe(duration);
  });
  next();
});

app.get("/metrics", async (req, res) => {
  res.setHeader("Content-Type", register.contentType);
  res.send(await register.metrics());
});

app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));
app.use(express.static(path.join(__dirname, "public")));
app.use(express.urlencoded({ extended: true }));

const START_TIME = Date.now();

// ---- health ----------------------------------------------------------
app.get("/health", (req, res) => {
  res.json({
    status: "UP",
    service: "ui-service",
    version: process.env.SERVICE_VERSION || "1.0.0",
    uptimeSeconds: Math.round((Date.now() - START_TIME) / 1000),
  });
});

// ---- home: product grid ----------------------------------------------
app.get("/", async (req, res) => {
  try {
    const category = req.query.category || "";
    const { data } = await http.get(`${CATALOGUE_URL}/api/products`, {
      params: category ? { category } : {},
    });
    const { data: catData } = await http.get(`${CATALOGUE_URL}/api/categories`);

    res.render("home", {
      products: data.items,
      categories: catData.items,
      activeCategory: category,
      pageError: null,
    });
  } catch (err) {
    console.error("home render failed:", err.message);
    res.render("home", {
      products: [],
      categories: [],
      activeCategory: "",
      pageError: "TrailHead's catalogue is temporarily unreachable. Please try again shortly.",
    });
  }
});

// ---- product detail: catalogue + recommendations + reviews -----------
app.get("/products/:id", async (req, res) => {
  const { id } = req.params;
  try {
    const productReq = http.get(`${CATALOGUE_URL}/api/products/${id}`);
    const recsReq = http
      .get(`${RECOMMENDATION_URL}/api/recommendations`, { params: { productId: id } })
      .catch(() => ({ data: { recommendations: [] } }));
    const reviewsReq = http
      .get(`${REVIEW_URL}/api/reviews/${id}`)
      .catch(() => ({ data: [] }));
    const summaryReq = http
      .get(`${REVIEW_URL}/api/reviews/${id}/summary`)
      .catch(() => ({ data: { averageRating: 0, count: 0 } }));

    const [productRes, recsRes, reviewsRes, summaryRes] = await Promise.all([
      productReq,
      recsReq,
      reviewsReq,
      summaryReq,
    ]);

    res.render("product", {
      product: productRes.data,
      recommendations: recsRes.data.recommendations || [],
      reviews: reviewsRes.data || [],
      summary: summaryRes.data || { averageRating: 0, count: 0 },
      formError: null,
    });
  } catch (err) {
    console.error("product render failed:", err.message);
    res.status(404).render("not-found", { productId: id });
  }
});

// ---- submit a review ---------------------------------------------------
app.post("/products/:id/reviews", async (req, res) => {
  const { id } = req.params;
  const { author, rating, comment } = req.body;

  try {
    await http.post(`${REVIEW_URL}/api/reviews/${id}`, {
      author: author || "Trail Guest",
      rating: Number(rating) || 5,
      comment: comment || "",
    });
    res.redirect(`/products/${id}#reviews`);
  } catch (err) {
    console.error("review submit failed:", err.message);
    res.redirect(`/products/${id}?reviewError=1#reviews`);
  }
});

app.use((req, res) => {
  res.status(404).render("not-found", { productId: null });
});

app.listen(PORT, () => {
  console.log(`trailhead ui-service listening on :${PORT}`);
  console.log(`  catalogue      -> ${CATALOGUE_URL}`);
  console.log(`  recommendation -> ${RECOMMENDATION_URL}`);
  console.log(`  review         -> ${REVIEW_URL}`);
});
