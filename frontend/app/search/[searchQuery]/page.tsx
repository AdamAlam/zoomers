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
      {searchResults && (
        <MovieGrid
          movies={searchResults}
          header={`Search results for '${decodeURI(params.searchQuery)}'`}
        />
      )}
    </div>
  );
}
export default SearchResults;
