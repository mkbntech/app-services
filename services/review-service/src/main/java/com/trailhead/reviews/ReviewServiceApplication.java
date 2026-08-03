package com.trailhead.reviews;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.event.ApplicationReadyEvent;
import org.springframework.context.event.EventListener;

import com.trailhead.reviews.model.Review;
import com.trailhead.reviews.repository.ReviewRepository;

/**
 * TrailHead Supply Co. — Voting / Review Service
 * Stack: Java 21 + Spring Boot 3 + Spring Data JPA + H2/Postgres
 */
@SpringBootApplication
public class ReviewServiceApplication {

    private final ReviewRepository reviewRepository;

    public ReviewServiceApplication(ReviewRepository reviewRepository) {
        this.reviewRepository = reviewRepository;
    }

    public static void main(String[] args) {
        SpringApplication.run(ReviewServiceApplication.class, args);
    }

    /**
     * Seed sample data after application is fully started.
     */
    @EventListener(ApplicationReadyEvent.class)
    public void seed() {
        if (reviewRepository.count() == 0) {
            reviewRepository.save(new Review(
                    "th-001",
                    "MarikaT",
                    5,
                    "Fits like it was measured for my torso. Survived a 4-day traverse."
            ));

            reviewRepository.save(new Review(
                    "th-001",
                    "dustin_hikes",
                    4,
                    "Great pack, wish the hip belt pockets were bigger."
            ));

            reviewRepository.save(new Review(
                    "th-003",
                    "campfirekate",
                    5,
                    "Pitched this in a hailstorm and stayed bone dry."
            ));

            reviewRepository.save(new Review(
                    "th-006",
                    "ridge_runner",
                    4,
                    "Locks hold even on scree. A little heavier than expected."
            ));
        }
    }
}