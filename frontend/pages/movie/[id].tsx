'use client';

import { Movie } from '@/movie.types';
import { AspectRatio } from '@radix-ui/react-aspect-ratio';
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
    <div className="mx-auto max-w-screen-lg">
      <div className="flex flex-col items-center justify-center">
        <div className="mb-4 flex justify-center">
          <Image
            src={`${imageUrl}${movieDetails.backdrop_path}`}
            width={1024}
            height={576}
            alt="Movie backdrop image"
          />
        </div>

        <div className="flex w-full justify-start">
          <div className="mr-8 shrink-0">
            <Image
              src={`${imageUrl}${movieDetails.poster_path}`}
              alt={movieDetails.title}
              width={200}
              height={300}
              style={{ borderRadius: '10px' }}
            />
          </div>
          <div>
            <h1>{movieDetails.title}</h1>
            <p>{movieDetails.overview}</p>
          </div>
        </div>
        <div></div>
        <div></div>
      </div>
    </div>
  ) : (
    <div>Loading...</div>
  );
};
export default MovieDetail;
