'use client';

import axios from 'axios';
import { useEffect, useState } from 'react';
import MovieGrid from './components/MovieGrid';
import ReviewCard from './components/ReviewCard';
import { Review } from './review.types';

export default function Home() {
  const [movieList, setMovieList] = useState([]);
  const [reviewList, setReviewsList] = useState<Review[]>([]);
  useEffect(() => {
    fetch('http://localhost:8000/movies/popular')
      .then(res => res.json())
      .then(data => setMovieList(data.results));
  }, []);

  useEffect(() => {
    // get's the user's 5 most recent reviews
    axios
      .get('http://localhost:8000/myReviews?limit=6', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('authToken')}`
        }
      })
      .then(res => setReviewsList(res.data));
  }, []);

  return (
    <div>
      <MovieGrid movies={movieList} />
      <div className="container">
        <h2 className="ml-8 text-lg font-semibold">My Recent Reviews</h2>
        <div className="container flex justify-between">
          {reviewList.map(review => (
            <div key={review.id}>
              <ReviewCard review={review} />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
