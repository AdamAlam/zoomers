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
    <div className="mx-auto max-w-screen-lg">
      <div className="flex flex-col items-center justify-center">
        <div className="relative mb-4 h-[500px] w-full">
          <Image
            src={`${imageUrl}${movieDetails.backdrop_path}`}
            layout="fill"
            objectFit="cover"
            alt="Movie backdrop image"
          />
          {/* Overlay for bottom fade */}
          <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-white to-transparent" />

          {/* Overlay for left side fade
          <div className="absolute bottom-0 left-0 top-0 w-32 bg-gradient-to-r from-white to-transparent" />
          {/* Overlay for right side fade */}
          {/* <div className="absolute bottom-0 right-0 top-0 w-32 bg-gradient-to-l from-white to-transparent" /> */}
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
            <h1 className="mb-2 font-serif text-3xl">{movieDetails.title}</h1>
            <p className="mb-2 text-sm uppercase">{movieDetails.tagline}</p>
            <p>{movieDetails.overview}</p>
          </div>
        </div>
      </div>
    </div>
  ) : (
    <div>Loading...</div>
  );
};

export default MovieDetail;
