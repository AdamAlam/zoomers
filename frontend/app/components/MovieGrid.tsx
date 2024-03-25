'use client';
import Image from 'next/image';
import { Movie } from '../movie.types';
import Link from 'next/link';

interface Props {
  movies: Movie[];
}

const MovieGrid = ({ movies }: Props) => {
  const imageBaseUrl = 'https://image.tmdb.org/t/p/original';

  return (
    <div className="py-6 sm:py-12 lg:mx-auto lg:max-w-7xl lg:px-8">
      <h2 className="text-2xl font-bold tracking-tight text-gray-900">
        Popular
      </h2>

      <div className="relative mt-8">
        <div className="relative -mb-6 w-full overflow-x-auto pb-6">
          <ul
            role="list"
            className="mx-4 inline-flex space-x-2 sm:mx-6 lg:mx-0"
          >
            {movies.map(movie => (
              <li
                key={movie.id}
                className="inline-flex w-36 flex-col text-center"
              >
                <div className="group relative">
                  <div className="aspect-h-3 aspect-w-2 w-full overflow-hidden rounded-md bg-gray-200">
                    <Link href={`/movie/${movie.id}`} key={movie.id}>
                      <Image
                        src={`${imageBaseUrl}${movie.poster_path}`}
                        alt={movie.title}
                        width={200}
                        height={300}
                        className="object-cover object-center group-hover:opacity-75"
                      />
                    </Link>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};
export default MovieGrid;
