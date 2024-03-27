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
    axios
      .get('http://localhost:8000/myReviews', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('authToken')}`
        }
      })
      .then(res => setReviewsList(res.data));
  }, []);

  return (
    <div>
      <MovieGrid movies={movieList} />
      <h2 className="text-lg font-semibold">My Reviews</h2>
      <div className="flex justify-between">
        {reviewList.map(review => (
          <div key={review.id}>
            <ReviewCard review={review} />
          </div>
        ))}
      </div>
    </div>
  );
}
