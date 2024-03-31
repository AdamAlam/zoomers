'use client';

import Image from 'next/image';
import Link from 'next/link';
import { Movie } from '../movie.types';

interface Props {
  movies: Movie[];
}

const MovieGrid = ({ movies }: Props) => {
  const imageBaseUrl = 'https://image.tmdb.org/t/p/original';

  return (
    <div className="ml-5">
      <h1 className="text-3xl font-bold">Popular</h1>
      <div
        className="flex overflow-y-hidden overflow-x-scroll p-5"
        id="movie-row"
      >
        {movies.map((movie: Movie) => (
          <div
            className="inline-flex flex-shrink-0 px-2"
            key={movie.id}
            style={{ width: 200, height: 300 }}
          >
            <Link href={`/movie/${movie.id}`}>
              <Image
                src={`${imageBaseUrl}${movie.poster_path}`}
                className="transition-transform hover:scale-110"
                layout="fixed"
                width={200}
                height={300}
                alt={movie.title}
              />
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
};
export default MovieGrid;
