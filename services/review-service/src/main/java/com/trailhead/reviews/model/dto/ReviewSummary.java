package com.trailhead.reviews.model.dto;

public class ReviewSummary {
    private final String productId;
    private final double averageRating;
    private final long count;

    public ReviewSummary(String productId, double averageRating, long count) {
        this.productId = productId;
        this.averageRating = averageRating;
        this.count = count;
    }

    public String getProductId() { return productId; }
    public double getAverageRating() { return averageRating; }
    public long getCount() { return count; }
}
