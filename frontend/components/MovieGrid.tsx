'use client';
import Image from 'next/image';
import {Movie} from '../movie.types';
import Link from 'next/link';

interface Props {
  movies: Movie[];
}
const MovieGrid = ({ movies }: Props) => {
  const imageBaseUrl = 'https://image.tmdb.org/t/p/original';

  return (
    <div className="ml-5">
      <h1>Popular</h1>
      <div
        className="flex overflow-y-hidden overflow-x-scroll p-5"
        id="movie-row"
      >
        {movies.map((movie: Movie) => (
          <Link href={`/movie/${movie.id}`} key={movie.id}>
            <Image
              src={`${imageBaseUrl}${movie.poster_path}`}
              className="mr-2 transform object-contain transition-transform hover:scale-110"
              width={200}
              height={300}
              alt={movie.title}
            />
          </Link>
        ))}
      </div>
    </div>
  );
};
export default MovieGrid;
