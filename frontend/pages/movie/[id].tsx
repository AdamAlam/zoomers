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

  return (
    <div className="flex h-screen w-screen flex-col bg-slate-400">
      <div
        className="absolute inset-0 mt-20 flex h-2/6 w-full items-center justify-center border-2 border-sky-950"
        style={{
          backgroundImage: `url(${imageUrl}${movieDetails?.backdrop_path})`,
          backgroundSize: 'cover',
          backgroundPosition: 'center'
        }}
      >
        <div>
          <Image
            src={`${imageUrl}${movieDetails?.poster_path}`}
            width={200}
            height={300}
            className="border-radius-2"
          />
        </div>
        <div className="text-white">
          <p className="text-3xl">{movieDetails?.title}</p>
        </div>
      </div>
    </div>
  );
};
export default MovieDetail;
