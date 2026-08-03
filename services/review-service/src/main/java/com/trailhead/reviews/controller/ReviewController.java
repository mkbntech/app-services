package com.trailhead.reviews.controller;

import com.trailhead.reviews.model.Review;
import com.trailhead.reviews.model.dto.ReviewRequest;
import com.trailhead.reviews.model.dto.ReviewSummary;
import com.trailhead.reviews.repository.ReviewRepository;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/reviews")
@CrossOrigin(origins = "*")
public class ReviewController {

    private final ReviewRepository repository;

    public ReviewController(ReviewRepository repository) {
        this.repository = repository;
    }

    @GetMapping("/{productId}")
    public List<Review> getReviews(@PathVariable String productId) {
        return repository.findByProductIdOrderByCreatedAtDesc(productId);
    }

    @GetMapping("/{productId}/summary")
    public ReviewSummary getSummary(@PathVariable String productId) {
        List<Review> reviews = repository.findByProductIdOrderByCreatedAtDesc(productId);
        double avg = reviews.stream().mapToInt(Review::getRating).average().orElse(0.0);
        return new ReviewSummary(productId, Math.round(avg * 10.0) / 10.0, reviews.size());
    }

    @PostMapping("/{productId}")
    public ResponseEntity<Review> addReview(@PathVariable String productId,
                                             @Valid @RequestBody ReviewRequest request) {
        Review saved = repository.save(new Review(
                productId, request.getAuthor(), request.getRating(), request.getComment()));
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }
}
