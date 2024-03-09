'use client';

import { Movie } from '@/movie.types';
import Image from 'next/image';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';

const MovieDetail = () => {
  const router = useRouter();
  const { id: movieId } = router.query;
  const [movieDetails, setMovieDetails] = useState<Movie>();
  const imageUrl = 'https://image.tmdb.org/t/p/original';

  useEffect(() => {
    if (movieId !== undefined) {
      fetch(`http://localhost:8000/movie/${movieId}}`)
        .then(res => res.json())
        .then(data => setMovieDetails(data));
    }
  }, [movieId]);

  return movieDetails ? (
    <div>
      <h1>{movieDetails.title}</h1>
      <Image
        src={`${imageUrl}${movieDetails.poster_path}`}
        alt={movieDetails.title}
        width={200}
        height={300}
      />
      <p>{movieDetails.overview}</p>
    </div>
  ) : (
    <div>Loading...</div>
  );
};
export default MovieDetail;
