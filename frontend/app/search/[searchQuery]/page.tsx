'use client';

import MovieGrid from '@/app/components/MovieGrid';
import axios from 'axios';
import { useEffect, useState } from 'react';

interface Props {}
function SearchResults({ params }: { params: { searchQuery: string } }) {
  const [searchResults, setSearchResults] = useState([]);
  useEffect(() => {
    axios
      .get(`/api/search/all/${params.searchQuery}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('authToken')}`
        }
      })
      .then(res => {
        console.log(res.data.results);
        setSearchResults(res.data.results);
      });
  }, [params.searchQuery]);
  return (
    <div>
      <h1>{decodeURI(params.searchQuery)}</h1>
      {searchResults && <MovieGrid movies={searchResults} />}
    </div>
  );
}
export default SearchResults;
