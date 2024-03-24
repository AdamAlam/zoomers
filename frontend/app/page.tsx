'use client';

import { useEffect, useState } from 'react';
import MovieGrid from './components/MovieGrid';

export default function Home() {
  const [movieList, setMovieList] = useState([]);
  useEffect(() => {
    fetch('http://localhost:8000/movies/popular')
      .then((res) => res.json())
      .then((data) => setMovieList(data.results));
  }, []);

  return (
    <div>
      <MovieGrid movies={movieList} />
    </div>
  );
}
