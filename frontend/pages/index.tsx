'use client';

import MovieGrid from '@/components/MovieGrid';
import { useEffect, useState } from 'react';

export default function Home() {
  const [movieList, setMovieList] = useState([]);
  useEffect(() => {
    fetch('http://localhost:8000/movies/popular')
      .then(res => res.json())
      .then(data => setMovieList(data.results));
  }, []);

  console.table(movieList);

  return (
    <div>
      <MovieGrid movies={movieList} />
    </div>
  );
}